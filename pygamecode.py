import pygame
import sys
import random
from pygame.locals import *
pygame.init()

screen_width = 1280
screen_height = 720

gameDisplay = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('DOOOOOOOOM!!!!')

clock = pygame.time.Clock()

bg = pygame.image.load('dungeon.bmp')
# Scaling background image
bg = pygame.transform.scale(bg,(1280,720))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 300
        self.height = 180
        
        self.image = pygame.image.load('gun.bmp')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width * .5
        self.rect.bottom = screen_height - 10
        # initializing horizontal speed
        self.speedx = 0

    def renderSprite(self):
        gameDisplay.blit(self.char, (self.x,self.y))

    def update(self):
        self.speedx = 0

        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.speedx = -20
        elif keys[K_d]:
            self.speedx = 20
        self.rect.x += self.speedx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
                

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.enemywidth = 200
        self.enemyheight = 180

        self.image = pygame.image.load('monster.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.enemywidth,self.enemyheight))
        
        self.rect = self.image.get_rect()

        # random positions for enemy sprites
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,10)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            # Spawning enemies from different x coordinates so they don't come from the same place
            self.rect.x = random.randrange(screen_width - self.rect.width)
            # Spawning enemies off screen at random y coordinates
            self.rect.y = random.randrange(-200, -80)
            # varying speeds for enemy sprites
            self.speedy = random.randrange(5,10)


def main():
    allsprites = pygame.sprite.Group()
    player = PlayerSprite()
    allsprites.add(player)
  
    enemymobs = pygame.sprite.Group()
    
    # creating list of random numbers from 3 to 8 and shuffling for randomness
    enemycount = list(range(3,8))
    random.shuffle(enemycount)

    for i in enemycount:
        mob = EnemySprite()
        # updating enemy sprites into allsprites
        allsprites.add(mob)
        # adding enemy sprites into sprites group
        enemymobs.add(mob)

    #spritesheet = pygame.image.load("spritesheet.bmp")
    #num_images = 10
    #current_imgs = 0

    clock.tick(60) # 60 fps cap

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        
        # updating sprites
        allsprites.update()

        # rendering
        gameDisplay.blit(bg,(0,0))
        allsprites.draw(gameDisplay)
        #if pygame.sprite.collide_rect():
            #myFont = pygame.font.Font(None, 100)
            #label = myFont.render("GAME OVER", 1, (255,255,0))
            #screen.blit(label, (220, 250))
        pygame.display.flip()

    #required
    pygame.quit()
    quit()				#exits python

main()
