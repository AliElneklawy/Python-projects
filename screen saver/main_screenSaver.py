from screenSaver import balls
import pygame
from pygame.locals import *
from sys import exit

# define constants
window_width = 640
window_height = 480
fps = 60

# initialize the world
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# initailize vars
balllist = []
Nballs = 3
for _ in range(Nballs):
    oBall = balls(window, window_width, window_height)
    balllist.append(oBall)

# loop
while True:
    # check and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()            

    # do any per frame action
    for oBall in balllist:
        oBall.update()

    # clear the window before doing it again
    window.fill("Black")

    # draw window elements
    for oBall in balllist:
        oBall.draw()

    # update the window
    pygame.display.update()

    # slow things down 
    clock.tick(fps)