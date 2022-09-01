import pygame
from pygame.locals import *
from sys import exit
from random import randrange

# define the constants
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
my_color = (10, 100, 200)
width = 1000
height = 700
frames_per_second = 60
chaser_width_height = 90 # pixels
max_width = width - chaser_width_height
max_height = height - chaser_width_height
target_width_height = 120
npixels_to_move = 10

# initialize the window
pygame.init()
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# load assets
chaser = pygame.image.load(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\chaser.png")
target = pygame.image.load(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\target2.png")
bounceSound = pygame.mixer.Sound(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\Cartoon Bounce Sound Effect.wav")
backgroundPic = pygame.image.load(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\backgroung.jpg")
backgroundSound = pygame.mixer.music.load(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\Chapter_5_PygameDemo4_OneballBounce_sounds_background.mp3")
pygame.mixer.music.play(-1, 0, 0)

# initialize the variables
chaserX = randrange(max_width)
chaserY = randrange(max_height)
chaserRect = pygame.Rect(chaserX, chaserY, chaser_width_height, chaser_width_height)
target_x = randrange(max_width)
target_y = randrange(max_height)
target_y = 320
targetRect = pygame.Rect(target_x, target_y, target_width_height, target_width_height)

while True:
    # check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:  # if this event's occurs, pygame creates an event object containing alot of data
            chaserX = randrange(max_width)
            chaserY = randrange(max_height)
            chaserRect = pygame.Rect(chaserX, chaserY, chaser_width_height, chaser_width_height)

    # per frame action
    keyPressedTuple = pygame.key.get_pressed()  # this return which key is currently down at each frame. 0 if key up 1 if key down
    if keyPressedTuple[pygame.K_LEFT]:
        chaserX -= npixels_to_move
    elif keyPressedTuple[pygame.K_RIGHT]:
        chaserX += npixels_to_move
    elif keyPressedTuple[pygame.K_UP]:
        chaserY -= npixels_to_move
    elif keyPressedTuple[pygame.K_DOWN]:
        chaserY += npixels_to_move

    if chaserY < 0:
        chaserY = max_height
    elif chaserY > height:
        chaserY = 0
    elif chaserX < 0:
        chaserX = max_width
    elif chaserX > max_width:
        chaserX = 0
    chaserRect = pygame.Rect(chaserX, chaserY, chaser_width_height, chaser_width_height)

    if chaserRect.colliderect(targetRect):
        bounceSound.play()
        target_x = randrange(max_width)
        target_y = randrange(max_height)
        targetRect = pygame.Rect(target_x, target_y, target_width_height, target_width_height)

    # window.fill(my_color)
    window.blit(backgroundPic, (0, 0))
    window.blit(target, (target_x, target_y))
    window.blit(chaser, (chaserX, chaserY))
    pygame.display.update()
    clock.tick(frames_per_second) # pause
