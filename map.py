import pygame
# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image,tile_width,tile_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height
    def update(self,road_speed):
        self.rect.y+=road_speed

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
map_1_tiles = [r'media/grass_left.png', r'media/lane.png', r'media/grass_right.png']
map_2_tiles = [r'media/grass_left_lidar.png', r'media/lane.png', r'media/grass_right.png']