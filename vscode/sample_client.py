import socket
import pickle
import sys


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 22222
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            serialized_data = pickle.dumps(data)
            # print(sys.getsizeof(serialized_data))
            # print(serialized_data)
            self.client.send(serialized_data)

            # temp = pickle.loads(self.client.recv(2048))
            # print(sys.getsizeof(temp))
            # print(temp)
            # return temp

        except socket.error as e:
            print(e)


def main():
    run = True

    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break


if __name__ == '__main__':
    main()
