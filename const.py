# #define constants
GODMODE=False #no collisions with obstacles, for testing
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
#speed related
FPS=60
SPEED_FACTOR=1
# NUM_OBSTACLES=int(5*50/FPS*SPEED_FACTOR)
STEERING_SPEED=int(10*50/FPS)
ROAD_SPEED=int(10*50/FPS*SPEED_FACTOR)
CAR_SPEED_DELTA_FROM=int(-1.5*50/FPS*SPEED_FACTOR)
CAR_SPEED_DELTA_TO=int(-2*50/FPS*SPEED_FACTOR)
# obstacles
carsImagePathList=[r'media/car1.png', r'media/car2.png',r'media/car3_80.png']
carsImagePathList_lidar=[r'media/car1_lidar.png', r'media/car2.png',r'media/car3_85.png']
stationaryObstaclesImagePathList=[r'media/cone1_small.png',r'media/tire1_55.png']
stationaryObstaclesImagePathList_lidar=[r'media/cone1_small.png',r'media/tire1_55.png']
NUM_OBSTACLES_CARS=5 #number of cars on the road in each vertical tile row
NUM_OBSTACLES_STATIONARY=2 #number of stationary obstacles (cones, EU palettes) in each vertical row
# sound paths
soundUpPath='media/powerUp1.mp3'
soundDownPath='media/powerDown2.mp3'
musicPath='media/raceGame1.mp3'
LIDARMASKPATH=r'media/arcMask1.png'