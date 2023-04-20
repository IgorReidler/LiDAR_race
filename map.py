import pygame
# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image,tile_width,tile_height,screen_width,screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height + (screen_height-3*tile_height)
        print("tile init y = "+str(self.rect.y))
    def update(self,road_speed, screen_width, screen_height):        
        # If the road goes off screen, reset it to the top of the screen and randomize the obstacles
        # print(self.rect.y)
        if self.rect.y > screen_height:
            self.rect.y = screen_height - tile_height*4
            print("moved tile to y="+str(self.rect.y))
        self.rect.y+=road_speed
            # self.rect.y -= tile_height*
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