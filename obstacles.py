import pygame
import random

# init obstacle
def loadObstacles(NUM_OBSTACLES,obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,VEHICLE_SPEED_DELTA_FROM,VEHICLE_SPEED_DELTA_TO,TILE_HEIGHT,BLOCK_WIDTH):
    obstacles_list = pygame.sprite.Group()
    for i in range(NUM_OBSTACLES): #vehicles
        # This represents a block
        speedDelta=random.uniform(VEHICLE_SPEED_DELTA_FROM,VEHICLE_SPEED_DELTA_TO) #random vehicle speed delta
        block = Obstacle(obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,speedDelta)
        # Set a random location for the block
        block.rect.x = random.randrange(0,4)*150+375-BLOCK_WIDTH/2+random.randint(-25,25)
        block.rect.y = random.randrange(TILE_HEIGHT)-TILE_HEIGHT
        # Add the block to the list of objects
        obstacles_list.add(block)
    return obstacles_list

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacleSpeed,obstacleImagePathList,obstacleImagePathList_lidar,speedDelta=0):
        super().__init__()
        # speed delta init
        self.obstacleSpeed=obstacleSpeed
        self.speedDelta = speedDelta
        self.obstacleImagePathList = obstacleImagePathList
        self.obstacleImagePathList_lidar = obstacleImagePathList_lidar
        self.vehicleTypeNum=random.randint(0,len(self.obstacleImagePathList)-1)
        self.image = pygame.image.load(self.obstacleImagePathList[self.vehicleTypeNum])
        self.rect = self.image.get_rect()
        self.lateralDir=random.randint(0, 1) * 2 - 1
        self.prevImageLidar=False
    def update(self, lateral_chance,screen_height,tile_height,tilesNum_height,obstacle_height,obstacle_width,drive_width,lidarFlag):        
        #if loaded images are non-lidar and flag is lidar, load lidar obstacles
        if lidarFlag==True and self.prevImageLidar==False:
            self.image = pygame.image.load(self.obstacleImagePathList_lidar[self.vehicleTypeNum])
            self.prevImageLidar=True
        #if loaded images are lidar and flag is non-lidar, load non-lidar obstacles
        elif lidarFlag==False and self.prevImageLidar==True:
            self.image = pygame.image.load(self.obstacleImagePathList[self.vehicleTypeNum])
            self.prevImageLidar=False
        self.rect.y+=self.obstacleSpeed+self.speedDelta
        if random.randrange(0,10)>(1-lateral_chance)*10:
            self.rect.x+=1*self.lateralDir

        # If the road tile goes off screen, reset it to the top of all road tile sprites
        # print(self.rect.y)
        if self.rect.y > screen_height:
            self.rect.x = random.randrange(0,4)*150+375-obstacle_width/2 + random.randint(-25,25)
            self.rect.y = random.randrange(tile_height) - tile_height - obstacle_height
            # self.rect.x = random.randrange(drive_width-obstacle_width)+math.ceil((screen_width-drive_width)/2)