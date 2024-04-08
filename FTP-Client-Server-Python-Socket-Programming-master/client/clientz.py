import socket
import os
import ssl
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'  # Server IP address
PORT = 2121

# Function to send command
def send_command(command_entry, response_text):
    command = command_entry.get()
    response_text.delete(1.0, tk.END)
    if command.lower() == 'quit':
        ssl_sock.sendall(command.encode())
        ssl_sock.close()
        root.quit()
    else:
        ssl_sock.sendall(command.encode())
        if command.lower().startswith('dwld'):
            data = ssl_sock.recv(1024)
            filename = command[5:].strip()
            with open(filename, 'wb') as file:
                file.write(data)
            response_text.insert(tk.END, f'File "{filename}" downloaded successfully\n')
        elif command.lower().startswith('upload'):
            filename = command[7:].strip()
            if os.path.exists(filename):
                with open(filename, 'rb') as file:
                    file_data = file.read()
                ssl_sock.sendall(file_data)
                response_text.insert(tk.END, f'File "{filename}" uploaded successfully\n')
            else:
                response_text.insert(tk.END, f'File "{filename}" does not exist.\n')
        else:
            data = ssl_sock.recv(1024)
            response_text.insert(tk.END, data.decode() + '\n')

# Create SSL socket and connect
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl_context.wrap_socket(clientSocket)

ssl_sock.connect((HOST, PORT))

# Create Tkinter window
root = tk.Tk()
root.title("SSL Client")

# Command entry
command_label = tk.Label(root, text="Enter your command:")
command_label.pack()

command_entry = tk.Entry(root, width=50)
command_entry.pack()

# Send button
send_button = tk.Button(root, text="Send", command=lambda: send_command(command_entry, response_text))
send_button.pack()

# Response text area
response_text = scrolledtext.ScrolledText(root, width=60, height=10)
response_text.pack()

# Run Tkinter event loop
root.mainloop()
