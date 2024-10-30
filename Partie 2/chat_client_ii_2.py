import socket
import sys

host = '10.33.49.118'
port = 13337 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

s.sendall(b'Hello')

data = s.recv(1024)

s.close()

if data :
    print(f"Le serveur a rÃ©pondu {repr(data)}")

sys.exit()