import pygame
import math
import random

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
    def update(self,road_speed, screen_width, screen_height,tile_height,tilesNum_height,obstacle_height,obstacle_width,drive_width):        
        self.rect.y+=road_speed
        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            # self.rect.y = screen_height - tile_height*tilesNum_height+math.ceil(road_speed)
            self.rect.y = random.randrange(tile_height) - tile_height - obstacle_height
            self.rect.x = random.randrange(drive_width-obstacle_width)+math.ceil((screen_width-drive_width)/2)
            # block.rect.x = random.randrange(DRIVE_WIDTH-BLOCK_WIDTH)+math.ceil((SCREEN_WIDTH-DRIVE_WIDTH)/2)
