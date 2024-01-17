import pygame
import time
import os
from datetime import datetime
import const

def gameOver(screen,obstaclesPassed):
    # Draw "Game over" text
    # font1 = pygame.font.Font('freesansbold.ttf', 48)
    # font2 = pygame.font.Font('freesansbold.ttf', 32)
    # text1 = font1.render('Game Over', True, (255, 0, 0))
    # text2 = font2.render('You passed '+str(obstaclesPassed)+' true positives!', True, (255, 0, 0))
    # textRect1 = text1.get_rect()
    # textRect2 = text2.get_rect()
    # textRect1.center = (600, 200)
    # textRect2.center = (600, 250)
    # screen.blit(text1, textRect1)
    # screen.blit(text2, textRect2)
    # Update the display
    pygame.display.flip()
    #stop the music
    pygame.mixer.music.stop()
    # Load and play sound
    gameOverSound = pygame.mixer.Sound('media/game-over-38511.mp3')
    gameOverSound.play()
    # time.sleep(1)

def write_high_score(playerName, highScore): #This function was entirely written by bing (GPT v4.0 on 27 Apr 2023)
    if not os.path.exists('highscore.txt'):
        open('highscore.txt', 'w').close()
    with open('highscore.txt', 'r') as f:
        lines = f.readlines()
        scores = {}
        for line in lines:
            name, score, date = line.strip().split(',')
            scores[name] = (int(score), date)
        if playerName in scores and highScore <= scores[playerName][0]:
            return
        scores[playerName] = (highScore, datetime.now().strftime('%H:%M %d/%m/%Y'))
    with open('highscore.txt', 'w') as f:
        for name, score_date in scores.items():
            f.write(f'{name},{score_date[0]},{score_date[1]}\n')

def speedChange(speed_delta,fps,speed_factor, road_speed, vehicle_speed_delta_from, vehicle_speed_delta_to,soundUpPath,soundDownPath):
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

    return speed_factor, road_speed, vehicle_speed_delta_from, vehicle_speed_delta_to

def drawText(screen,text,position):
    if position not in ['center', 'side']: #validating position input
        raise ValueError("Position must be either 'center' or 'side'")
    if position == 'center':
        positionArgument=(screen.get_width()/2, screen.get_height()/2)
    if position == 'side':
        positionArgument=(screen.get_width()/4, screen.get_height()/4)
    font = pygame.font.Font(None, 72)  # Create a Font object with the default font and a size of 72
    text_surface = font.render(text, True, (255, 255, 255))  # Create a white Surface with the text
    text_rect = text_surface.get_rect(center=positionArgument)  # Get the rectangle of the text surface and set its center to the center of the screen
    screen.blit(text_surface, text_rect)  # Draw the text Surface onto the screen at the calculated position
def collide(self):
        write_high_score(self.playerName,self.score)
        gameOver(self.screen,self.score)
        self.moving = False
        self.gameOver = True
        self.gameOverMenu()
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
            drawText(self.screen,self.mainMessage,'center')
            self.mainMessageFrameCounter+=1
        elif self.mainMessage != None:
            self.mainMessageFrameCounter=0
            self.mainMessage=None
        pygame.display.update()
        clock.tick(const.FPS)