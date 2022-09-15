import pygame
from pygame.locals import *
import random
import pygwidgets
from Constants import *
from abc import ABC, abstractmethod

SOUND_PATH = r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\OOP\pop the balloons\sounds"
IMG_PATH = r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\OOP\pop the balloons\images"

class Balloon(ABC):
    popSoundLoaded = False
    popSound = None
    
    @abstractmethod
    def __init__(self, window, maxW, maxH, ID, oImage, size, nPoints, speedY) -> None:
        self.window = window
        self.ID = ID
        self.ballonImage = oImage
        self.size = size
        self.nPoints = nPoints
        self.speedY = speedY
        if not Balloon.popSoundLoaded:
            Balloon.popSoundLoaded = True
            Balloon.popSound = pygame.mixer.Sound(f"{SOUND_PATH}\\popped.wav")
            
        balloonRect = self.ballonImage.getRect()
        self.width = balloonRect.width
        self.height = balloonRect.height
        self.x = random.randrange(maxW - self.width)
        self.y = maxH + random.randrange(75)
        self.ballonImage.setLoc((self.x, self.y))
        
    def clickedInside(self, mousePoint):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if myRect.collidepoint(mousePoint):
            Balloon.popSound.play()
            return True, self.nPoints
        else:
            return False, 0
        
    def update(self):
        self.y -= self.speedY
        self.ballonImage.setLoc((self.x, self.y))
        if self.y < -self.height:
            return BALLOON_MISSED
        else:
            return BALLON_MOVING
        
    def draw(self):
        self.ballonImage.draw()
        
    def __del__(self):
        print(self.size, "Balloon", self.ID, "is going away")
        
class BalloonSmall(Balloon):
    ballonImage = pygame.image.load(f"{IMG_PATH}\\redBalloonSmall.png")
    def __init__(self, window, maxW, maxH, ID) -> None:
        oImage = pygwidgets.Image(window, (0, 0), BalloonSmall.ballonImage)
        
        super().__init__(window, maxW, maxH, ID, oImage, "Small", 30, 3.1)
        
class BalloonMed(Balloon):
    ballonImage = pygame.image.load(f"{IMG_PATH}\\redBalloonMedium.png")
    def __init__(self, window, maxW, maxH, ID) -> None:
        oImage = pygwidgets.Image(window, (0, 0), BalloonMed.ballonImage)
        
        super().__init__(window, maxW, maxH, ID, oImage, "Medium", 20, 2.2)
        
class BalloonLarge(Balloon):
    
    ballonImage = pygame.image.load(f"{IMG_PATH}\\redBalloonLarge.png")
    def __init__(self, window, maxW, maxH, ID) -> None:
        oImage = pygwidgets.Image(window, (0, 0), BalloonLarge.ballonImage)
        
        super().__init__(window, maxW, maxH, ID, oImage, "Large", 10, 1.5)