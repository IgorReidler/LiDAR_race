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

#TODO:
#map_plan is randomized only once per game, in map.py. Randomize every draw.
#add obstacles: EU pallette

import pygame
import map, obstacles, common
from pygame.locals import *
import const
from sys import exit
from time import sleep
import os
os.environ['PNG_IGNORE_WARNINGS'] = '1' # to suppress warnings about PNG files

class Game:
    def __init__(self):
        print("Lets go!")
        self.playerName='Player1'
        self.running = True
        self.moving = False
        self.highScore=0
        # Create your sprite groups
        self.map_tiles_cam = pygame.sprite.Group()
        self.map_tiles_lidar = pygame.sprite.Group()
        self.map_tiles=self.map_tiles_cam
        #add all tiles to a map list called map_tiles_cam
        for row in range(len(map.map_plan)):
            currentWidth=0
            for col in range(len(map.map_plan[row])):
                tile_1 = map.Tile(currentWidth, row, map.map_cam_tiles[map.map_plan[row][col]-1],const.SCREEN_HEIGHT) #xStart=currentWidth
                tile_2 = map.Tile(currentWidth, row, map.map_lidar_tiles[map.map_plan[row][col]-1],const.SCREEN_HEIGHT) #xStart=currentWidth
                currentWidth += tile_1.image.get_width()
                self.map_tiles_cam.add(tile_1)
                self.map_tiles_lidar.add(tile_2)
        self.lidar=False
        self.gameOver=False
        self.score=0 #number of obstacles passed (used for score calculation)
        self.fadeAlpha=0 # used to calculate fadeAlphaMax 
        self.player_angle = 0
        self.player_angle_change = 0
        self.lidarMask = pygame.image.load(const.LIDARMASKPATH)
        self.lidarMask600 = pygame.transform.scale(self.lidarMask, (900,600))
        self.lidarMask600_rect=(150,0)
        # fade to black surface
        self.fadeFillSurface = pygame.Surface((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))  # , pygame.SRCALPHA)
        self.fadeFillSurface.fill((0, 0, 0, 0))

        #init player
        self.player  = pygame.sprite.Group()
        self.player_image = pygame.image.load(r'media/ego_vehicle.png')
        self.player.image = self.player_image
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = const.SCREEN_WIDTH/2
        self.player.rect.y = const.SCREEN_HEIGHT - const.PLAYER_HEIGHT - 10
        #init menus
        self.start_menu  = pygame.sprite.Group()
        self.start_menu_image = pygame.image.load(r'media/menu.png')
        self.start_menu.image = self.start_menu_image
        self.start_menu.rect = self.player.image.get_rect()
        self.start_menu.rect.x=const.SCREEN_WIDTH/2-self.start_menu_image.get_width()/2
        self.start_menu.rect.y=const.SCREEN_HEIGHT/2-self.start_menu_image.get_height()/2

        self.gameOver_menu  = pygame.sprite.Group()
        self.gameOver_menu_image = pygame.image.load(r'media/gameOver_menu.png')
        self.gameOver_menu.image = self.gameOver_menu_image
        self.gameOver_menu.rect = self.player.image.get_rect()
        self.gameOver_menu.rect.x=const.SCREEN_WIDTH/2-self.start_menu_image.get_width()/2
        self.gameOver_menu.rect.y=const.SCREEN_HEIGHT/2-self.start_menu_image.get_height()/2
    
        # create an obstacle to cover grass
        self.grassLeft_obstacle_rect = pygame.Rect(0, 0, 300, const.SCREEN_HEIGHT)
        self.grassRight_obstacle_rect = pygame.Rect(900, 0, 300, const.SCREEN_HEIGHT)

        self.all_obstacles_list=pygame.sprite.Group()
        # Create car obstacles list
        self.cars_list=obstacles.loadObstacles(const.NUM_OBSTACLES_CARS,const.ROAD_SPEED, const.carsImagePathList,const.carsImagePathList_lidar,const.CAR_SPEED_DELTA_FROM,const.CAR_SPEED_DELTA_TO,const.TILE_HEIGHT,const.BLOCK_WIDTH,const.CAR_LATERAL_CHANCE)
        # Create static obstacles list (cones, EU pallete etc..)
        self.static_obstacles_list=obstacles.loadObstacles(const.NUM_OBSTACLES_STATIONARY,const.ROAD_SPEED,const.stationaryObstaclesImagePathList,const.stationaryObstaclesImagePathList_lidar,0,0,const.TILE_HEIGHT,const.BLOCK_WIDTH,0)
        # add all lists to all obstacles list
        self.all_obstacles_list.add(self.cars_list, self.static_obstacles_list)

        # Set up the player
        self.player_x =const.SCREEN_WIDTH // 2 - const.PLAYER_WIDTH // 2
        self.player_y = const.SCREEN_HEIGHT - const.PLAYER_HEIGHT - 30

        # Set up the road
        self.road_width = const.SCREEN_WIDTH // 4
        self.road_height = const.SCREEN_HEIGHT * 2
        self.road_x = const.SCREEN_WIDTH // 2 - self.road_width // 2
        self.road_y = -self.road_height + self.player_y + const.PLAYER_HEIGHT + 10
        # Load and play music
        pygame.mixer.music.load(const.musicPath)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
        self.lidar=False
    def prepareScreen(self):
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("LiDAR race")

        # Set up the clock
        self.map_tiles=self.map_tiles_cam
        #after key event
        self.map_tiles.draw(self.screen)
        # draw the player car
        self.screen.blit(self.player.image,
                    (self.player.rect.x, self.player.rect.y))
        # mask by arc
        self.all_obstacles_list.draw(self.screen)
        if self.lidar:  # if lidar, mask with pie from an image
            self.screen.blit(self.lidarMask600, (self.player.rect.centerx-const.ARCWIDTH/2,
                        self.lidarMask600_rect[1]), special_flags=pygame.BLEND_RGBA_MIN)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
                self.player.rect.centerx-const.ARCWIDTH/2-600, 0, 600, 600))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
                self.player.rect.centerx+const.ARCWIDTH/2, 0, 600, 600))
    
    def run(self):
        #unpause music
        pygame.mixer.music.unpause()
        # Set up the clock
        clock = pygame.time.Clock()
        frameCount=0
        # map_tiles=self.map_tiles_cam

        # main loop
        while self.running:
            # read keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE and self.lidar == False:
                        self.lidar = True
                        self.map_tiles = self.map_tiles_lidar  # change map tiles to lidar
                        break
                    if event.key == pygame.K_SPACE and self.lidar == True:
                        self.lidar = False
                        self.map_tiles = self.map_tiles_cam  # change map tiles to camera
                        break
                    if event.key == pygame.K_LEFT:
                        self.player_angle = 20
                    elif event.key == pygame.K_RIGHT:
                        self.player_angle = -20
                    if event.key == pygame.K_UP and self.moving:  # increase speed
                        const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO = common.speedChange(
                            const.SPEED_STEP, const.FPS, const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO, const.soundUpPath, const.soundDownPath)
                        break
                    if event.key == pygame.K_DOWN and self.moving:  # decrease speed
                        if const.SPEED_FACTOR-const.SPEED_STEP>0:
                            const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO = common.speedChange(
                                -const.SPEED_STEP, const.FPS, const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO, const.soundUpPath, const.soundDownPath)
                            break
            keys = pygame.key.get_pressed()
                # steer the player car with left and right arrows
            if keys[pygame.K_LEFT]:  # and player_x > lanes[0].x:
                self.player.rect.x -= const.STEERING_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += const.STEERING_SPEED
            self.map_tiles.draw(self.screen)
            # draw the player car
            self.screen.blit(self.player.image,(self.player.rect.x, self.player.rect.y))
            # mask by arc
            self.all_obstacles_list.draw(self.screen)
            if self.lidar:  # if lidar, mask with pie from an image
                self.screen.blit(self.lidarMask600, (self.player.rect.centerx-const.ARCWIDTH/2,
                            self.lidarMask600_rect[1]), special_flags=pygame.BLEND_RGBA_MIN)
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
                    self.player.rect.centerx-const.ARCWIDTH/2-600, 0, 600, 600))
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
                    self.player.rect.centerx+const.ARCWIDTH/2, 0, 600, 600))

            frameCount += 1  # for darkening
            fadeAlpha = min(255, int(frameCount/const.darkeningFactor))  # calc alpha for darkening
            self.fadeFillSurface.set_alpha(
                fadeAlpha)  # set alpha for darkening

            # update y of the road map
            self.map_tiles_cam.update(const.ROAD_SPEED, const.SCREEN_HEIGHT, len(
                map.map_plan), const.TILE_HEIGHT)  # Alpha 0-255
            self.map_tiles_lidar.update(const.ROAD_SPEED, const.SCREEN_HEIGHT, len(
                map.map_plan), const.TILE_HEIGHT)  # 255=no darkening
            for obstacle in self.all_obstacles_list:
                wasPassed = obstacle.update(const.SCREEN_HEIGHT, len(
                    map.map_plan), const.BLOCK_HEIGHT, const.BLOCK_WIDTH, self.lidar, const.ROAD_SPEED)
                self.score += wasPassed
            
            if const.GODMODE == False:
                if pygame.sprite.spritecollide(self.player, self.all_obstacles_list, False, pygame.sprite.collide_rect) or self.grassLeft_obstacle_rect.collidepoint(self.player.rect.x, self.player.rect.y) or self.grassRight_obstacle_rect.collidepoint(self.player.rect.x+self.player.rect.width-5, self.player.rect.y):
                    self.collide()
                collisions = pygame.sprite.groupcollide(
                    self.all_obstacles_list, self.all_obstacles_list, False, False)
                if const.obstaclesCollideKillFlag:
                    for obstacle in collisions:
                        if len(collisions[obstacle]) > 1:
                            obstacle.kill()
                            self.all_obstacles_list.add(obstacles.loadObstacles(1, const.ROAD_SPEED, const.carsImagePathList, const.carsImagePathList_lidar,
                                                const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO, const.TILE_HEIGHT, const.BLOCK_WIDTH, const.CAR_LATERAL_CHANCE))

            # Update the display and tick the clock
            if self.lidar == False and self.moving == 1:
                self.screen.blit(self.fadeFillSurface, (0, 0))
            self.showText(clock)
        pygame.quit() #quit the game
        exit() #sys.exit game
    def collide(self):
        common.write_high_score(self.playerName,self.score)
        common.gameOver(self.screen,self.score)
        self.moving = False
        self.gameOver = True
        self.pauseMenu()
    def showText(self,clock):
            # text display
            font = pygame.font.Font(None, 30)
            text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (255, 0, 0))
            text_alpha = font.render('ALPHA: ' + str(int(self.fadeAlpha)), 1, (0, 0, 255))
            text_speedFactor = font.render('NEED4SPEED', 1, (255, 255, 255))

            text_score = font.render('SCORE: ' + str(self.score), 1, (255, 255, 255))
            self.screen.blit(text_fps, (70, 70))
            self.screen.blit(text_alpha, (70, 100))
            self.screen.blit(text_speedFactor, (70, 130))
            self.screen.blit(text_score, (70, 160))
            pygame.display.update()
            clock.tick(const.FPS)
    
    def startMenu(self):
        self.prepareScreen()
        self.screen.blit(self.start_menu.image,(self.start_menu.rect.x, self.start_menu.rect.y))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_r:
                        self.moving = True
                        self.run()
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit() #quit the game
                        exit() #sys.exit game
            pygame.display.update()
            sleep(0.2)
    
    def pauseMenu(self):
        while True:
            for event in pygame.event.get():
                # if event.type == pygame.QUIT:
                #     self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.gameOver == True:
                        # self.running = False
                        initGame()
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit() #quit the game
                        exit() #sys.exit game
            self.screen.blit(self.gameOver_menu.image,
                                (self.gameOver_menu.rect.x, self.gameOver_menu.rect.y))
            pygame.display.update()
            sleep(0.5)
        
        
def initGame():
    pygame.init()
    myGame=Game()
    myGame.startMenu()

if __name__ == '__main__':
    initGame()