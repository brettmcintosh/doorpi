import socket
import sys


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
    finally:
        sock.close()


if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    request = {'action': 'nfc', 'nfc_id': sys.argv[1]}
    client(host, port, request)