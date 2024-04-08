import socket
import os
import ssl

HOST = '127.0.0.1'  # Server IP address
PORT = 2121

# SSL context creation
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl_context.wrap_socket(clientSocket)

ssl_sock.connect((HOST, PORT))

while True:
    command = input('Enter your command: ')
    ssl_sock.sendall(command.encode())

    if command.lower() == 'quit':
        break

    if command.lower().startswith('dwld'):
        data = ssl_sock.recv(1024)
        filename = command[5:].strip()
        with open(filename, 'wb') as file:
            file.write(data)
        print(f'File "{filename}" downloaded successfully')

    elif command.lower().startswith('upload'):
        filename = command[7:].strip()
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                file_data = file.read()
            ssl_sock.sendall(file_data)
            print(f'File "{filename}" uploaded successfully')
        else:
            print(f'File "{filename}" does not exist.')

    else:
        data = ssl_sock.recv(1024)
        print(data.decode())

ssl_sock.close()
