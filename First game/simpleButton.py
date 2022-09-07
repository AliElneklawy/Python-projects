import pygame
from pygame.locals import *

class SimpleButton():

    STATE_IDLE = "idle"
    STATE_ARMED = "armed"
    STATE_DISARMED = "disarmed"

    def __init__(self, window, loc, up, down) -> None:
        self.window = window
        self.loc = loc
        self.surfaceUp = pygame.image.load(up)
        self.surfaceDown = pygame.image.load(down)
        self.rect = self.surfaceUp.get_rect() # get_rect always starts at (0, 0) with same width and height of the given image
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]
        self.state = SimpleButton.STATE_IDLE

    def handle_event(self, eventObj) -> bool:
        if eventObj.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
            return False

        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if self.state == SimpleButton.STATE_IDLE:
            if (eventObj.type == MOUSEBUTTONDOWN) and eventPointInButtonRect:
                self.state = SimpleButton.STATE_ARMED

        elif self.state == SimpleButton.STATE_ARMED:
            if (eventObj.type == MOUSEBUTTONUP) and eventPointInButtonRect:
                self.state = SimpleButton.STATE_IDLE
                return True

            if (eventObj.type == MOUSEMOTION) and (not eventPointInButtonRect):
                self.state = SimpleButton.STATE_DISARMED
            
        elif self.state == SimpleButton.STATE_DISARMED:
            if eventPointInButtonRect:
                self.state = SimpleButton.STATE_ARMED
            elif eventObj.type == MOUSEBUTTONUP:
                self.state = SimpleButton.STATE_IDLE
        
        return False
                
    def draw(self) -> None:
        if self.state == SimpleButton.STATE_ARMED:
            self.window.blit(self.surfaceDown, self.loc)
        else:
            self.window.blit(self.surfaceUp, self.loc)
