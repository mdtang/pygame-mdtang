import pygame
import time
import random
from pygame.locals import *
pygame.init()

screen_width = 1280
screen_height = 720

gameDisplay = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('DOOOOOOOOOOOOOOOM!!!!')

clock = pygame.time.Clock()

bg = pygame.image.load('dungeon.bmp')
# Scaling background image
bg = pygame.transform.scale(bg,(screen_width,screen_height))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 250
        self.height = 150
        
        self.image = pygame.image.load('gun.bmp')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

        self.rect = self.image.get_rect()

        # centerx and bottom from pygame.Rect documentation
        self.rect.centerx = screen_width * .5
        self.rect.bottom = screen_height - 10

        # initializing horizontal speed
        self.speedX = 0


    def update(self):
        self.speedX = 0

        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.speedX = -20
        elif keys[K_d]:
            self.speedX = 20
        self.rect.x += self.speedX
        
        # creating walls so player will not leave edges of screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        # bullet starts at center of x and top of player
        bullet = BulletSprite(self.rect.centerx, self.rect.top)

        # adding bullet sprite to all sprites group
        allsprites.add(bullet)

        bullets.add(bullet)
                

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.enemywidth = 150
        self.enemyheight = 135

        self.image = pygame.image.load('monster.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.enemywidth,self.enemyheight))
        
        self.rect = self.image.get_rect()

        # declare variables for random positions for enemy sprites
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedY = random.randrange(1,10)

    def update(self):
        self.rect.y += self.speedY
        if self.rect.top > screen_height + 10:
            # Spawning enemies from different x coordinates so they don't come from the same place
            self.rect.x = random.randrange(screen_width - self.rect.width)
            # Spawning enemies off screen at random y coordinates
            self.rect.y = random.randrange(-200, -80)
            # varying speeds for enemy sprites
            self.speedY = random.randrange(5,10)


class BulletSprite(pygame.sprite.Sprite):
    # x and y are for bullet coordinates
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.enemywidth = 25
        self.enemyheight = 90

        self.image = pygame.image.load('bullet.bmp')
        self.image = pygame.transform.scale(self.image, (self.enemywidth,self.enemyheight))

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y

        self.speedY = -15
    
    def update(self):
        self.rect.y += self.speedY

        # if bullet gets past top of screen
        if self.rect.bottom < 0:
            # removes bullet sprite
            self.kill()

# sprite groups created
allsprites = pygame.sprite.Group()
enemymobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = PlayerSprite()
allsprites.add(player)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.QUIT:
            gameExit = True
    
    # updating sprites
    allsprites.update()

    # check for player-enemy sprite collision (creates list)
    hits = pygame.sprite.spritecollide(player,enemymobs, False)
    if hits:
        #myFont = pygame.font.Font(None, 100)
        #label = myFont.render("GAME OVER", 1, (255,255,0))
        #gameDisplay.blit(label, (220, 250))
        # ends game
        gameExit = True

    # check for enemy-bullet sprite collision
    bullethits = pygame.sprite.groupcollide(enemymobs,bullets, True, True)
    for hits in bullethits:
        # spawn new enemy mob
        mob = EnemySprite()
        allsprites.add(mob)
        enemymobs.add(mob)



    # rendering
    gameDisplay.blit(bg,(0,0))
    allsprites.draw(gameDisplay)
    pygame.display.flip()

#required
pygame.quit()
quit()				#exits python


