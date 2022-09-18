# how to break apart a sprite sheet into seperate images and put them in an image list
# snake parts image is 320 x 256 pixels with 5 images across and 4 down
# so therefore each image is 64 x 64 pixels
import pygame
pygame.init()
win = pygame.display.set_mode((700,840))

# this code loads the image into a surface called spriteSheet and outputs its size (just to be sure)
spriteSheet = pygame.image.load('spritesheet1.jpg')
print(spriteSheet.get_size())

# this code displays the full sprite sheet
win.fill((255,255,255))
win.blit(spriteSheet,(0,0))
pygame.display.update()
pygame.time.delay(2000)

# this code creates a list of snake images from the sprite sheet and puts them in a list
# I have chosen to take the images a row at a time (ie working across the sprite sheet
# but you could do it a column at a time (ie working down the sprite sheet) just as easily
Pictures = []
for y in range(0,840,120):
    for x in range(0,700,100):
        print(x,y)
       pictures.append(spriteSheet.subsurface((x,y,100,120)))


### this code draws one of the body parts.  Try changing it up to draw a different part!!
win.fill((200,200,200))
win.blit(pictures[48],(0,0))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
