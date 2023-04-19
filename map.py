import pygame
# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image,width,height,screen_width,screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * width
        self.rect.y = y * height

class Map():
    def __init__(self, screen_width,screen_height):
        # Define some constants
        width = 400
        height = 400
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
        map_2_tiles = [r'media/grass_left.png', r'media/lane.png', r'media/grass_right.png']

        images_1 = []
        for tile in map_1_tiles:
            images_1.append(pygame.image.load(tile))

        images_2 = []
        for tile in map_2_tiles:
            images_2.append(pygame.image.load(tile))

        # Create your sprite groups
        self.all_sprites_1 = pygame.sprite.Group()
        self.all_sprites_2 = pygame.sprite.Group()

        # Iterate over each element of the matrix and create a sprite for each element
        for row in range(len(map_1)):
            for col in range(len(map_1[row])):
                tile = Tile(col, row, images_1[map_1[row][col]-1],width,height,screen_width,screen_height)
                self.all_sprites_1.add(tile)

        for row in range(len(map_2)):
            for col in range(len(map_2[row])):
                tile = Tile(col + len(map_2[0]), row, images_2[map_2[row][col]-1],width,height,screen_width,screen_height)
                self.all_sprites_2.add(tile)