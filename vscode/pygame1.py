import pickle

import pygame
from sample_client import Network

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 400)
my_window_size = (400, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption('Moving Rectangle')

# Set the frame rate
frame_rate = 60
# Set the clock
clock = pygame.time.Clock()

# Set the speed at which the rectangle will move
movement_size = 50

# Create a rectangle with a size of (50, 50) and a color of red
rectangle = pygame.Rect((0, 0), (50, 50))
rectangle.center = (225, 225)  # Set the initial position of the rectangle
color = pygame.Color('red')

# player
rectangle2 = pygame.Rect((0, 0), (50, 50))
rectangle2.center = (225 + 400, 225)  # Set the initial position of the rectangle
color2 = pygame.Color('blue')

n = Network()
player = int(n.getP())
print("You are player", player)
temp = None

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

            n.send([rectangle.center, rectangle.size])
            temp = n.client.recv(2048)
            if temp:
                temp = pickle.loads(temp)
                rectangle2.center, rectangle2.size = temp
                rectangle2.x += 400

    # Fill the screen with a background color
    screen.fill((255, 255, 255))

    # Draw the rectangle on the screen
    pygame.draw.rect(screen, color, rectangle)

    pygame.draw.rect(screen, color2, rectangle2)

    # Update the display
    pygame.display.flip()
    # Limit the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
exit(0)
