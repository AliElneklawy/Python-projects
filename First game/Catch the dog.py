import pygame
from pygame.locals import *
from sys import exit
from random import randrange
from textDisplay import SimpleText
from simpleButton import SimpleButton

# define the constants
path = r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\First game"
black = (0, 0, 0)
my_color = (10, 100, 200)
width = 1000
height = 700
frames_per_second = 60
chaser_width_height = 90 # pixels
max_width = width - chaser_width_height
max_height = height - chaser_width_height
target_width_height = 120
npixels_to_move = 10

# initialize the world
pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the dog")
clock = pygame.time.Clock()

# load assets
chaser = pygame.image.load(f"{path}\\images\\chaser.png").convert_alpha()
target = pygame.image.load(f"{path}\\images\\target2.png").convert_alpha()
backgroundPic = pygame.image.load(f"{path}\\images\\backgroung.jpg").convert()
bounceSound = pygame.mixer.Sound(f"{path}\\sounds\\Cartoon Bounce Sound Effect.wav")
backgroundSound = pygame.mixer.music.load(f"{path}\\sounds\\Chapter_5_PygameDemo4_OneballBounce_sounds_background.mp3")
pygame.mixer.music.play(-1, 0, 0)

# initialize the variables
chaserRect = chaser.get_rect() # this returns a rect object which we will save in chaserRect var
chaserRect.left = randrange(max_width)
chaserRect.top = randrange(max_height)

targetRect = target.get_rect()
targetRect.left = randrange(max_width)
targetRect.top = randrange(max_height)

oCollisionsLabel = SimpleText(window, (10, 20), "Score ", black)
oCollisionsCounter = SimpleText(window, (140, 20), "0", black)
oRestartButton = SimpleButton(window, (870, 20), f"{path}\\buttons\\restartUp.png", f"{path}\\buttons\\restartDown.png")
collisionsCounter = 0

while True:
    # check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:  # if this event's occurs, pygame creates an event object containing alot of data
            if chaserRect.collidepoint(event.pos):  # if the click was inside the rect
                chaserRect = chaser.get_rect()
                chaserRect.left = randrange(max_width)
                chaserRect.top = randrange(max_height)

        if oRestartButton.handle_event(event):
            collisionsCounter = 0
            oCollisionsCounter.setValue("0")

    # per frame actions
    keyPressedTuple = pygame.key.get_pressed()  # this return which key is currently down at each frame. 0 if key up 1 if key down
    if keyPressedTuple[pygame.K_LEFT]:
        chaserRect.left -= npixels_to_move
    elif keyPressedTuple[pygame.K_RIGHT]:
        chaserRect.left += npixels_to_move
    elif keyPressedTuple[pygame.K_UP]:
        chaserRect.top -= npixels_to_move
    elif keyPressedTuple[pygame.K_DOWN]:
        chaserRect.top += npixels_to_move

    if chaserRect.top < 0:
        chaserRect.top = max_height
    elif chaserRect.top > height:
        chaserRect.top = 0
    elif chaserRect.left < 0:
        chaserRect.left = max_width
    elif chaserRect.left > max_width:
        chaserRect.left = 0

    if chaserRect.colliderect(targetRect):
        bounceSound.play()
        collisionsCounter += 1
        oCollisionsCounter.setValue(str(collisionsCounter))
        targetRect = target.get_rect()
        targetRect.left = randrange(max_width)
        targetRect.top = randrange(max_height)

    window.blit(backgroundPic, (0, 0))
    window.blit(target, targetRect)
    window.blit(chaser, chaserRect)
    oCollisionsCounter.draw()
    oCollisionsLabel.draw()
    oRestartButton.draw()
    pygame.display.update()
    clock.tick(frames_per_second) # pause
