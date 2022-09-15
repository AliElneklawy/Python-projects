import pygame
from pygame.locals import *
from sys import exit
import pygwidgets
from Constants import *
from balloonMgr import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
PANEL_HEIGHT = 60
USABLE_HEIGHT = WINDOW_HEIGHT - PANEL_HEIGHT
FPS = 30

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

oScoreDisplay = pygwidgets.DisplayText(window, (10, USABLE_HEIGHT + 25), "Score: 0", fontSize=24, width=140, backgroundColor=None)
oStatusDisplay = pygwidgets.DisplayText(window, (180, USABLE_HEIGHT + 25), "", textColor="Black", backgroundColor=None)
oStartButton = pygwidgets.TextButton(window, (WINDOW_WIDTH - 110, USABLE_HEIGHT + 10), "Start")

oBalloonMgr = BalloonMgr(window, WINDOW_WIDTH, USABLE_HEIGHT)
playing = False

while True:
    nPointsEarned = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if playing:
            oBalloonMgr.handleEvent(event)
            theScore = oBalloonMgr.getScore()
            oScoreDisplay.setValue(theScore)
        elif oStartButton.handleEvent(event):
            oBalloonMgr.start()
            oScoreDisplay.setValue("Score: 0")
            playing = True
            oStartButton.disable()
            
    if playing:
        oBalloonMgr.update()
        nPopped = oBalloonMgr.getCountPopped()
        nMissed = oBalloonMgr.getCountMissed()
        oStatusDisplay.setValue("Popped: " + str(nPopped) + 
                                "   Missed: " + str(nMissed) +
                                "   Out of: " + str(N_BALLOONS))
        if nPopped + nMissed == N_BALLOONS:
            playing = False
            oStartButton.enable()
            
    window.fill((0, 180, 180))
    if playing:
        oBalloonMgr.draw()
        
    pygame.draw.rect(window, "Gray", pygame.Rect(0, USABLE_HEIGHT, WINDOW_WIDTH, PANEL_HEIGHT))
    oScoreDisplay.draw()
    oStartButton.draw()
    oStatusDisplay.draw()
    
    pygame.display.update()
    
    clock.tick(FPS)
