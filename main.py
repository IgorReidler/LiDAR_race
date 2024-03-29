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
#Add driving assistance = auto break
#Add autonomous driving - avoiding obstacles
#Car steering speed according to speed
#Purchase menu
#darkening after restart
# [backlog]
# Car turns at an angle - very hard to calculate collisions

#map_plan is randomized only once per game, in map.py. Randomize every draw.
#add obstacles: EU pallette

import pygame
import map, obstacles, common
from pygame.locals import *
import const
from sys import exit
from time import sleep
import os
if const.PROFILEMODE:
    import cProfile
    import pstats
    import io


os.environ['PNG_IGNORE_WARNINGS'] = '1' # to suppress warnings about PNG files

class Game:
    def __init__(self):
        print("Lets go!")
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        if const.PROFILEMODE:
            self.pr = cProfile.Profile()
        
        self.prev_player_x = None
        self.playerName='Player1'
        self.running = True
        self.moving = False
        
        self.highScore=0
        self.mainMessage=None
        self.mainMessageFrameCounter=0
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
        self.lidarMask = pygame.image.load(const.LIDARMASKPATH_ione).convert()
        self.lidarMask600 = pygame.transform.scale(self.lidarMask, (900,600))
        self.lidarMask600_rect=(150,0)
        # fade to black surface
        self.fadeFillSurface = pygame.Surface((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))  # , pygame.SRCALPHA)
        self.fadeFillSurface.fill((0, 0, 0, 0))

        #init player
        self.player  = pygame.sprite.Group()
        self.player_image = pygame.image.load(r'media/ego_vehicle.png').convert()
        self.player.image = self.player_image
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x = const.SCREEN_WIDTH/2
        self.player.rect.y = const.SCREEN_HEIGHT - const.PLAYER_HEIGHT - 10
        #init menus
        self.start_menu  = pygame.sprite.Group()
        self.start_menu_image = pygame.image.load(r'media/menu.png').convert()
        self.start_menu.image = self.start_menu_image
        self.start_menu.rect = self.player.image.get_rect()
        self.start_menu.rect.x=const.SCREEN_WIDTH/2-self.start_menu_image.get_width()/2
        self.start_menu.rect.y=const.SCREEN_HEIGHT/2-self.start_menu_image.get_height()/2

        self.gameOver_menu  = pygame.sprite.Group()
        self.gameOver_menu_image = pygame.image.load(r'media/gameOver_menu.png').convert()
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
        # screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("LiDAR race")

        # Set up the clock
        self.map_tiles=self.map_tiles_cam
        #after key event
        self.map_tiles.draw(self.screen)
        # draw the player car
        # If the x-coordinate has changed, draw the player car
        # self.screen.blit(self.player.image,
                        # (self.player.rect.x, self.player.rect.y))
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                    self.running = False
                    if const.PROFILEMODE:
                        self.pr.disable()
                        s = io.StringIO()
                        ps = pstats.Stats(self.pr, stream=s).sort_stats('time')
                        ps.print_stats()
                        print(s.getvalue())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.lidar = not self.lidar
                        self.map_tiles = self.map_tiles_lidar if self.lidar else self.map_tiles_cam
                    elif event.key in (pygame.K_UP, pygame.K_DOWN) and self.moving:
                        speed_step = const.SPEED_STEP if event.key == pygame.K_UP else -const.SPEED_STEP
                        if const.SPEED_FACTOR - speed_step > 0 or event.key == pygame.K_UP:
                            const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO = common.speedChange(
                                speed_step, const.FPS, const.SPEED_FACTOR, const.ROAD_SPEED, const.CAR_SPEED_DELTA_FROM, const.CAR_SPEED_DELTA_TO, const.soundUpPath, const.soundDownPath)
                    elif event.key == pygame.K_p:
                        self.moving = not self.moving
                        self.pauseMenu()
                        if self.moving:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif (event.key == pygame.K_1) & (self.lidar==True):
                        self.lidarMask = pygame.image.load(const.LIDARMASKPATH_ione).convert()
                        self.lidarMask600 = pygame.transform.scale(self.lidarMask, (900,600))
                        #write on screen
                        self.mainMessage='Innoviz iOne'
                    elif (event.key == pygame.K_2) & (self.lidar==True):
                        self.lidarMask = pygame.image.load(const.LIDARMASKPATH_itwo).convert()
                        self.lidarMask600 = pygame.transform.scale(self.lidarMask, (900,600))
                        self.mainMessage='Innoviz iTwo'
                    elif (event.key == pygame.K_3) & (self.lidar==True):
                        self.lidarMask = pygame.image.load(const.LIDARMASKPATH_competitor).convert()
                        self.lidarMask600 = pygame.transform.scale(self.lidarMask, (900,600))
                        self.mainMessage='Competitor LiDAR'



            keys = pygame.key.get_pressed()
                # steer the player car with left and right arrows
            if keys[pygame.K_LEFT]:  # and player_x > lanes[0].x:
                self.player.rect.x -= const.STEERING_SPEED
                # turn the car by 30deg
                self.player_angle_change = 30
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += const.STEERING_SPEED
                self.player_angle_change = 30
                # turn the car by 30deg
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
                # self.mainMessage='LiDAR Enabled'

            frameCount += 1  # for darkening
            # if fadeAlpha > 100:
            fadeAlpha = min(const.MIN_FADE_ALPHA, int(frameCount/const.darkeningFactor))  # calc alpha for darkening
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
                    common.collide(self)
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
            # Update the previous x-coordinate for the next frame
            self.prev_player_x = self.player.rect.x
        pygame.quit() #quit the game
        exit() #sys.exit game
    # def collide(self):
    #     common.write_high_score(self.playerName,self.score)
    #     common.gameOver(self.screen,self.score)
    #     self.moving = False
    #     self.gameOver = True
    #     self.gameOverMenu()
    def showText(self,clock):
            # text display
            font = pygame.font.Font(None, 30)
            text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (255, 0, 0))
            text_alpha = font.render('ALPHA: ' + str(int(self.fadeAlpha)), 1, (0, 0, 255))
            # text_speedFactor = font.render('NEED4SPEED', 1, (255, 255, 255))

            text_score = font.render('SCORE: ' + str(self.score), 1, (255, 255, 255))
            self.screen.blit(text_fps, (70, 70))
            # self.screen.blit(text_alpha, (70, 100))
            # self.screen.blit(text_speedFactor, (70, 130))
            self.screen.blit(text_score, (70, 100))
            # if mainMessage is not equal to none, display it
            if (self.mainMessage != None) & (self.mainMessageFrameCounter<const.MAINMESSAGETIME): #changing mainMessage from None to any text draws it here
                common.drawText(self.screen,self.mainMessage,'center')
                self.mainMessageFrameCounter+=1
            elif self.mainMessage != None:
                self.mainMessageFrameCounter=0
                self.mainMessage=None
            pygame.display.update()
            clock.tick(const.FPS)
    
    def startMenu(self):
        self.prepareScreen()
        self.screen.blit(self.start_menu.image,(self.start_menu.rect.x, self.start_menu.rect.y))
        while True:
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_r:
                        self.moving = True
                        if const.PROFILEMODE:
                            self.pr.enable()  # Start the profiler
                        self.run()  # The method you want to profile
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit() #quit the game
                        exit() #sys.exit game                        
            pygame.display.update()
            sleep(0.2)
    
    def pauseMenu(self):
        self.prepareScreen()
        self.screen.blit(self.start_menu.image,(self.start_menu.rect.x, self.start_menu.rect.y))
        while True:
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.type == pygame.KEYDOWN:
                    if event.key == event.key == pygame.K_r:
                        self.moving = True
                        if const.PROFILEMODE:
                            self.pr.enable()  # Start the profiler
                        self.run()  # The method you want to profile
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit() #quit the game
                        exit() #sys.exit game
            pygame.display.update()
            sleep(0.2)
    
    def gameOverMenu(self):
        self.prepareScreen()
        self.screen.blit(self.gameOver_menu.image,(self.start_menu.rect.x, self.start_menu.rect.y))
        while True:
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        self.__init__()  # Re-initialize the game
                        self.run()  # Start the game
                    # if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_r:
                    #     self.moving = True
                    #     if const.PROFILEMODE:
                    #         self.pr.enable()  # Start the profiler
                    #     self.run()  # The method you want to profile
                    import const
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit() #quit the game
                        exit() #sys.exit game
            pygame.display.update()
            sleep(0.2)

        
def initGame():
    pygame.init()
    myGame=Game()
    myGame.startMenu()

if __name__ == '__main__':
    initGame()