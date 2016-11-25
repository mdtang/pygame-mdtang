import pygame
import time
import random
from pygame.locals import *

pygame.mixer.init()
pygame.init()

white = (255, 255, 255)
screen_width = 1280
screen_height = 720

gameDisplay = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('DOOOOOOOOOOOOOOOM!!!!')

clock = pygame.time.Clock()

# loading and resizing background image
bg = pygame.image.load('dungeon.bmp')
bg = pygame.transform.scale(bg,(screen_width,screen_height))

def display_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = x, y
    surface.blit(text_surface, text_rect)

def display_lives(surface, x, y, lives, image):
    for i in range(lives):
        image_rect = image.get_rect()
        # 50 is for the space between each sprite
        image_rect.x = x + 50 * i
        image_rect.y = y
        surface.blit(image, image_rect)

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 160
        self.height = 160
        
        self.image = pygame.image.load('gun.bmp')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

        # smaller image of player for player count icon use
        self.smallimage = pygame.transform.scale(self.image, (40,40))

        self.rect = self.image.get_rect()

        # drawing circle for improved collision
        # radius is half of diameter/width
        self.radius = 80

        #pygame.draw.circle (self.image, white, self.rect.center, self.radius)

        # placing playersprite - centerx and bottom from pygame.Rect documentation
        self.rect.centerx = screen_width * .5
        self.rect.bottom = screen_height - 10

        # initializing horizontal speed
        self.speedX = 0
        
        # no delay when holding shoot button
        self.shootdelay = 0
        self.lastshot = pygame.time.get_ticks()

        self.lives = 3

        self.hidden = False
        self.hidetimer = pygame.time.get_ticks()

    def update(self):
        self.speedX = 0
        # hides player for 2 seconds 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            # restore player to original location
            self.rect.centerx = screen_width * .5
            self.rect.bottom = screen_height - 10
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.speedX = -20
        if keys[K_RIGHT]:
            self.speedX = 20
        if keys[K_SPACE]:
            self.shoot()
        self.rect.x += self.speedX
        
        # creating walls so player will not leave edges of screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.lastshot) > self.shootdelay:
            self.lastshot = now
            # bullet starts at center of x and top of player
            bullet = BulletSprite(self.rect.centerx, self.rect.top)

            # adding bullet sprite to all sprites group
            allsprites.add(bullet)

            bullets.add(bullet)

            #adding gun sound only when prompted
            gun_sound.play()
    
    def hide(self):
        # temporarily hide player when hit
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        # hide player below screen
        self.rect.center = (screen_width * 0.5, screen_height + 300)

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.enemywidth = 120
        self.enemyheight = 100
        
        # randomly choose enemy images
        self.image = random.choice(enemyimages)

        self.image = pygame.transform.scale(self.image, (self.enemywidth,self.enemyheight))
        
        self.rect = self.image.get_rect()
        
        self.radius = int(self.rect.width * .35)
        # pygame.draw.circle(self.image, white, self.rect.center, self.radius)

        # declare variables for random positions for enemy sprites
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        self.speedX = random.randrange(-2,2)
        self.speedY = random.randrange(5,10)

    def update(self):
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        if self.rect.top > screen_height + 10:
            # Spawning enemies from different x coordinates so they don't come from the same place
            self.rect.x = random.randrange(screen_width - self.rect.width)
            # Spawning enemies off screen at random y coordinates
            self.rect.y = random.randrange(-200, -80)
            # varying speeds for enemy sprites
            self.speedX = random.randrange(-2,2)
            self.speedY = random.randrange(5,10)


class BulletSprite(pygame.sprite.Sprite):
    # x and y are for bullet coordinates
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.bulletwidth = 20
        self.bulletheight = 80

        self.image = pygame.image.load('bullet.bmp')
        self.image = pygame.transform.scale(self.image, (self.bulletwidth,self.bulletheight))

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

class ExplosionSprites(pygame.sprite.Sprite):
    def __init__(self, center, version):
        pygame.sprite.Sprite.__init__(self)
        self.version = version
        self.image = expl_anim[self.version][0]

        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.frame = 0
        self.lastupdate = pygame.time.get_ticks()
        self.framerate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastupdate > self.framerate:
            self.lastupdate = now
            # counting frames
            self.frame += 1
            if self.frame == len(expl_anim[self.version]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.version][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# loading multiple enemy images
enemyimages = []
enemylist = ['monster1.gif', 'monster2.gif', 'monster3.gif', 'monster4.gif']

for image in enemylist:
    enemyimages.append(pygame.image.load(image).convert_alpha())

# loading explosion animation images with a dictionary
expl_anim = {}
expl_anim['enemy'] = []
expl_anim['player'] = []

for i in range(15):
    filename = '{}.bmp'.format(i)
    image = pygame.image.load(filename)
    image.set_colorkey(white)
    image = pygame.transform.scale(image, (100,100))
    expl_anim['enemy'].append(image)

for i in range(14):
    filename = 'player{}.bmp'.format(i)
    image = pygame.image.load(filename)
    image.set_colorkey(white)
    image = pygame.transform.scale(image, (200, 200))
    expl_anim['player'].append(image)

gun_sound = pygame.mixer.Sound("gunsound.wav")

# loading different monster death sounds
monster_sounds = []
soundslist = ['enemysound1.wav','enemysound2.wav','enemysound3.wav']
for sound in soundslist:
    monster_sounds.append(pygame.mixer.Sound(sound))

# loading continuous background music
pygame.mixer.music.load('bgmusic.wav')

# creating sprite groups
allsprites = pygame.sprite.Group()
enemymobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = PlayerSprite()
allsprites.add(player)

# creating list of random number of enemies from 8 to 20 and shuffling for randomness
enemycount = list(range(8, 20))
random.shuffle(enemycount)

for i in enemycount:
    mob = EnemySprite()
    # updating enemy sprites into allsprites
    allsprites.add(mob)
    # adding enemy sprites into sprites group
    enemymobs.add(mob)


clock.tick(60) # 60 fps cap

# initialize score
score = 0 

# infinite looping background music
pygame.mixer.music.play(loops= -1)

gameExit = False
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    
    # updating sprites
    allsprites.update()

    # check for player-enemy (circle sprites) sprite collision (creates list)
    hits = pygame.sprite.spritecollide(player,enemymobs, False, pygame.sprite.collide_circle)
    if hits:
        # spawn player death explosion
        player_expl = ExplosionSprites(player.rect.center, 'player')
        allsprites.add(player_expl)
        player.hide()
        player.lives -= 1

    # check for enemy-bullet sprite collision
    bullethits = pygame.sprite.groupcollide(enemymobs,bullets, True, True)
    for hits in bullethits:
        # +100 score per kill
        score += 100

        # randomly choose and play enemy sounds
        random.choice(monster_sounds).play()
        
        # spawn enemy explosions
        expl = ExplosionSprites(hits.rect.center, 'enemy')
        allsprites.add(expl)

        # spawn new enemy mob
        mob = EnemySprite()
        allsprites.add(mob)
        enemymobs.add(mob)

    if player.lives == 0 and not player_expl.alive():
        gameExit = True


    # rendering
    gameDisplay.blit(bg,(0,0))
    allsprites.draw(gameDisplay)
    # drawing number of lives on top left of screen
    display_lives(gameDisplay, 10, 5, player.lives, player.smallimage)
    # text is score
    display_text(gameDisplay, str(score), 30, screen_width * .5, 10)

    # displaying
    pygame.display.flip()

#required
pygame.quit()
quit()				#exits python


