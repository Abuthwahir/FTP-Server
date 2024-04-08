import socket
import os
import ssl

HOST = '10.30.203.130'                                                       # 192.168.1.21
PORT = 2125                                                


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)        #ssl_context =ssl.create_default_context() to Disbale SSL Authentication
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()

print(f'Server listening on {HOST}:{PORT}')

while True: # wait for                                                   #infinite loop.
    conn, addr = serverSocket.accept()                                   # Accept a new connection and get the client's address or side
    print(f'Connected with: {addr}')

    ssl_conn = ssl_context.wrap_socket(conn, server_side=True)           # wraps the connection object (conn) with the SSL context. 

    try:
        while True:
            command = ssl_conn.recv(1024).decode()                       # Receive data from ssl and decode it into strings
            print(f'Received command: {command}')

            if command.lower() == 'quit':
                break
            elif command.lower() == 'list':
                file_list = '\n'.join(os.listdir())                      #list of files in the current directory using OS or OS.listdir()
                ssl_conn.sendall(file_list.encode())                     #Encode the list and send it to the client
            elif command.lower().startswith('dwld'):
                filename = command[5:].strip()
                if filename in os.listdir():
                    with open(filename, 'rb') as file:                     
                        file_data = file.read()
                    ssl_conn.sendall(file_data)                          #Send the file data to the client
                else:
                    ssl_conn.sendall(f'File "{filename}" not found'.encode())
            elif command.lower().startswith('upload'):
                filename = command[7:].strip()
                file_data = ssl_conn.recv(1024)
                with open(filename, 'wb') as file:
                    file.write(file_data)
                ssl_conn.sendall(f'File "{filename}" uploaded successfully'.encode())
            else:
                ssl_conn.sendall('Invalid command'.encode())

    finally:
        ssl_conn.close()                                    

serverSocket.close()

