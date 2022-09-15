from inputnumber import *
from displaymoney import *
import pygame
from pygame.locals import *
import pygwidgets
import sys

window_width = 640
window_height = 480
fps = 30

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

title = pygwidgets.DisplayText(window, (200, 40), "Currency calculator", fontSize=30, justified='center')
Ok_BUTTON = pygwidgets.TextButton(window, (430, 150), "OK", overColor=(255, 255, 250), downColor="Yellow")
input_cap = pygwidgets.DisplayText(window, (20, 150), "Input money amount", fontSize=24, width=190, justified="right")
input_field = InputNumber(window, (230, 150), '', width=150)
output_cap1 = pygwidgets.DisplayText(window, (20, 300), "Output dollars and cents", fontSize=24, width=190, justified="right")
moneyField1 = DisplayMoney(window, (230, 300), textColor="Black", backgroundColor="White", width=150)
output_cap2 = pygwidgets.DisplayText(window, (20, 400), "Output dollars", fontSize=24, width=190, justified="right")
moneyField2 = DisplayMoney(window, (230, 400), textColor="Black", backgroundColor="White", width=150, show_cents=False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if input_field.handleEvent(event) or Ok_BUTTON.handleEvent(event):
            try:
                thevalue = input_field.getValue()
            except ValueError:
                input_field.setValue("Not a number")
            else:
                theText = str(thevalue)
                moneyField1.setValue(theText)
                moneyField2.setValue(theText)
                
    window.fill((0, 180, 180))
    title.draw()
    input_field.draw()
    input_cap.draw()
    Ok_BUTTON.draw()
    output_cap1.draw()
    output_cap2.draw()
    moneyField1.draw()
    moneyField2.draw()
    
    pygame.display.update()
    clock.tick(fps)
            