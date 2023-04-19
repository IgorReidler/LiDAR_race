import pygame
import random
import map
import sys

# Define screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
player_width = 50
player_height = 100
steering_speed = 10

# init map
myMap = map.Map(SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.init()

# Set up the player
player_x =SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10

# Set up the road
road_width =SCREEN_WIDTH // 4
road_height = SCREEN_HEIGHT * 2
road_x =SCREEN_WIDTH // 2 - road_width // 2
road_y = -road_height + player_y + player_height + 10
road_speed = steering_speed


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
        player_x -= steering_speed
    if keys[pygame.K_RIGHT]:# and player_x < lanes[-1].x + lanes[-1].width - player_width:
        player_x += steering_speed
    
    #display text
    font = pygame.font.Font(None, 24)
    text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (0, 0, 0))
    textpos_fps = text_fps.get_rect(centery=70, centerx=70)

    # Move the road down
    road_y += road_speed
    print('road y='+str(road_y))
    # If the road goes off screen, reset it to the top of the screen and randomize the obstacles
    if road_y > SCREEN_HEIGHT:
        road_y = -road_height + player_y + player_height + 10

    # Draw everything on the screen
    screen.fill((255, 255, 255))
    # # Draw each sprite on the screen
    # myMap.all_sprites_1.draw(screen)
    # all_sprites_2.draw(screen)


    # for lane in lanes:
    #     pygame.draw.rect(screen, (0, 0, 0), lane)
    # drawing the player car
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    
    # text display
    screen.blit(text_fps, textpos_fps)

    # update road position
    # myMap.all_sprites_1.update(road_x, road_y)
    myMap.all_sprites_1.rect.y = road_y
    myMap.all_sprites_1.draw(screen)
    
    # Update the screen
    pygame.display.flip()
    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(60)

pygame.quit()