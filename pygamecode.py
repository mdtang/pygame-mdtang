import pygame
import sys
import random
from pygame.locals import *
pygame.init()

gameDisplay = pygame.display.set_mode((800,600))

pygame.display.set_caption('Adventure!')

clock = pygame.time.Clock()

bg = pygame.image.load('grass.bmp')
# Scaling background image
bg = pygame.transform.scale(bg,(1800,600))

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.enemyx = 500
        self.enemyy = 250

        self.enemywidth = 300
        self.enemyheight = 180

        self.enemy = pygame.image.load('enemy.bmp')
        self.enemy = pygame.transform.scale(self.enemy, (self.enemywidth,self.enemyheight))
        
        self.enemypos = self.enemy.get_rect()
        # x and y coordinates, respectively
        self.enemyspeed = [random.randint(1,6),random.randint(1,6)]

    def renderEnemy(self):
        gameDisplay.blit(self.enemy, (self.enemyx,self.enemyy), self.enemypos)

    def move(self):
        # Moving enemy
        self.enemypos.move_ip(self.enemyspeed)
        if self.enemypos[0] > 800 or self.enemypos[0] < 0:
            self.enemyspeed[0] = -self.enemyspeed[0]


class Sprite (pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = 0
        self.y = 250

        self.width = 150
        self.height = 120
        
        self.char = pygame.image.load('char.bmp')
        self.char = pygame.transform.scale(self.char, (self.width,self.height))

        self.speed = 10

    def renderSprite(self):
        gameDisplay.blit(self.char, (self.x,self.y))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            self.y -= self.speed
            if self.y > 600:
                self.y = 600
        elif keys[K_s]:
            self.y += self.speed
            if self.y < 0:
                self.y = 0
        elif keys[K_a]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif keys[K_d]:
            self.x += self.speed
            if self.x > 730:
                self.x = 730


def main():
    player = Sprite(0,250)
    enemy = EnemySprite(500, 250)

    spritesheet = pygame.image.load("spritesheet.bmp")
    num_images = 10
    current_imgs = 0

    clock.tick(60) # 60 fps cap

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        gameDisplay.blit(bg,(0,0))
        enemy.renderEnemy()
        player.renderSprite()
         
        player.update()
        enemy.move()
        #if pygame.sprite.collide_rect():
            #myFont = pygame.font.Font(None, 100)
            #label = myFont.render("GAME OVER", 1, (255,255,0))
            #screen.blit(label, (220, 250))
        pygame.display.flip()

    #required
    pygame.quit()
    quit()				#exits python

main()
