import pygame
import random
import map
import sys

# Define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
player_width = 50
player_height = 100
STEERING_SPEED=14
SPEED=2

pygame.init()

# Set up the map
images_1 = []
for tile in map.map_1_tiles:
    images_1.append(pygame.image.load(tile))

# images_2 = []
# for tile in map_2_tiles:
#     images_2.append(pygame.image.load(tile))

# Create your sprite groups
all_sprites_1 = pygame.sprite.Group()
# all_sprites_2 = pygame.sprite.Group()

# Iterate over each element of the matrix and create a sprite for each element
for row in range(len(map.map_1)):
    for col in range(len(map.map_1[row])):
        tile = map.Tile(col, row, images_1[map.map_1[row][col]-1],map.tile_width,map.tile_height)
        all_sprites_1.add(tile)


# Set up the player
player_x =SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10

# Set up the road
road_width =SCREEN_WIDTH // 4
road_height = SCREEN_HEIGHT * 2
road_x =SCREEN_WIDTH // 2 - road_width // 2
road_y = -road_height + player_y + player_height + 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LiDAR race")

# Set up the clock
clock = pygame.time.Clock()

# Set up the lanes
# lanes = []
# for i in range(4):
#     lane_x = i * road_width + road_x
#     lane_y = road_y + road_height // 4 * i
#     lane_width = road_width
#     lane_height = road_height // 4
#     lanes.append(pygame.Rect(lane_x, lane_y, lane_width, lane_height))

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    # Move the player left or right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:# and player_x > lanes[0].x:
        player_x -= STEERING_SPEED
    if keys[pygame.K_RIGHT]:# and player_x < lanes[-1].x + lanes[-1].width - player_width:
        player_x += STEERING_SPEED
    
    #display text
    font = pygame.font.Font(None, 24)
    text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (0, 0, 0))
    textpos_fps = text_fps.get_rect(centery=70, centerx=70)

    # Move the road down
    road_y += SPEED
    # print('road y='+str(road_y))
    # If the road goes off screen, reset it to the top of the screen and randomize the obstacles
    if road_y > SCREEN_HEIGHT:
        road_y = -road_height + player_y + player_height + 10
    
    #update y of the road map
    all_sprites_1.update(SPEED)
    
    # Draw everything on the screen
    screen.fill((255, 255, 255))
    # # Draw each sprite on the screen
    all_sprites_1.draw(screen)

    # for lane in lanes:
    #     pygame.draw.rect(screen, (0, 0, 0), lane)
    # drawing the player car
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    
    # text display
    screen.blit(text_fps, textpos_fps)

    # update road position
    # all_sprites_1.update()
    
    # Update the screen
    pygame.display.flip()
    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(60)

pygame.quit()