import pickle
import time
import pygame
from _thread import *

import socket


class MySocket:
    def __init__(self, server="localhost", port=22222):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server  # "172.20.10.4"  # "localhost"
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


pygame.init()

window_size = (800, 400)
my_window_size = (400, 400)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Moving Rectangle')

frame_rate = 60
clock = pygame.time.Clock()

# Set the movement size of rectangle
movement_size = 50
# Create custom socket connection
conn = MySocket()

# my Rectangle
rectangle = pygame.Rect((0, 0), (50, 50))
rectangle.center = (225, 225)
color = pygame.Color('red')

# partner Rectangle(xpos+=400)
rectangle2 = pygame.Rect((0, 0), (50, 50))
rectangle2.center = (225 + 400, 225)
color2 = pygame.Color('blue')


def threaded_func(conn):
    while True:
        time.sleep(0.15)
        conn.send([rectangle.center, rectangle.size])
        rect2_data = conn.recv()
        rectangle2.center, rectangle2.size = rect2_data
        rectangle2.x += 400


# Waiting for partner
while True:
    data = conn.client.recv(16)  # pickle없이 그냥처리
    if not data:
        continue
    if data == b"start":
        print("Game start!")
        break
    time.sleep(1)

start_new_thread(threaded_func, (conn,))

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and rectangle.left > 0:
                rectangle.x -= movement_size
            elif keys[pygame.K_RIGHT] and rectangle.right < my_window_size[0]:
                rectangle.x += movement_size
            elif keys[pygame.K_UP] and rectangle.top > 0:
                rectangle.y -= movement_size
            elif keys[pygame.K_DOWN] and rectangle.bottom < my_window_size[1]:
                rectangle.y += movement_size
            else:
                pass

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, color, rectangle)
    pygame.draw.rect(screen, color2, rectangle2)

    pygame.display.flip()
    clock.tick(frame_rate)

pygame.quit()
exit(0)
