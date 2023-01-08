import socket
import ssl

# Cloudflare DNS server address
DNS_SERVER_ADDRESS = ("1.1.1.1", 853)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to port 53
sock.bind(("127.0.0.1", 53))

# Set the socket to listen for incoming connections
sock.listen(5)

while True:
    # Accept an incoming connection
    client_sock, client_address = sock.accept()

    # Receive the client's DNS query
    query = client_sock.recv(1024)

    # Create a TLS context
    context = ssl.create_default_context()

    # Connect to the Cloudflare DNS server over TLS
    server_sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=DNS_SERVER_ADDRESS[0])
    server_sock.connect(DNS_SERVER_ADDRESS)

    # Send the query to the Cloudflare DNS server
    server_sock.sendall(query)

    # Receive the response from the Cloudflare DNS server
    response = server_sock.recv(1024)

    # Forward the response back to the client
    client_sock.sendall(response)

    # Close the client and server sockets
    client_sock.close()
    server_sock.close()