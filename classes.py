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

        self.bulletShouldSpawn = False
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pyrect)

    def handle_controls(self, eventKey, screenWidth, screenHeight):
        canMove = self.y + self.height <= screenHeight and self.y >= 0 and self.x + self.width < screenWidth and self.x >= 0 # wont move if at top or bottom or sides of screen
        if canMove:
            if eventKey == pygame.K_w:
                self.y -= self.moveFactor
            elif eventKey == pygame.K_a:
                self.x -= self.moveFactor
            elif eventKey == pygame.K_s:
                self.y += self.moveFactor
            elif eventKey == pygame.K_d:
                self.x += self.moveFactor
            elif eventKey == pygame.K_SPACE:
                self.bulletShouldSpawn = True

        self.pyrect = update_rect(self.x, self.y, self.width, self.height)

    def return_rect(self) -> pygame.Rect:
        return self.pyrect
    
    def return_bullet_spawn(self) -> bool:
        return self.bulletShouldSpawn

class Bullet(Plane):
    def __init__(self, image, moveFactor, x, y, width, height, plane: Plane):
        super().__init__(image, moveFactor, x, y, width, height)

        self.plane = plane
        self.planeRect = self.plane.return_rect()
        

    def draw(self, screen: pygame.Surface):
        self.planeRect = self.pla
        screen.blit(self.image, pygame.Rect(self.planeRect.x + self.planeRect.width, self.planeRect.y + (self.planeRect.height - 20), self.width, self.height)) # change the - 20 because you need it to be at the top of the gun, so that the bullet shoots out of it

    @override
    def handle_controls(self, eventKey, screenWidth):
        if eventKey == pygame.K_SPACE:
            while self.x < screenWidth:
                self.x += self.moveFactor

        self.pyrect = update_rect(self.x, self.y, self.width, self.height)

class Balloon:
    def __init__(self, image, moveFactor, screenWidth, screenHeight, x,width, height, bullet: Bullet):
        self.self = self
        self.image = image
        self.moveFactor = moveFactor
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.x = x
        self.width = width
        self.height = height

        self.shouldBeRemoved = False
        self.y = randint(0, self.screenHeight - self.width)
        self.bullet = bullet.return_rect()
        self.pyrect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pyrect)
        self.x += self.moveFactor
        if self.pyrect.colliderect(self.bullet):
            self.shouldBeRemoved = True