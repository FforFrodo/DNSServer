import socket
import ssl
import logging

DNS_SERVER_ADDRESS = ("1.1.1.1", 853)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

def create_tcp_socket():
    """
    Create a TCP socket and bind it to port 53
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 53))
    sock.listen(5)
    log.info("TCP socket created and bound to port 53")
    return sock

def handle_query(client_sock):
    """
    Handle a DNS query from a client
    """
    query = b''
    while 1:
        try:
            data = client_sock.recv(1024)
            if data:
                query += data
            else:
                log.debug("Received query from client: %s", query)
                break
        except socket.error as e:
            if e.errno == 11:
                continue
            else:
                log.error("Error receiving data from client: %s", e)
                break

    context = ssl.create_default_context()
    server_sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=DNS_SERVER_ADDRESS[0])
    server_sock.connect(DNS_SERVER_ADDRESS)

    server_sock.sendall(query)
    log.debug("Sent query to DNS server: %s", query)

    response = b''
    while 1:
        try:
            data = server_sock.recv(1024)
            if data:
                response += data
            else:
                log.debug("Received response from DNS server: %s", response)
                break
        except socket.error as e:
            if e.errno == 11:
                continue
            else:
                log.error("Error receiving data from DNS server: %s", e)
                break

    client_sock.sendall(response)
    log.debug("Sent response to client: %s", response)

    server_sock.close()
    client_sock.close()
    log.info("Closed connection with client")

def run_proxy():
    """
    Run the DNS proxy
    """
    sock = create_tcp_socket()
    while True:
        client_sock, client_address = sock.accept()
        log.info("Accepted connection from client: %s", client_address)
        handle_query(client_sock)

if __name__ == '__main__':
    run_proxy()