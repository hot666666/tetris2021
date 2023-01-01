import socket
import pickle
import sys


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"  # "172.20.10.4"  # "localhost"
        self.port = 22222
        self.addr = (self.server, self.port)

        try:
            self.client.connect(self.addr)
        except:
            print('connection error')

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
