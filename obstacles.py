import pygame
import math
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speedDelta=0):
        super().__init__()
        # speed delta init
        self.speedDelta = speedDelta
        vehicle_images = [r'media/vehicle1.png', r'media/vehicle2.png']
        self.image = pygame.image.load(vehicle_images[random.randint(0,len(vehicle_images)-1)])
        self.rect = self.image.get_rect()
        self.lateralDir=random.randint(0, 1) * 2 - 1
    def update(self,vehicle_speed, lateral_chance,screen_height,tile_height,tilesNum_height,obstacle_height,obstacle_width,drive_width):        
        self.rect.y+=vehicle_speed+self.speedDelta
        if random.randrange(0,10)>(1-lateral_chance)*10:
            self.rect.x+=1*self.lateralDir

        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            self.rect.x = random.randrange(0,4)*150+375-obstacle_width/2 + random.randint(-25,25)
            self.rect.y = random.randrange(tile_height) - tile_height - obstacle_height
            # self.rect.x = random.randrange(drive_width-obstacle_width)+math.ceil((screen_width-drive_width)/2)
