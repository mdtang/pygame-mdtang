import pygame
pygame.init()

#create colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkblue = (71, 76, 149)

#position vars
x_pos = 0
y_pos = 0

gameDisplay = pygame.display.set_mode((800,600))

pygame.display.set_caption('Adventure!')

gameExit = False
while not gameExit:
    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		    gameExit = True


    gameDisplay.fill(darkblue)
    pygame.draw.rect(gameDisplay, white, [300,300, 10, 100])	
    pygame.draw.rect(gameDisplay, white, [500,300, 10, 100])
    pygame.draw.rect(gameDisplay, white, [300,100, 10, 100])
    pygame.draw.rect(gameDisplay, white, [500,100, 10, 100])
    pygame.draw.rect(gameDisplay, white, [300,500, 10, 100])
    pygame.draw.rect(gameDisplay, white, [500,500, 10, 100])
    pygame.draw.rect(gameDisplay, white, [400,500, 5, 100])
    pygame.draw.rect(gameDisplay, white, [400,200, 5, 100])
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:	
            gameDisplay.fill(darkblue)
            pygame.draw.rect(gameDisplay, white, [300,200, 10, 100])	
            pygame.draw.rect(gameDisplay, white, [500,200, 10, 100])
            pygame.draw.rect(gameDisplay, white, [300,0, 10, 100])
            pygame.draw.rect(gameDisplay, white, [500,0, 10, 100])
            pygame.draw.rect(gameDisplay, white, [300,400, 10, 100])
            pygame.draw.rect(gameDisplay, white, [500,400, 10, 100])
            pygame.draw.rect(gameDisplay, white, [400,300, 5, 100])
            pygame.draw.rect(gameDisplay, white, [400,100, 5, 100])

    if event.type == pygame.KEYDOWN:
	    if event.key == pygame.K_LEFT:
		    x_pos -= 10
	    if event.key == pygame.K_RIGHT:
		    x_pos += 10
	    if event.key == pygame.K_UP:
		    y_pos -= 10
	    if event.key == pygame.K_DOWN:
		    y_pos += 10

    gameDisplay.fill(white, rect=[x_pos,y_pos, 20,20])
    pygame.display.update()	

#required
pygame.quit()
quit()				#exits python
