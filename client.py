import socket
import threading

# connection data
host = '127.0.0.1'
port = 55555

# choose nickname
nickname = input("Choose your nickname")

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# listening to the server and send nickname
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Enter your nickname ':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except Exception as e:
            # close the connection
            print('An error occurred')
            print(e)
            client.close()
            break

def write():
    while True:
        message = '{} {}'.format(nickname, input('')).encode('ascii')
        client.send(message)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()