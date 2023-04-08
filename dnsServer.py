import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

register_data = {}

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to a specific address and port
    s.bind((HOST, PORT))
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        # Receive data from the client
        data, addr = s.recvfrom(1024)
        # Process the received data
        message = data.decode()
        if message.startswith("register:"):
            # Extract the hostname, IP source gateway, and public key from the message
            _, register_data_str = message.split(":")
            hostname, ip_src_gateway, public_key = register_data_str.split(";")
            # Store the register data in a dictionary
            register_data[hostname] = {
                "ip_src_gateway": ip_src_gateway,
                "public_key": public_key
            }
            print(f"Registered {hostname} with IP source gateway {ip_src_gateway} and public key {public_key}")
            # Send a response back to the client
            response = "Registration successful"
            s.sendto(response.encode(), addr)
        elif message.startswith("dnsQuery:"):
            # Extract the hostname from the message
            _, hostname = message.split(":")
            hostname = hostname.strip()
            if hostname in register_data:
                # Retrieve the IP source gateway and public key for the specified hostname
                ip_src_gateway = register_data[hostname]["ip_src_gateway"]
                public_key = register_data[hostname]["public_key"]
                # Send a response back to the client with the IP source gateway and public key
                response = f"{ip_src_gateway},{public_key}"
                s.sendto(response.encode(), addr)
            else:
                # Send an error message back to the client if the specified hostname is not registered
                response = f"Hostname '{hostname}' not found"
                s.sendto(response.encode(), addr)
        else:
            # Send an error message back to the client if the message is in an invalid format
            response = "Invalid message format"
            s.sendto(response.encode(), addr)
