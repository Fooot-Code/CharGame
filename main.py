# Simple pygame program

# Import and initialize the pygame library
import pygame
from classes import *
from os import path

pygame.init()

WIDTH, HEIGHT = 1000, 600

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()

# Load Images
balloonImg = pygame.transform.scale(pygame.image.load("C:\\Documents\\GitHub\\CharGame\\Images\\balloon.png"), (75, 75))
planeImg = pygame.transform.scale(pygame.image.load("C:\\Documents\\GitHub\\CharGame\\Images\\Plane1.jpg"), (75, 75))
bulletImg = pygame.transform.scale(pygame.image.load("C:\\Documents\\GitHub\\CharGame\\Images\\R.jpg"), (75, 75))
popImg = pygame.transform.scale(pygame.image.load("C:\\Documents\\GitHub\\CharGame\\Images\\pop.png"), (75, 75))
bulletList = []
balloonList = []

maxBalloonCount = 3
balloonMoveFactor = 2
bulletMoveFactor = 5
planeMoveFactor = 1.5

plane1 = Plane(planeImg, planeMoveFactor, 100, 100, planeImg.get_width(), planeImg.get_height())

# Have counter for making balloon or plane have a couple of cycles before disappearing
cycleCounter = 0

# Run until the user asks to quit
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        plane1.handle_controls(keys, WIDTH, HEIGHT, dt, balloonList)

    
    if plane1.bulletShouldSpawn and len(bulletList) < 1:
        bulletList.append(Bullet(bulletImg, bulletMoveFactor, bulletImg.get_width(), bulletImg.get_height(), plane1))
    
    # Fill the background with white
    screen.fill((255, 255, 255))

    plane1.draw(screen)
    
    if len(balloonList) < maxBalloonCount:
        for balloon in range(maxBalloonCount - len(balloonList)):
            newBalloon = Balloon(balloonImg, balloonMoveFactor, WIDTH, HEIGHT, WIDTH, balloonImg.get_width(), balloonImg.get_height(), bulletList)
            balloonList.append(newBalloon)

    if len(balloonList) > 0:
        for balloon in balloonList:
            balloon.draw(screen, dt, popImg)
            if balloon.shouldBeRemoved:
                cycleCounter += 1
                if cycleCounter > 20:
                    balloonList.pop(balloonList.index(balloon))
                    cycleCounter = 0

    if len(bulletList) > 0:
        for bullet in bulletList:
            if bullet.shouldBeRemoved:
                bulletList.pop(bulletList.index(bullet))
            else:
                bullet.draw(screen, WIDTH, dt)
            

    # Flip the display
    pygame.display.flip()
    

# Done! Time to quit.
pygame.quit()