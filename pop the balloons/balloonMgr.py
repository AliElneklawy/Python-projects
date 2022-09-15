import pygame
from pygame.locals import *
import random
import pygwidgets
from Constants import *
from balloon import *

class BalloonMgr():
    def __init__(self, window, maxW, maxH) -> None:
        self.window = window
        self.maxW = maxW
        self.maxH = maxH
        self.score = 0
        
    def start(self):
        self.balloonList = []
        self.nPopped = 0
        self.nMissed = 0
        
        for balloonNum in range(N_BALLOONS):
            randBalloonClass = random.choice((BalloonSmall, BalloonMed, BalloonLarge))
            oBalloon = randBalloonClass(self.window, self.maxW, self.maxH, balloonNum)
            self.balloonList.append(oBalloon)
            
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for oBalloon in reversed(self.balloonList):
                wasHit, nPoints = oBalloon.clickedInside(event.pos)
                if wasHit:
                    if nPoints > 0:
                        self.balloonList.remove(oBalloon)
                        self.nPopped += 1
                        self.score += nPoints
                    return
                    
    def update(self):
        for oBalloon in self.balloonList:
            status = oBalloon.update()
            if status == BALLOON_MISSED:
                self.balloonList.remove(oBalloon)
                self.nMissed += 1
                
    def getScore(self):
        return self.score
    
    def getCountPopped(self):
        return self.nPopped
    
    def getCountMissed(self):
        return self.nMissed
    
    def draw(self):
        for oBalloon in self.balloonList:
            oBalloon.draw()
            