# how to break apart a sprite sheet into seperate images and put them in an image list
# snake parts image is 320 x 256 pixels with 5 images across and 4 down
# so therefore each image is 64 x 64 pixels
import pygame
pygame.init()
win = pygame.display.set_mode((1053,587))

# this code loads the image into a surface called spriteSheet and outputs its size (just to be sure)
spriteSheet = pygame.image.load('SPRITE.gif')
print(spriteSheet.get_size())

# this code displays the full sprite sheet
win.fill((255,255,255))
win.blit(spriteSheet,(0,0))
pygame.display.update()
pygame.time.delay(2000)

# this code creates a list of snake images from the sprite sheet and puts them in a list
# I have chosen to take the images a row at a time (ie working across the sprite sheet
# but you could do it a column at a time (ie working down the sprite sheet) just as easily
snakeParts = []
for y in range(0,587,118):
    for x in range(0,1053,81):
        snakeParts.append(spriteSheet.subsurface((x,y,81,118)))

### this code sets up some constants for the indices of the various parts of the snake
### CTL => Corner top left, HUP = > Head Facing Up, TD => Tail Facing Down, A => Apple, BH => Body horizontal etc.
CTL,CTR,CBL,CBR,HU,HD,HR,HL,TU,TD,TL,TR,A,BH,BV = 0,2,5,12,3,9,4,8,13,19,18,14,15,1,7
##
### this code draws one of the body parts.  Try changing it up to draw a different part!!
win.fill((200,200,200))
win.blit(snakeParts[A],(0,0))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
