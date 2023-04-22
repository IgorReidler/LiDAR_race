import pygame
import math
import random

# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, xStart, y, image,screen_height):
        super().__init__()
        self.image = image
        tile_width=self.image.get_width()
        tile_height=self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = xStart#x * tile_width
        self.rect.y = y * tile_height + (screen_height-3*tile_height)
    def update(self,road_speed, screen_height,tilesNum_height,tile_height):        
        self.rect.y+=road_speed
        # If the road tile goes off screen, reset it to the top of all road tile sprites
        if self.rect.y > screen_height:
            self.rect.y = screen_height - tile_height*tilesNum_height+6#math.ceil(road_speed/2)
            

# Define some constants
# tile_width = 400
# tile_height = 400
# Define your maps
map_1 = [
        [1,2,2,2,3,4],
        [1,2,2,2,3,4],
        [1,2,2,2,3,4],
        [1,2,2,2,3,4],
]

map_2 = map_1

# Load your images
map_1_tiles = [r'media/grass_left.png', r'media/lane_marks.png', r'media/lane_empty.png',r'media/grass_right.png']
map_2_tiles = [r'media/grass_left.png', r'media/lane_marks.png', r'media/lane_empty.png',r'media/grass_right.png']
