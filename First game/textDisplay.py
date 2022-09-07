import pygame
from pygame.locals import *

class SimpleText():
    def __init__(self, window, loc, value, textColor) -> None:
        self.window = window
        self.loc = loc
        self.font = pygame.font.Font(r"C:\Users\M E T R O\OneDrive\Desktop\Study\python\6 exercise\First game\fonts\Cartoon Madness.otf", 30)
        self.textColor = textColor
        self.text = None
        
        self.setValue(value)
        
    def setValue(self, newText):
        if self.text == newText:
            return
        
        self.text = newText
        self.textSurface = self.font.render(self.text, True, self.textColor)
        
    def draw(self):
        self.window.blit(self.textSurface, self.loc)