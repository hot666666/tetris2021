import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

while True:
    data = sock.recv(16)
    if not data:
        continue
    if data == b"start":
        print("Game started!")
        break
    print(data)
    time.sleep(0.5)

while True:
    message = input(
        "Enter a message to send (enter 'exit' to close the connection): ")
    sock.sendall(message.encode())
    if message == "exit":
        break

    data = sock.recv(16)
    if data:
        print("Received:", data.decode())
    else:
        print('here - no data')
        break

sock.close()
