#TODO: make sure all obstacle properties are properties of the class, for example obstacle_width is externally passed to update function
import pygame
import random

# init obstacle
def loadObstacles(NUM_OBSTACLES,obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,car_SPEED_DELTA_FROM,car_SPEED_DELTA_TO,TILE_HEIGHT,BLOCK_WIDTH,car_lateral_chance):
    obstacles_list = pygame.sprite.Group()
    for i in range(NUM_OBSTACLES): #cars
        # This represents a block
        speedDelta=random.uniform(car_SPEED_DELTA_FROM,car_SPEED_DELTA_TO) #random car speed delta
        block = Obstacle(obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,speedDelta,car_lateral_chance)
        # Set a random location for the block
        block.rect.y = random.randrange(TILE_HEIGHT*2)-TILE_HEIGHT*2 #spawn height of obstacles
        if car_SPEED_DELTA_TO==0: #stationary obstacles, like cones
            block.rect.x = 300+random.randrange(0,4)*150-BLOCK_WIDTH/2 #place between lanes
        else: #moving obstacles, like cars
            block.rect.x = random.randrange(0,4)*150+375-BLOCK_WIDTH/2+random.randint(- 25,25) #place at center of lanes

        # Add the block to the list of objects
        obstacles_list.add(block)
    return obstacles_list

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,speedDelta=0,car_lateral_chance=0):
        super().__init__()
        # speed delta init
        self.car_lateral_chance=car_lateral_chance
        self.obstacleSpeed=obstacleSpeed
        self.speedDelta = speedDelta
        self.obstacleImagePathList = obstacleImagePathList
        self.obstacleImagePathList_lidar = obstacleImagePathList_lidar
        self.carTypeNum=random.randint(0,len(self.obstacleImagePathList)-1)
        self.image = pygame.image.load(self.obstacleImagePathList[self.carTypeNum])
        self.rect = self.image.get_rect()
        self.lateralDir=random.randint(0, 1) * 2 - 1
        self.prevImageLidar=False
        self.timesPassed=0
    def update(self,screen_height,tile_height,obstacle_height,obstacle_width,lidarFlag, road_speed):        
        #if loaded images are non-lidar and flag is lidar, load lidar obstacles
        self.road_speed=road_speed
        self.obstacleSpeed=road_speed
        if lidarFlag==True and self.prevImageLidar==False:
            self.image = pygame.image.load(self.obstacleImagePathList_lidar[self.carTypeNum])
            self.prevImageLidar=True
        #if loaded images are lidar and flag is non-lidar, load non-lidar obstacles
        elif lidarFlag==False and self.prevImageLidar==True:
            self.image = pygame.image.load(self.obstacleImagePathList[self.carTypeNum])
            self.prevImageLidar=False
        self.rect.y+=self.obstacleSpeed+self.speedDelta #main vertical move
        if random.randrange(0,10)>(1-self.car_lateral_chance)*10:
            self.rect.x+=1*self.lateralDir
        # If the obstacle goes below bottom of the screen, reset it to the top
        if self.rect.y > screen_height:
            self.rect.y = random.randrange(tile_height) - tile_height - obstacle_height
            if self.speedDelta==0: #stationary obstacles, like cones
                self.rect.x = 300+random.randrange(0,4)*150-obstacle_width/2 #place between lanes
            else: #moving obstacles, like cars
                self.rect.x = random.randrange(0,4)*150+375-obstacle_width/2+random.randint(- 25,25) #place at center of lanes
            # return 1 #mark obstacle was passed by the player
            return 1
        else:
            return 0
        # else:
        #     return 0