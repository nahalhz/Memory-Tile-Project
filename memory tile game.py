#----------------------------------------------------------------------------
# Program: SUMMATIVE: MEMORY TILE GAME
# Author: Nahal H.
# Date: December 23, 2020
# Description: The program lets the users choose between three categories with 
# different difficulties which then randomly chooses a picture rebus puzzle for a
# multiplayer game of memory tiles under which the puzzle is hidden. The first player who
# is able to guess the puzzle is the winner. 
# They can quit the game and go back to categories menu to try another category 
# Input: User uses the cruisor to input coordinates and therefore allow
# them to press on the cards and so program to function accordingly based
# on the instruction that follow. They are also able to type of their guess
# in the input box that pops up to indicate whether they got it correctly or not. 
#---------------------------------------------------------------------------
#------------------------#
#    IMPORTING MODULES   #
#------------------------#
import pygame
import random
import math
import inputbox
#------------------------#
# SETTING SOME CONSTANTS #
#------------------------#
WIDTH = 700
HEIGHT = 700
FPS = 30
MAIN_SCREEN = 1
START_SCREEN = 0
CATEGORIES_SCREEN = 2
#------------------------#
# DEFINING COLOURS       #
#------------------------#
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
LIGHT_BLUE = (102,255,255)
LIGHT_PURPLE = (177,156,217)
BLUE = (64,224,208)
#------------------------#
# SETTING UP FONTS       #
#------------------------#
pygame.font.init()
regular_font = pygame.font.SysFont("arial", 20)
player_font = pygame.font.SysFont("calibri", 30)
statement_font = pygame.font.SysFont("calibri", 50)
#---------------------------------------#
# SETTING UP memory CARD Pictures       #
#---------------------------------------#
spriteSheet = pygame.image.load('spritesheet1.jpg')
pictures = []
for y in range(0,840,120):
    for x in range(0,700,100):
        pictures.append(spriteSheet.subsurface((x,y,100,120)))
backofCard = pygame.image.load('backCard1.png')
#---------------------------------------------------#
# FUNCTION TO CHOOSE RANDOM INDICES OF PICTURE LIST #
#---------------------------------------------------#
def randomCardList(n):
    imageIndices = [i for i in range(49)]
    board = []
    for i in range(n):
        rndIndex= random.randrange(0, len(imageIndices))
        num =imageIndices[rndIndex]
        board.append(num)
        del imageIndices[rndIndex]
    board = board * 2
    random.shuffle(board)
    return board
#----------------------------------------------------------------------------------#
# FUNCTION TO FIND CARD COORDINATES AND PLACE THEM IN DESIRED ROWS AND COLUMNS     #
#----------------------------------------------------------------------------------#
def getCardCoordinates(rows, cols,startx,starty):
    width = 100
    height = 120
    x,y = startx, starty
    gap = 5
    cardCoordinates = []
    for col in range(cols):
        for row in range(rows):
            cardCoordinates.append((x,y))
            x += width + gap
        y += height + gap
        x = startx
    return cardCoordinates
#-----------------------------------------#
# FUNCTION TO DRAW THE CARDS              #
#-----------------------------------------#
def drawCards(screen,cardCoordinates, board,backofCard):
    width = 100
    length = 120
    x,y = 130,100
    gap = 5
    for i,xy in enumerate(cardCoordinates):
        if i not in CardsUsed:
            if cardShown[i] == 1: 
                screen.blit(pictures[board[i]], (xy))
            elif cardShown[i] == 0:
                screen.blit(backofCard, (xy))    
#-----------------------------------------#
# FUNCTION TO DRAW RECTANGULAR BUTTONS    #
#-----------------------------------------#
def DrawRectButtons(screen,text,r,bColor=(177,156,217),fColor=(255, 0, 0),font=pygame.font.SysFont("arial", 30)):
    pygame.draw.rect(screen,bColor,r)
    pygame.draw.rect(screen,fColor, r, 3)
    txtSurface = font.render(text,True,(0, 0, 0))
    screen.blit(txtSurface, (r[0]+(r[2]-txtSurface.get_width())//2,r[1]+(r[3]-txtSurface.get_height())//2))
#-----------------------------------------------#
# FUNCTION TO DRAW RECTANGULAR BUTTONS IN A ROW #
#-----------------------------------------------#   
def drawRectBtns(rList, txtList, bColor=(177,156,217)):
    for i,r in enumerate (rList):
        DrawRectButtons(screen,txtList[i],r, bColor)
#------------------------------#
# FUNCTION TO GET BUTTON INDEX #
#------------------------------#
def getRectButtonIndex(rList, mp): # for Rectangular buttons
    for i,r in enumerate(rList):
        if pygame.Rect(r).collidepoint(mp):
            return i
    return -1

def getCardIndex(cardCoordinates, mp): # for the memory cards
    for i,xy in enumerate(cardCoordinates):
        if pygame.Rect((xy[0],xy[1],100,120)).collidepoint(mp):
            return i
    return -1
#------------------------------#
# FUNCTION TO CHANGE PLAYER    #
#------------------------------#
def changePlayer(totalPlayers=2):
    global currentPlayer
    currentPlayer += 1
    if currentPlayer == totalPlayers:
        currentPlayer = 0
#------------------------#
# FILES UPLOADED         #
#------------------------#
fileName = 'game-title.png'
fileUpload = pygame.image.load(fileName)
# How to read in categories an dthe answers of the guess pictures
fi = open('puzzleKey.txt', 'r')
puzzleANS = [[],[],[]]
categories = []
for cat in range(3):
    newCat = fi.readline().strip()
    categories.append(newCat)
    n = int(fi.readline().strip())
    for g in range(n):
        newPuzzleANS = fi.readline().strip()
        puzzleANS[cat].append(newPuzzleANS)
easyImages = []                                      
easyImages.append(pygame.image.load('easy1.png'))
easyImages.append(pygame.image.load('easy2.jpg'))
easyImages.append(pygame.image.load('easy3.png'))
mediumImages = []
mediumImages.append(pygame.image.load('medium1.jpg'))
mediumImages.append(pygame.image.load('medium2.png'))
mediumImages.append(pygame.image.load('medium3.jpg'))
hardImages = []
for i in range(3):
    fileNames = 'hard' + str(i+1) + '.jpg'
    hardImages.append(pygame.image.load(fileNames))
Imageslst = []
Imageslst.append(easyImages)
Imageslst.append(mediumImages)
Imageslst.append(hardImages)
#---------------------------#
# FUNCTION TO REDRAW SCREEN #
#---------------------------#
def redraw_screen():
    global delayOn
    global foundmatch
    global frstPick
    global scndPick
    global CardsUsed
    global cardCoordinates
    global currentPlayer
    global rndPuzzleIndex
    global gameDone
    global puzzleImage
    if currentScreen == MAIN_SCREEN:
        screen.fill(LIGHT_PURPLE)
        player1 = player_font.render('Player 1 ', True, YELLOW)
        screen.blit(player1,(15,15))
        player2 = player_font.render('Player 2 ', True, YELLOW)
        screen.blit(player2,(595,15))
        if gameDone == False:
            screen.blit(puzzleImage,(130,100))
            drawCards(screen,cardCoordinates, board, backofCard)
            drawRectBtns([guessBtns[currentPlayer]],guessBtnstxt,YELLOW) #only shows the guess button for the player who is his turn
            drawRectBtns(settingBtns,settingBtnstxt ,YELLOW)
        else:
            screen.blit(puzzleImage,(130,100))
            drawRectBtns(settingBtns,settingBtnstxt ,YELLOW)
            statement = 'Player '+str(currentPlayer+1)+' WINS!'
            statementDisplay = statement_font.render('GAME OVER!'+statement, True, RED)
            screen.blit(statementDisplay,((85,50)))
    elif currentScreen == START_SCREEN:
        screen.fill(YELLOW)
        screen.blit(fileUpload,(40 , 40))
        drawRectBtns(startBtn,startBtntxt)
    elif currentScreen == CATEGORIES_SCREEN:
        screen.fill(YELLOW)
        screen.blit(fileUpload,(40 , 40))
        drawRectBtns(categoriesBtn,categoriesBtntxt)
        drawRectBtns(quitBtn,quitBtntxt)
    pygame.display.update()
    if delayOn:   #delay when the cards flip so they are showed before they turned around or disappear
        delayOn = False
        pygame.time.delay(1000)
        if foundmatch:  #if the cards match
            cardShown[frstPick] = 2
            cardShown[scndPick] = 2
            CardsUsed.append(frstPick)
            CardsUsed.append(scndPick)
        else:
             cardShown[frstPick] = 0 
             cardShown[scndPick] = 0
        frstPick = -1
        scndPick = -1
    
#------------------------#
# INITIALIZING GAME      #
#------------------------#
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MEMORY TILES BY NAHAL H.")
#------------------------#
#      GAME LOOP         #
#------------------------#
currentScreen = START_SCREEN
running = True
gameDone = False
foundmatch = False
delayOn = False
currentPlayer = 0
guess_answer = ''
startBtn = [(250,300,200,100)]
startBtntxt = ['Start']
categoriesBtn = [(250,215,200,100),(250,355,200,100),(250,495,200,100)]
categoriesBtntxt = [ 'EASY', 'MEDIUM', 'HARD']
quitBtn = [(250,615,200,50)]
quitBtntxt = ['<QUIT>']
settingBtns = [(460,630,100,50),(580,630,100,50)]
settingBtnstxt = [ 'Menu', 'Quit']
guessBtns = [(30,485,80,80),(590,485,80,80)]
guessBtnstxt = [ 'GUESS','GUESS']
frstPick = -1
ScndPick = -1
CardsUsed = []
cardCoordinates = getCardCoordinates(4,4,130,100)
board = randomCardList(8)
cardShown = [0] * len(board)
while running:
    redraw_screen()
    clock = pygame.time.delay(30)
    # process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:   #if user clicks anywhere on screen
            clickPos = pygame.mouse.get_pos()
            if currentScreen == START_SCREEN:      #you're in the start category screen
                startBtnIndex = getRectButtonIndex(startBtn, clickPos)
                if  startBtnIndex != -1:
                    currentScreen = CATEGORIES_SCREEN
            elif currentScreen == CATEGORIES_SCREEN:
                    categoriesBtnIndex = getRectButtonIndex(categoriesBtn, clickPos)
                    quitBtnIndex = getRectButtonIndex(quitBtn, clickPos)
                    if categoriesBtnIndex != -1:
                        c = categoriesBtnIndex
                        rndPuzzleIndex = random.randrange(0,len(puzzleANS[c])) #random indice for picking a puzzle for the category
                        guess_answer = puzzleANS[c][rndPuzzleIndex] #variable to store the guess answer
                        puzzleImage = Imageslst[c][rndPuzzleIndex]  #variable to store the picture
                        currentScreen = MAIN_SCREEN
                    elif quitBtnIndex != -1:
                        running = False         
            elif currentScreen == MAIN_SCREEN:       # you're in the main game screen
                settingBtnsIndex = getRectButtonIndex(settingBtns, clickPos)
                if settingBtnsIndex != -1:
                    if settingBtnsIndex == 0:
                        gameDone = False
                        currentScreen = CATEGORIES_SCREEN
                        cardShown = [0] * len(board)
                        frstPick = -1
                        ScndPick = -1
                        CardsUsed = []
                        currentPlayer = 0
                    else:
                        running = False
                else:
                    cardIndex = getCardIndex(cardCoordinates, clickPos)
                    if cardIndex != -1:
                        cardShown[cardIndex] = 1
                        if frstPick == -1:
                            frstPick = cardIndex
                        elif frstPick != -1:
                            scndPick = cardIndex
                            if board[frstPick] == board[scndPick]:
                                foundmatch = True
                            else:
                                foundmatch = False
                            delayOn = True
                            changePlayer()
                    guessBtnsIndex = getRectButtonIndex(guessBtns, clickPos)
                    if guessBtnsIndex != -1:
                        answer = inputbox.ask(screen, "Your answer:") #input box is shown 
                        if answer.lower() == guess_answer:            #if the answer the user puts is the same as the puzzle
                            gameDone = True
pygame.quit()


                     


                

                    
                        
                           
                        
                        
    

