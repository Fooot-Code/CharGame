import pygame
from typing import override
from random import randint

def update_rect(x, y, width, height):
    return pygame.Rect(x, y, width, height)

class Plane:
    def __init__(self, image, moveFactor, x, y, width, height):
        self.self = self
        self.image = image
        self.moveFactor = moveFactor
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.moveNorth = False
        self.moveEast = False
        self.moveSouth = False
        self.moveWest = False
        self.movementX = 0
        self.movementY = 0
        self.bulletShouldSpawn = False
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        self.x += self.movementX
        self.y += self.movementY

        self.pyrect = update_rect(self.x, self.y, self.width, self.height)

        screen.blit(self.image, self.pyrect)

    def handle_controls(self, eventKey, screenWidth, screenHeight, dt, balloonList):
        
        canMoveNorth = self.y >= 0
        canMoveEast = self.x + self.width <= screenWidth
        canMoveSouth = self.y + self.height <= screenHeight
        canMoveWest = self.x >= 0

        self.movementX = 0
        self.movementY = 0

        deltaAdjMovementFactor = self.moveFactor * dt

        if eventKey[pygame.K_w] and canMoveNorth:
            self.movementY -= deltaAdjMovementFactor

        elif eventKey[pygame.K_d] and canMoveEast:
            self.movementX += deltaAdjMovementFactor

        elif eventKey[pygame.K_s] and canMoveSouth:
            self.movementY += deltaAdjMovementFactor

        elif eventKey[pygame.K_a] and canMoveWest:
            self.movementX -= deltaAdjMovementFactor

        if eventKey[pygame.K_w] and eventKey[pygame.K_d] and canMoveNorth and canMoveEast:
            # Move diagonally up and to the right
            self.movementX += deltaAdjMovementFactor
            self.movementY -= deltaAdjMovementFactor

        elif eventKey[pygame.K_w] and eventKey[pygame.K_a]:
            # up and to the left
            self.movementX -= deltaAdjMovementFactor
            self.movementY -= deltaAdjMovementFactor

        elif eventKey[pygame.K_s] and eventKey[pygame.K_d]:
            # Move diagonally down and to the right
            self.movementX += deltaAdjMovementFactor
            self.movementY += deltaAdjMovementFactor

        elif eventKey[pygame.K_s] and eventKey[pygame.K_a]:
            # Move diagonally down and to the left
            self.movementX -= deltaAdjMovementFactor
            self.movementY += deltaAdjMovementFactor

        if eventKey[pygame.K_SPACE]:
            self.bulletShouldSpawn = True

        if len(balloonList) > 0:
            for balloon in balloonList:
                if self.pyrect.colliderect(balloon.return_rect()):
                    print("dead")

    def return_rect(self) -> pygame.Rect:
        return self.pyrect
    
    def return_bullet_spawn(self) -> bool:
        return self.bulletShouldSpawn

class Bullet:
    def __init__(self, image, moveFactor, x, y, width, height, plane: Plane):
        self.self = self
        self.image = image
        self.moveFactor = moveFactor
        self.width = width
        self.height = height

        self.plane = plane
        self.x = self.plane.x + self.plane.width
        self.y = self.plane.y
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shouldBeRemoved = False
        self.spaceKeyPressed = False

    def draw(self, screen, screenWidth, dt):
        if self.plane.bulletShouldSpawn:
            self.x += self.moveFactor * dt
            
            self.pyrect = update_rect(self.x, self.y, self.width, self.height)
            screen.blit(self.image, self.pyrect)
        
        if self.x >= screenWidth:
            self.shouldBeRemoved = True
            self.plane.bulletShouldSpawn = False

    def return_rect(self) -> pygame.Rect:
        return self.pyrect



class Balloon:
    def __init__(self, image, moveFactor, screenWidth, screenHeight, x, width, height, bulletList: list):
        self.self = self
        self.image = image
        self.moveFactor = moveFactor
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.x = x
        self.width = width
        self.height = height
        self.bulletList = bulletList

        self.shouldBeRemoved = False
        self.y = randint(0, self.screenHeight - self.width)
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface, dt):
        
        self.x -= self.moveFactor * dt

        if self.bulletList != None:
            for bullet in self.bulletList:
                if self.pyrect.colliderect(bullet.return_rect()):
                    self.shouldBeRemoved = True

        if self.x + self.width <= 0:
            self.shouldBeRemoved = True

        self.pyrect = update_rect(self.x, self.y, self.width, self.height)

        screen.blit(self.image, self.pyrect)

    def return_rect(self):
        return self.pyrect