#The MIT License (MIT)

#Copyright (c) 2012 Robin Duda, (chilimannen)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#Camera module will keep track of sprite offset.

#TODO:
#place trees
#obstacles: EU pallette, cone (with blooming!)
#randomize obstacle images
#move camera when steering
#changing lighting throughout the day
#start menu - Update and fix
#option to restart game without re-launching

#sprite editor: https://www.piskelapp.com/

import pygame
import map, obstacles
import random
import common

pygame.init()

#Rotate car.
# def rot_center(image, rect, angle):
#         """rotate an image while keeping its center"""
#         rot_image = pygame.transform.rotate(image, angle)
#         rot_rect = rot_image.get_rect(center=rect.center)
#         return rot_image,rot_rect

# Define screen size
GODMODE=False
FPS=100
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 400
DRIVE_WIDTH=600
# TILE_WIDTH=400
TILE_HEIGHT=400
PLAYER_WIDTH = 36
PLAYER_HEIGHT = 88
BLOCK_WIDTH=36
BLOCK_HEIGHT=88
STEERING_SPEED=6
VEHICLES_SPEED=3
ROAD_SPEED=5
LATERAL_CHANCE=0 #DISABLED BY DEFAULT = 0, Chance of lateral movement of vehicles
NUM_OBSTACLES=5
CAMALPHA=255
#player angle 
player_angle = 0
player_angle_change = 0

#init player
player  = pygame.sprite.Group()
player_image = pygame.image.load(r'media/ego_vehicle.png')
player.image=player_image
player.rect = player.image.get_rect()
player.rect.x=SCREEN_WIDTH/2
player.rect.y=SCREEN_HEIGHT - PLAYER_HEIGHT - 10
#init menus
start_menu  = pygame.sprite.Group()
start_menu_image = pygame.image.load(r'media/menu.png')
start_menu.image = start_menu_image
start_menu.rect = player.image.get_rect()
start_menu.rect.x=SCREEN_WIDTH/2-start_menu_image.get_width()/2
start_menu.rect.y=SCREEN_HEIGHT/2-start_menu_image.get_height()/2

# Load and play music
pygame.mixer.music.load(r'media/raceGame1.mp3')
# create an obstacle to cover grass
grassLeft_obstacle_rect = pygame.Rect(0, 0, 300, SCREEN_HEIGHT)
grassRight_obstacle_rect = pygame.Rect(900, 0, 300, SCREEN_HEIGHT)

# Create your sprite groups
map_tiles_cam = pygame.sprite.Group()
map_tiles_lidar = pygame.sprite.Group()

#add all tiles to a map list called map_tiles_cam
for row in range(len(map.map_plan)):
    currentWidth=0
    for col in range(len(map.map_plan[row])):
        tile_1 = map.Tile(currentWidth, row, map.map_cam_tiles[map.map_plan[row][col]-1],SCREEN_HEIGHT) #xStart=currentWidth
        tile_2 = map.Tile(currentWidth, row, map.map_lidar_tiles[map.map_plan[row][col]-1],SCREEN_HEIGHT) #xStart=currentWidth
        currentWidth += tile_1.image.get_width()
        map_tiles_cam.add(tile_1)
        map_tiles_lidar.add(tile_2)
        #add trees
        if col==0:
            tree1=map.Tile(100,row,map.tree_images[0],SCREEN_HEIGHT)
            map_tiles_cam.add(tree1)
            tree1=map.Tile(100,row,map.tree_images[0],SCREEN_HEIGHT)
            map_tiles_cam.add(tree1)
# init a block obstacle
block_list = pygame.sprite.Group()

#create 5 obstacles
for i in range(NUM_OBSTACLES):
    # This represents a block
    speedDelta=random.uniform(0.7, 1.2) #random vehicle speed delta
    block = obstacles.Obstacle(speedDelta)
    # Set a random location for the block
    # block.rect.x = random.randrange(DRIVE_WIDTH-BLOCK_WIDTH)+math.ceil((SCREEN_WIDTH-DRIVE_WIDTH)/2)
    block.rect.x = random.randrange(0,4)*150+375-BLOCK_WIDTH/2+random.randint(-25,25)
    block.rect.y = random.randrange(TILE_HEIGHT)-TILE_HEIGHT
    # Add the block to the list of objects
    block_list.add(block)

# Set up the player
player_x =SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30

# Set up the road
road_width =SCREEN_WIDTH // 4
road_height = SCREEN_HEIGHT * 2
road_x =SCREEN_WIDTH // 2 - road_width // 2
road_y = -road_height + player_y + PLAYER_HEIGHT + 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LiDAR race")

# Load and play music
pygame.mixer.music.load(r'media/raceGame1.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

# Set up the clock
clock = pygame.time.Clock()
# player.image = pygame.transform.rotate(player.image, 45)
# player.image, player.rect = rot_center(player.image, player.rect, 45)
# player.rect = player.image.get_rect()
# Main loop
running = True
moving = False
frameCount=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                player_angle_change = 0.2
            elif event.key == pygame.K_RIGHT:
                player_angle_change = -0.2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player_angle_change > 0:
                player_angle_change = 0
            elif event.key == pygame.K_RIGHT and player_angle_change < 0:
                player_angle_change = 0
    # Get key press
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP]) and moving == False:# and player_x < lanes[-1].x + lanes[-1].width - PLAYER_WIDTH:
        moving = True
        pygame.mixer.music.unpause()
        # player.rect.x = player_x
    # Handle events
    # Draw white fill on the screen
    screen.fill((0, 0, 0))
    # Draw map tile list
    # map_tiles_cam.draw(screen)
    map_tiles_cam.draw(screen)
    # draw the player car
    screen.blit(player.image, (player.rect.x, player.rect.y))
    # text display
    font = pygame.font.Font(None, 24)
    text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (0, 0, 0))
    textpos_fps = text_fps.get_rect(centery=70, centerx=70)
    screen.blit(text_fps, textpos_fps)


    block_list.draw(screen)
    
    if moving == False:
        # draw menu
        screen.blit(start_menu.image, (start_menu.rect.x, start_menu.rect.y))
    # update the display
    pygame.display.update()

    if moving:        
        player_angle += player_angle_change
        # player.image = pygame.transform.rotate(player.image, player_angle)

        #update y of the road map
        map_tiles_cam.update(ROAD_SPEED,SCREEN_HEIGHT,len(map.map_plan),TILE_HEIGHT,CAMALPHA) #Alpha 0-255
        map_tiles_lidar.update(ROAD_SPEED,SCREEN_HEIGHT,len(map.map_plan),TILE_HEIGHT,255) #255=no darkening

        # map_tiles_lidar.update(ROAD_SPEED,SCREEN_WIDTH,SCREEN_HEIGHT,len(map.map_plan),TILE_HEIGHT)
        block_list.update(VEHICLES_SPEED,LATERAL_CHANCE,SCREEN_HEIGHT,TILE_HEIGHT,len(map.map_plan),BLOCK_HEIGHT,BLOCK_WIDTH,DRIVE_WIDTH)
        # steer the player car with left and right arrows
        if keys[pygame.K_LEFT]:# and player_x > lanes[0].x:
            player.rect.x -= STEERING_SPEED
            # player.rect.x = player_x
        if keys[pygame.K_RIGHT]:# and player_x < lanes[-1].x + lanes[-1].width - PLAYER_WIDTH:
            player.rect.x += STEERING_SPEED
        if GODMODE==False:
            if pygame.sprite.spritecollide(player, block_list, False, pygame.sprite.collide_rect):
                common.gameOver(screen)
                running = False
        #check collision with right and left grass
        if grassLeft_obstacle_rect.collidepoint(player.rect.x, player.rect.y) or grassRight_obstacle_rect.collidepoint(player.rect.x+player.rect.width-5, player.rect.y): #-5 to tune to grass collision
            common.gameOver(screen)
            running = False
    
    screen.blit(text_fps, textpos_fps)
    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)
    # print("player angle = "+str(player_angle))
    # print("player angle change = "+str(player_angle_change))
    frameCount+=1
pygame.quit()