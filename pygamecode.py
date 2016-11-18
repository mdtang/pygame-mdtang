import pygame
import sys
import random
from pygame.locals import *
pygame.init()

screen_width = 1280
screen_height = 720

gameDisplay = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Adventure!')

clock = pygame.time.Clock()

bg = pygame.image.load('dungeon.bmp')
# Scaling background image
bg = pygame.transform.scale(bg,(1280,720))

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.enemyx = 540
        self.enemyy = 0

        self.enemywidth = 200
        self.enemyheight = 180

        self.enemy = pygame.image.load('monster.gif').convert_alpha()
        self.enemy = pygame.transform.scale(self.enemy, (self.enemywidth,self.enemyheight))
        
        self.rect = self.enemy.get_rect()
        # x and y coordinates, respectively
        self.enemyspeed = [0,random.randint(1,6)]

    def renderEnemy(self):
        gameDisplay.blit(self.enemy, (self.enemyx,self.enemyy), self.rect)

    def move(self):
        # Moving enemy
        self.rect.move_ip(self.enemyspeed)
        if self.rect[1] > 1280 or self.rect[1] < 0:
            self.enemyspeed[1] = -self.enemyspeed[1]


class GunSprite (pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.width = 300
        self.height = 180

        # Making sure gun sprite starts in the middle bottom of screen
        self.x = 480
        self.y = screen_height - self.height
        
        self.char = pygame.image.load('gun.bmp')
        self.char = pygame.transform.scale(self.char, (self.width,self.height))

        self.speed = 10

    def renderSprite(self):
        gameDisplay.blit(self.char, (self.x,self.y))

    def update(self):
        keys = pygame.key.get_pressed()

        #if keys[K_w]:
            #self.y -= self.speed
            #if self.y > 600:
                #self.y = 600
        #elif keys[K_s]:
            #self.y += self.speed
            #if self.y < 0:
                #self.y = 0
        if keys[K_a]:
            self.x -= self.speed
            if self.x < 220:
                self.x = 220
        elif keys[K_d]:
            self.x += self.speed
            if self.x > 800:
                self.x = 800


def main():

    enemy_list = pygame.sprite.Group()

    for i in range(10):
        enemy = EnemySprite(500, 250)

        enemy.rect.x = random.randrange(screen_width)
        enemy.rect.y = random.randrange(screen_height)

        enemy_list.add(enemy)

    player = GunSprite(0,250)

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
