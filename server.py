import socket
import threading
from threading import Lock
from game import generateNumber, evaluateSolution

# connection data
host = '127.0.0.1'
port = 55555

# list for clients and usernames
clients = []
usernames = []
no_tries = []
solution = 0

# send messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# handling message from clients
def handle(client, no_tries: list, lock):
    global solution
    global answer
    while True:
        try:
            # broadcast message
            message = client.recv(1024).decode('ascii')
            print('tries')
            print(no_tries)
            print('number {}'.format(message))
            print('solution {}'.format(solution))

            user = message.split(" ")[0]
            number = message.split(" ")[1]
            print('answer')
            print([int(i) for i in list(number)])
            lock.acquire()
            no_tries[usernames.index(user)] = no_tries[usernames.index(user)] + 1
            r = evaluateSolution(solution, [int(i) for i in list(number)])
            lock.release()
            if r != (4, 0):
                client.send('number of centered digits: {} number of uncentered digits {} try number: {}'.format(r[0], r[1], no_tries[usernames.index(user)]).encode('ascii'))
            else:
                broadcast('User {} has guessed the number in {} tries. A new number has been generated.'.format(user, no_tries[usernames.index(user)]).encode('ascii'))
                lock.acquire()
                solution = generateNumber()
                no_tries = [0 for _ in no_tries]
                lock.release()
        except:
            # removing and closing client
            lock.acquire()
            index = clients.index(client)
            clients[index].close()
            clients.pop(index)
            nickname = usernames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            usernames.pop(index)
            no_tries.pop(index)
            lock.release()
            break

# receiving / listening
def receive():
    global solution
    lock = Lock()
    lock.acquire()
    solution = generateNumber()
    lock.release()

    while True:
        # accept connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # request and store nickname
        client.send('Enter your nickname '.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        while (nickname in usernames):
            client.send('This username already exists. Pick another one'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
        lock.acquire()
        usernames.append(nickname)
        no_tries.append(0)
        clients.append(client)
        lock.release()

        client.send('Connected to server. Guess the four digit number'.encode('ascii'))

        # start thread for client
        thread = threading.Thread(target=handle, args=(client, no_tries, lock, ))
        thread.start()


# starting server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port))
    server.listen()
    print("Server is listening ...")
    receive()
