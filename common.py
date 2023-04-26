import pygame
import time

def gameOver(screen):
    # Draw "Game over" text
    font1 = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 24)
    text1 = font1.render('Game Over!', True, (255, 0, 0))
    text2 = font2.render('You have received a formal escalation letter', True, (255, 0, 0))
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (600, 200)
    textRect2.center = (600, 250)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    # Update the display
    pygame.display.flip()
    #stop the music
    pygame.mixer.music.stop()
    # Load and play sound
    gameOverSound = pygame.mixer.Sound('media/game-over-38511.mp3')
    gameOverSound.play()
    time.sleep(4)

def speedChange(speed_delta,fps,speed_factor, vehicle_speed, road_speed, vehicle_speed_delta_from, vehicle_speed_delta_to,soundUpPath,soundDownPath):
    speed_factor=speed_factor+speed_delta
    vehicle_speed=int(5*50/fps*speed_factor)
    road_speed=int(7*50/fps*speed_factor)
    vehicle_speed_delta_from=int(-0.7*50/fps*speed_factor)
    vehicle_speed_delta_to=int(-1.5*50/fps*speed_factor)
    if speed_delta>0:
        speedChangeSound = pygame.mixer.Sound(soundUpPath) #if speed increases, play up sound effect
    else:
        speedChangeSound = pygame.mixer.Sound(soundDownPath)  #if speed decreases, play down sound effect
    speedChangeSound.play()

    return speed_factor, vehicle_speed, road_speed, vehicle_speed_delta_from, vehicle_speed_delta_to

    speed_factpr, vehicle_speed, road_speed, vehicle_speed_delta_from, vehicle_speed_delta_to=changeSpeed(SPEED_FACTOR,0.5,FPS)
    speedIncreaseSound = pygame.mixer.Sound('media/powerUp1.mp3')
    speedIncreaseSound.play()
