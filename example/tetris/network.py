from _thread import *
import socket
import pickle


class MySocket:
    def __init__(self, server="localhost", port=22222):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server  # "172.20.10.4"
        self.port = port
        self.addr = (self.server, self.port)

        try:
            self.client.connect(self.addr)
        except Exception as e:
            print(e)

    def send(self, rect_data):
        try:
            serialized_data = pickle.dumps(rect_data)
            self.client.send(serialized_data)
        except socket.error as e:
            print(e)

    def recv(self, size=1024):
        while True:
            try:
                temp = self.client.recv(size)
                if temp:
                    return pickle.loads(temp)
            except socket.error as e:
                print(e)
                break
