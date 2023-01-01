import socket
from _thread import *
import time

server = ''
port = 22222

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)
print("Waiting for a connection, Server Started")

clients = []
q_data = [None, None]


def threaded_client(client, player):
    partner = (player + 1) % 2
    pclient = clients[partner]
    time.sleep(0.1)

    while True:
        raw_data = client.recv(1024)
        if raw_data:
            pclient.sendall(raw_data)
        else:
            clients.remove(clients[player])
            clients[player].close()
            break


while True:
    conn, _ = sock.accept()
    try:
        clients.append(conn)
        print(conn)
        if len(clients) == 2:
            print(len(clients), clients)
            print("Two clients have joined, starting game...")
            for idx, client in enumerate(clients):
                client.sendall(b"start")
                start_new_thread(threaded_client, (client, idx))

    except Exception as e:
        print(e)
        conn.close()
        break
