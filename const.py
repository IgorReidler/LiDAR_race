# #define constants
SCREEN_WIDTH = 1200 #1920
SCREEN_HEIGHT = 600 #1080
DRIVE_WIDTH=600
TILE_HEIGHT=400
PLAYER_WIDTH = 36
PLAYER_HEIGHT = 88
BLOCK_WIDTH=36
BLOCK_HEIGHT=88
CAR_LATERAL_CHANCE=0.2 #DISABLED BY DEFAULT = 0, Chance of lateral movement of cars
ARCWIDTH=900

#flags
GODMODE=False #no collisions with obstacles, for testing
PROFILEMODE=False #
obstaclesCollideKillFlag=False
#speed related
FPS=70
SPEED_FACTOR=1
# NUM_OBSTACLES=int(5*50/FPS*SPEED_FACTOR)
STEERING_SPEED=int(10*50/FPS)
ROAD_SPEED=int(10*50/FPS*SPEED_FACTOR)
CAR_SPEED_DELTA_FROM=int(-1.5*50/FPS*SPEED_FACTOR)
CAR_SPEED_DELTA_TO=int(-2*50/FPS*SPEED_FACTOR)
SPEED_STEP=0.2
darkeningFactor=4
# obstacles
carsImagePathList=[r'media/car1.png', r'media/car2.png',r'media/car3_80.png']
carsImagePathList_lidar=[r'media/car1_lidar.png', r'media/car2_lidar.png',r'media/car3_80_lidar.png']
# stationaryObstaclesImagePathList=[r'media/cone1_small.png',r'media/tire1_55.png']
stationaryObstaclesImagePathList=[r'media/cone1_small.png',r'media/tire1_55.png']
stationaryObstaclesImagePathList_lidar=[r'media/cone1_small.png',r'media/tire1_55.png']
NUM_OBSTACLES_CARS=3 #number of cars on the road in each vertical tile row
NUM_OBSTACLES_STATIONARY=2 #number of stationary obstacles (cones, EU palettes) in each vertical row
# sound paths
soundUpPath='media/powerUp1.mp3'
soundDownPath='media/powerDown2.mp3'
musicPath='media/raceGame1.mp3'
LIDARMASKPATH_itwo=r'media/arcMask_stretched.png'
LIDARMASKPATH_ione=r'media/arcMask_iONE.png'#r'media/arcMask_stretched.png'
LIDARMASKPATH_competitor=r'media/arcMask_competitor_gray.png'#r'media/arcMask_stretched.png'
MIN_FADE_ALPHA=180
MAINMESSAGETIME=70 #main message display time in frames