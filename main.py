# Simple pygame program

# Import and initialize the pygame library
import pygame
from classes import *
from time import sleep

pygame.init()

WIDTH, HEIGHT = 1000, 600

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()

# Load Images
balloonImg = pygame.transform.scale(pygame.image.load("Images/redBalloon.png"), (75, 75))
planeImg = pygame.transform.scale(pygame.image.load("Images/Plane1.png"), (100, 100))
bulletImg = pygame.transform.scale(pygame.image.load("Images/Bullet.png"), (35, 35))
popImg = pygame.transform.scale(pygame.image.load("Images/pop.png"), (75, 75))
backgroundImg = pygame.transform.scale(pygame.image.load("Images/bgChar.png"), (1000, 600))

scoreFont = pygame.font.SysFont("Arial", 20)

bulletList = []
balloonList = []
bulletBooleanList = [False for i in range(10)]

maxBalloonCount = 3
balloonMoveFactor = 4
bulletMoveFactor = 5
planeMoveFactor = 1.5

plane1 = Plane(planeImg, planeMoveFactor, 100, 100, planeImg.get_width(), planeImg.get_height(), bulletBooleanList)

# Have counter for making balloon or plane have a couple of cycles before disappearing
cycleCounter = 0

def end_game():
    global running

    screen.fill((0, 0, 0))

    gameDead = scoreFont.render("Game Over!", False, (255, 0, 0))
    screen.blit(gameDead, (WIDTH / 2, HEIGHT / 2))

    pygame.time.wait(3000)
    running = False

# Run until the user asks to quit
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        plane1.handle_controls(keys, WIDTH, HEIGHT, dt, balloonList)
        print(plane1.bulletShouldSpawn)
    
        if plane1.bulletShouldSpawn and len(bulletList) <= 10:
            bulletList.append(Bullet(bulletImg, bulletMoveFactor, bulletImg.get_width(), bulletImg.get_height(), plane1))

    if plane1.endGame:
        end_game()

    # Fill the background with white
    screen.blit(backgroundImg, (0, 0))

    plane1.draw(screen)

    scorePlane1 = scoreFont.render(f"Score Plane 1: {str(plane1.score)}", False, (0,0,0))
    screen.blit(scorePlane1, (0, 0))

    healthPlane1 = scoreFont.render(f"Health Plane 1: {str(plane1.health)}", False, (0, 0, 0))
    screen.blit(healthPlane1, (0, 30))
    
    if len(balloonList) < maxBalloonCount:
        for balloon in range(maxBalloonCount - len(balloonList)):
            newBalloon = Balloon(balloonImg, balloonMoveFactor, WIDTH, HEIGHT, WIDTH, balloonImg.get_width(), balloonImg.get_height(), plane1, bulletList)
            balloonList.append(newBalloon)

    if len(balloonList) > 0:
        for balloon in balloonList:
            balloon.draw(screen, dt, popImg)
            if balloon.x + balloon.width <= 0:
                plane1.health -= 1
                balloonList.pop(balloonList.index(balloon))
            if balloon.shouldBeRemoved and not balloon.x + balloon.width <= 0:
                cycleCounter += 1
                if cycleCounter > 20:
                    balloonList.pop(balloonList.index(balloon))
                    cycleCounter = 0
            
        for bullet in bulletList:
            if bullet.shouldBeRemoved:
                bulletList.pop(bulletList.index(bullet))
            else:
                bullet.draw(screen, WIDTH, dt)
            

    # Flip the display
    pygame.display.flip()
    

# Done! Time to quit.
pygame.quit()