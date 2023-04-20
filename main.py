#TODO:
#infinite map scroll
#objects
#lanes for the objects to move in
#collision mechanism

import pygame
import map

pygame.init()

# Define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
player_width = 36
player_height = 88
STEERING_SPEED=11
SPEED=2
#init player
player  = pygame.sprite.Group()
player_image = pygame.image.load(r'media/ego_vehicle.png')
player.image=player_image

# Set up the map
images_1 = []
for tile in map.map_1_tiles:
    images_1.append(pygame.image.load(tile))
images_2 = []
for tile in map.map_2_tiles:
    images_2.append(pygame.image.load(tile))

# Create your sprite groups
all_sprites_1 = pygame.sprite.Group()
all_sprites_2 = pygame.sprite.Group()

# Iterate over each element of the matrix and create a sprite for each element
for row in range(len(map.map_1)):
    for col in range(len(map.map_1[row])):
        tile_1 = map.Tile(col, row, images_1[map.map_1[row][col]-1],map.tile_width,map.tile_height,SCREEN_WIDTH,SCREEN_HEIGHT)
        all_sprites_1.add(tile_1)
        tile_2 = map.Tile(col, row, images_2[map.map_2[row][col]-1],map.tile_width,map.tile_height,SCREEN_WIDTH,SCREEN_HEIGHT)
        all_sprites_2.add(tile_2)

# Set up the player
player_x =SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 30

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
        
    # Draw white fill on the screen
    screen.fill((255, 255, 255))
    # Draw map tile list
    all_sprites_2.draw(screen)
    # draw the player car
    screen.blit(player.image, (player_x, player_y))
    # text display
    font = pygame.font.Font(None, 24)
    text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (0, 0, 0))
    textpos_fps = text_fps.get_rect(centery=70, centerx=70)
    screen.blit(text_fps, textpos_fps)

    #update y of the road map
    all_sprites_1.update(SPEED,SCREEN_WIDTH,SCREEN_HEIGHT)
    all_sprites_2.update(SPEED,SCREEN_WIDTH,SCREEN_HEIGHT)

    # Update the screen
    # pygame.display.flip() #probably not needed
    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(60)

pygame.quit()


# If the image goes off the screen, reset its position
    # if y > image.get_height():
    #     y = 0 - screen.get_height()