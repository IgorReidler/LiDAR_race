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
    # Load and play sound
    gameOverSound = pygame.mixer.Sound('media/game-over-38511.mp3')
    gameOverSound.play()
    time.sleep(3)