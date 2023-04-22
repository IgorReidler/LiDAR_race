import pygame
import math
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speedDelta=0):
        super().__init__()
        # speed delta init
        self.speedDelta = speedDelta
        self.image = pygame.image.load(r'media/vehicle2.png')
        self.rect = self.image.get_rect()
    def update(self,road_speed, screen_width, screen_height,tile_height,tilesNum_height,obstacle_height,obstacle_width,drive_width):        
        self.rect.y+=road_speed+self.speedDelta
        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            # self.rect.y = screen_height - tile_height*tilesNum_height+math.ceil(road_speed)
            self.rect.y = random.randrange(tile_height) - tile_height - obstacle_height
            self.rect.x = random.randrange(drive_width-obstacle_width)+math.ceil((screen_width-drive_width)/2)
            # block.rect.x = random.randrange(DRIVE_WIDTH-BLOCK_WIDTH)+math.ceil((SCREEN_WIDTH-DRIVE_WIDTH)/2)
