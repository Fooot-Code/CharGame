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
        self.bulletShouldSpawn = False
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface, dt):
        if self.moveNorth:
            self.pyrect.y -= self.moveFactor * dt
        elif self.moveEast:
            self.pyrect.x += self.moveFactor * dt
        elif self.moveSouth:
            self.pyrect.y += self.moveFactor * dt
        elif self.moveWest:
            self.pyrect.x -= self.moveFactor * dt

        screen.blit(self.image, self.pyrect)

    def handle_controls(self, eventKey, screenWidth, screenHeight):
        canMoveNorth = self.y > 0
        canMoveEast = self.x + self.width < screenWidth
        canMoveSouth = self.y + self.height < screenHeight
        canMoveWest = self.x >= 0


        if eventKey[pygame.K_w] and canMoveNorth:
            self.moveNorth = True
            self.moveEast = False
            self.moveSouth = False
            self.moveWest = False
        elif eventKey[pygame.K_d] and canMoveEast:
            self.moveEast = True
            self.moveNorth = False
            self.moveSouth = False
            self.moveWest = False
        elif eventKey[pygame.K_s] and canMoveSouth:
            self.moveSouth = True
            self.moveWest = False
            self.moveNorth = False
            self.moveEast = False
        elif eventKey[pygame.K_a] and canMoveWest:
            self.moveWest = True
            self.moveNorth = False
            self.moveEast = False
            self.moveSouth = False
        elif eventKey[pygame.K_SPACE]:
            self.bulletShouldSpawn = True

        
        

    def return_rect(self) -> pygame.Rect:
        return self.pyrect
    
    def return_bullet_spawn(self) -> bool:
        return self.bulletShouldSpawn

class Bullet(Plane):
    def __init__(self, image, moveFactor, x, y, width, height, plane: Plane):
        super().__init__(image, moveFactor, x, y, width, height)

        self.plane = plane
        self.shouldBeRemoved = False
        self.spaceKeyPressed = False
        

    def draw(self, screen: pygame.Surface):
        self.planeRect = self.plane.return_rect()
        screen.blit(self.image, pygame.Rect(self.planeRect.x + self.planeRect.width, self.planeRect.y + (self.planeRect.height - 20), self.width, self.height)) # change the - 20 because you need it to be at the top of the gun, so that the bullet shoots out of it

    @override
    def handle_controls(self, eventKey, screenWidth):
        self.spaceKeyPressed = True if eventKey == pygame.K_SPACE else False

        if self.x > screenWidth and self.spaceKeyPressed:
            self.x += self.moveFactor
        
        self.pyrect = update_rect(self.x, self.y, self.width, self.height)

class Balloon:
    def __init__(self, image, moveFactor, screenWidth, screenHeight, x,width, height, bulletList: list):
        self.self = self
        self.image = image
        self.moveFactor = moveFactor
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.x = x
        self.width = width
        self.height = height
        self.bulletList = bulletList if len(bulletList) > 0 else None

        self.shouldBeRemoved = False
        self.y = randint(0, self.screenHeight - self.width)
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pyrect)
        self.x += self.moveFactor
        if self.bulletList != None:
            for bullet in self.bulletList:
                if self.pyrect.colliderect(bullet):
                    self.shouldBeRemoved = True