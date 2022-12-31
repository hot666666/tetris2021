import socket
from _thread import *


def threaded_client(conn, pnum, game_id):
    '''
    This function is called when a new client connects to the server.
    each player in the game will be assigned a number (0 or 1)
    each player will be assigned a game id
    each player will send data to server and server will send data to other player

    :param conn: accepted connection
    :param pnum: id for the player
    :param game_id: id for the game(two palyers per game)
    :return:
    '''

    global idCount
    conn.send(str.encode(str(pnum)))

    while True:
        try:
            data = conn.recv(2048)

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    conn.sendall(data)
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    idCount -= 1
    conn.close()


games = {}
idCount = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    pnum = 0
    game_id = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[game_id] = game_id
        print("Creating a new game...")
    else:
        games[game_id].append(pnum)
        pnum = 1

    start_new_thread(threaded_client, (conn, pnum, game_id))