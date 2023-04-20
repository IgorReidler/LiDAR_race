import pygame
import math

# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image,tile_width,tile_height,screen_width,screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height + (screen_height-3*tile_height)
    def update(self,road_speed, screen_width, screen_height,tilesNum_height,tile_height):        
        self.rect.y+=road_speed
        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            self.rect.y = screen_height - tile_height*tilesNum_height+math.ceil(road_speed)

# Define some constants
tile_width = 400
tile_height = 400
# Define your maps
map_1 = [
        [1,2,3],
        [1,2,3],
        [1,2,3],
        [1,2,3],
]

map_2 = map_1

# Load your images
map_1_tiles = [r'media/grass_left_marked.png', r'media/lane.png', r'media/grass_right.png']
map_2_tiles = [r'media/grass_left_lidar.png', r'media/lane.png', r'media/grass_right.png']