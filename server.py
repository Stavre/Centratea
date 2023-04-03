import socket
import threading
from threading import Lock
# connection data
from game import generateNumber, evaluateSolution

host = '127.0.0.1'
port = 55555

# starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# list for clients and usernames
clients = []
usernames = []
no_tries = []

# send messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# handling message from clients
def handle(client, no_tries: list, lock):
    solution = generateNumber()
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
            lock.release()
            r = evaluateSolution(solution, [int(i) for i in list(number)])
            if r != (4, 0):
                client.send('number of centered digits: {} number of uncentered digits {} try number: {}'.format(r[0], r[1], no_tries[usernames.index(user)]).encode('ascii'))
            else:
                solution = generateNumber()
                broadcast('User {} has guessed the number in {} tries. A new number has been generated.'.format(user, no_tries[usernames.index(user)]).encode('ascii'))
                lock.acquire()
                no_tries = [0 for _ in no_tries]
                lock.release()

            # broadcast(message)
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
    lock = Lock()

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
print("Server is listening ...")
receive()
