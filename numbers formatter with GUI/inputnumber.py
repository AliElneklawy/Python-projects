import pygame
from pygame.locals import *
import pygwidgets

legal_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END,
              pygame.K_KP_ENTER, pygame.K_DELETE, pygame.K_BACKSPACE,
              pygame.K_RETURN)

legal_chars = ('0123456789.-')

class InputNumber(pygwidgets.InputText):
    def __init__(self, window, loc, value='', fontName=None, fontSize=24,
                 width=200, textColor="Black", backgroundColor="White", focusColor="Black",
                 initialFocus=False, nickname=None, callBack=None,
                 mask=None, keepFocusOnSubmit=False,
                 allowFloatingNumber=True, allowNegNumber=True):

        self.allowFloatingNumber = allowFloatingNumber
        self.allowNegNumber = allowNegNumber

        super().__init__(window, loc, value, fontName, fontSize, width, textColor,
                         backgroundColor, focusColor, initialFocus, nickname,
                         callBack, mask, keepFocusOnSubmit)

    def handleEvent(self, event):
        if (event.type == pygame.KEYDOWN):
            allowed_key = (event.key in legal_keys) or (event.unicode in legal_chars)
            
            if not allowed_key: 
                return False
            
            if event.unicode == '-':
                if not self.allowNegNumber:
                    return False
                if self.cursorPosition > 0:
                    return False
                if '-' in self.text:
                    return False
                
            if event.unicode == '.':
                if not self.allowFloatingNumber:
                    return False
                if '.' in self.text:
                    return False
                
        res = super().handleEvent(event)
        return res
        
    def getValue(self):
        user_in = super().getValue()
        try:
            if self.allowFloatingNumber:
                retVal = float(user_in)
            else:
                retVal = int(user_in)
        except ValueError:
            raise ValueError("Entry is not a number.")
        
        return retVal
