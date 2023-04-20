import pygame

class Player(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        player  = pygame.sprite.Group()
        player_image = pygame.image.load(r'media/ego_vehicle.png')
        player.image=player_image

 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
    def update(self,road_speed, screen_width, screen_height,tile_height,tilesNum_height):        
        self.rect.y+=road_speed
        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            self.rect.y = screen_height - tile_height*tilesNum_height+2