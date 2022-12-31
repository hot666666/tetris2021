import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(2)
print("Waiting for clients to join...")

clients = []

while True:
    connection, client_address = sock.accept()
    try:
        clients.append(connection)
        print(connection)
        if len(clients) == 2:
            print("Two clients have joined, starting game...")
            for client in clients:
                client.sendall(b"start")

            while True:
                data = clients[0].recv(16)
                if data:
                    clients[1].sendall(data)
                else:
                    clients.remove(clients[0])
                    clients[0].close()
                    break
                data = clients[1].recv(16)
                if data:
                    clients[0].sendall(data)
                else:
                    clients.remove(clients[1])
                    clients[0].close()
                    break

    except Exception as e:
        print(e)
        connection.close()
