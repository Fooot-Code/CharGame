# Simple pygame program

# Import and initialize the pygame library
import pygame
from classes import *

pygame.init()

WIDTH, HEIGHT = 1000, 600

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

bulletList = []
balloonList = []

maxBalloonCount = 3
balloonMoveFactor = 2
planeMoveFactor = 2

plane1 = Plane(0, planeMoveFactor, 0, 0, 0, 0)

# Run until the user asks to quit
running = True
while running:
    plane1.draw()
    
    if len(balloonList) < maxBalloonCount:
        for balloon in range(maxBalloonCount - len(balloonList)):
            newBalloon = Balloon(1, balloonMoveFactor, WIDTH, HEIGHT, 0, 0, 1, 3)

    for balloon in balloonList:
        balloon.draw(screen)
        if balloon.shouldBeRemoved:
            balloonList.pop(balloonList.index(balloon))

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            plane1.handle_controls(event.key)
            for bullet in bulletList:
                balloon.handle_controls()
            
    # Flip the display
    pygame.display.flip()
    

# Done! Time to quit.
pygame.quit()