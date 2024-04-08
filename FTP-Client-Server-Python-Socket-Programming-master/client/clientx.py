import socket
import os
import ssl
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog

HOST = '10.30.203.130'  # Server IP address
PORT = 2126

# SSL context creation
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl_context.wrap_socket(clientSocket)

ssl_sock.connect((HOST, PORT))

def send_command():
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
        else:
            data = ssl_sock.recv(1024)
            response_text.insert(tk.END, data.decode() + '\n')

def upload_file():
    filename = filedialog.askopenfilename()
    if filename:
        ssl_sock.sendall(f'upload {os.path.basename(filename)}'.encode())
        with open(filename, 'rb') as file:
            file_data = file.read()
        ssl_sock.sendall(file_data)
        response_text.insert(tk.END, f'File "{os.path.basename(filename)}" uploaded successfully\n')
    else:
        response_text.insert(tk.END, 'No file selected\n')

root = tk.Tk()
root.title("SSL Client")

command_label = tk.Label(root, text="Enter your command:")
command_label.pack()

command_entry = tk.Entry(root, width=50)
command_entry.pack()

send_button = tk.Button(root, text="Send", command=send_command)
send_button.pack()

upload_button = tk.Button(root, text="Upload", command=upload_file)
upload_button.pack()

response_text = scrolledtext.ScrolledText(root, width=60, height=10)
response_text.pack()

# Default command to display upon startup
response_text.insert(tk.END, 'Welcome to SSL Client\n')
response_text.insert(tk.END, 'Type list to list files\n')
response_text.insert(tk.END, 'Type dwld <filename> to download a file\n')
response_text.insert(tk.END, 'Type upload to upload a file\n')
response_text.insert(tk.END, 'Type quit to exit\n')

root.mainloop()
