import pygame

# Define some constants
WIDTH = 400
HEIGHT = 400
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

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

# Define your sprites
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * WIDTH
        self.rect.y = y * HEIGHT

# Create your sprite groups
all_sprites_1 = pygame.sprite.Group()
all_sprites_2 = pygame.sprite.Group()

# Iterate over each element of the matrix and create a sprite for each element
for row in range(len(map_1)):
    for col in range(len(map_1[row])):
        tile = Tile(col, row, images_1[map_1[row][col]-1])
        all_sprites_1.add(tile)

for row in range(len(map_2)):
    for col in range(len(map_2[row])):
        tile = Tile(col + len(map_2[0]), row, images_2[map_2[row][col]-1])
        all_sprites_2.add(tile)

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("My Game")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw each sprite on the screen
    all_sprites_1.draw(screen)
    # all_sprites_2.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame when we're done
pygame.quit()