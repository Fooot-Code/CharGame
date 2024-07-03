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

    def handle_controls(self, eventKey, screenWidth, screenHeight, dt):
        key_to_direction = {
            pygame.K_w: (0, -1),  # North
            pygame.K_d: (1, 0),   # East
            pygame.K_s: (0, 1),   # South
            pygame.K_a: (-1, 0)   # West
        }

        direction = key_to_direction.get(eventKey, (0, 0))
        dx, dy = direction

        new_x = self.x + dx * self.moveFactor * dt
        new_y = self.y + dy * self.moveFactor * dt

        if 0 <= new_x < screenWidth:
            self.pyrect.x = new_x
        if 0 <= new_y < screenHeight:
            self.pyrect.y = new_y

        if eventKey[pygame.K_SPACE]:
            self.bulletShouldSpawn = True

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pyrect)

        
        

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