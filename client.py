import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        # Prompt the user for input
        message = input("Enter message: ")
        if message.lower() == "exit":
            # Send an exit message to the server and break the loop
            s.sendto("exit".encode(), (HOST, PORT))
            break
        # Send the message to the server
        s.sendto(message.encode(), (HOST, PORT))
        # Receive a response from the server
        data, addr = s.recvfrom(1024)
        print(data.decode())
