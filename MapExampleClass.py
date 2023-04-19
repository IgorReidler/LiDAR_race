import pygame
import map

# Define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

myMap = map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)
# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("LiDAR race")

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
    # screen.fill((255, 255, 255))

    # Draw each sprite on the screen
    myMap.all_sprites_1.draw(screen)
    # all_sprites_2.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame when we're done
pygame.quit()