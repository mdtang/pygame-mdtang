import pygame
import sys
from pygame.locals import *
pygame.init()

#create colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkblue = (71, 76, 149)

gameDisplay = pygame.display.set_mode((800,600))

bg = pygame.image.load('bg.bmp')
# Scaling background image
bg = pygame.transform.scale(bg, (1400,600))

pygame.display.set_caption('Adventure!')

clock = pygame.time.Clock()

class Sprite:
    def __init__(self,x,y):
        self.x = 0
        self.y = 250

        self.width = 150
        self.height = 120

        self.char = pygame.image.load('char.bmp')
        self.smaller_char = pygame.transform.scale(self.char, (self.width,self.height))
        
        self.speed = 10

    def renderSprite(self):
        gameDisplay.blit(self.smaller_char, (self.x,self.y))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            self.y -= self.speed
            if self.y < 200:
                self.y = 200
        elif keys[K_s]:
            self.y += self.speed
            if self.y > 300:
                self.y = 300
        elif keys[K_a]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif keys[K_d]:
            self.x += self.speed
            if self.x > 800:
                self.x = 800

player = Sprite(0,250)

spritesheet = pygame.image.load("spritesheet.bmp")
num_images = 10
current_imgs = 0

gameExit = False
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    gameDisplay.blit(bg, (0,0))
    
    player.renderSprite()
    player.update()

    clock.tick(60) # 60 fps cap

    pygame.display.flip()

#required
pygame.quit()
quit()				#exits python
