import pygame
from pygame.locals import *
from random import randrange, choice

class balls():
    def __init__(self, window, width, height) -> None:
        self.window = window
        self.width = width
        self.height = height

        self.image = pygame.image.load(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\OOP\screen saver\ball.png").convert_alpha()
        ballRect = self.image.get_rect()
        self.ballwidth = ballRect.width
        self.ballheight = ballRect.height
        self.maxwidth = width - self.ballwidth
        self.maxheight = height - self.ballheight

        self.ballX = randrange(self.maxwidth)
        self.ballY = randrange(self.maxheight)

        speedlist = [-4, -3, -2, -1, 1, 2, 3, 4]
        self.speedX = choice(speedlist)
        self.speedY = choice(speedlist)

    def update(self):
        if self.ballX < 0 or self.ballX >= self.maxwidth:
            self.speedX = -self.speedX
        if self.ballY < 0 or self.ballY >= self.maxheight:
            self.speedY = -self.speedY
        
        self.ballX += self.speedX
        self.ballY += self.speedY

    def draw(self):
        self.window.blit(self.image, (self.ballX, self.ballY))