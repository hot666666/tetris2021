import socket
from _thread import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(2)
print("Waiting for clients to join...")

clients = []
q_data = [None, None]


def threaded_client(client, player):
    partner = (player + 1) % 2
    pclient = clients[partner]
    while True:
        q_data[partner] = client.recv(16)
        print(player, partner, q_data)
        if q_data[partner]:
            pclient.sendall(q_data[partner])
        else:
            clients.remove(pclient)
            pclient.close()
            break


while True:
    conn, addr = sock.accept()
    try:
        clients.append(conn)
        print(conn)
        if len(clients) == 2:
            print(len(clients), clients)
            print("Two clients have joined, starting game...")
            for client in clients:
                client.sendall(b"start")

            start_new_thread(threaded_client, (clients[0], 0))
            start_new_thread(threaded_client, (clients[1], 1))

    except Exception as e:
        print(e)
        conn.close()
