from pygame import *
from random import *
from math import *

width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

X=0
Y=1
W=2
H=3
S=4

game="menu"

fish=[400,300,30,15,0]    #coordinate of fish and its width and height
vel=[0,0]               #The speed of the fish [hor speed, vert speed]
accel=[0,0]             #Acceleration of the fish [hor accel,vert,accel]
fishyPic=image.load("images/fishyPre.png")

bonesPic=image.load("images/bones.png")         #loading in bone picture
bonesSize=transform.scale(bonesPic,(100,50))    #Scaling in to a diffrent size
bones=transform.flip(bonesSize,False,True)      #Fliping it upside down
yBones=300                                      #Its starting y pos

squid=[400,300,30,15]                       #Coordinate and size of squid
squidLoad=image.load("images/squid.png")    #loading in image
squidPic=transform.rotate(squidLoad,(90))   #Rotating image horizontaly
squidStart=[]                               #Where the squid starts when clicked
destination=[]                              #Where the user clicked
firstClick=0                                #The first click shouldn't count

score=0                     #score of player

enemy=[]                # coordiante of all enemy fish on screen
side=[]                 # 0's and 1's 0 represents coming from right side and 1 represents coming from left side
eSpeed=[]               # Random number the speed on the enemy
eSize=[]                # The enemies size(width * height)

shark=[-50,-25,75,37,0]                     #Starting Pos and size of shark
sharkComp="pending"                         #checks if shark has been completed        
sharkTimer=0                                #Timer for how long it runs
sharkPic=image.load("images/shark.png")     #Loading in image
sharkImage=transform.scale(sharkPic,(shark[W],shark[H]))#Changing size

rMenu=Rect(10,10,50,50)             #The rect displayed to go back to the menu
homePic=image.load("images/home.png")
homeImage=transform.scale(homePic,(50,50))
retry=Rect(375,365,50,50)          #The rect displayed to retry the game
restartPic = image.load("images/restart.png")
restartImage=transform.scale(restartPic,(50,50))

start=Rect(50,150,200,30)          #The rect displayed to start the game
rules=Rect(50,300,200,30)          #The rect displayed to see the rules
character=Rect(50,450,200,30)      #The rect displayed to go to chracter select

player="fish"                       #Which player is in use

bx=0                    #This is the horizontal value of the bar on the screen
nextLevel=False         #Checks if he opponent went to the next level
stage=1                 #What stage is the player on
timer=[0,0]             #The timer which runs when you go to the next level

star=[0,-50,30,30,0,0,0]                #the coordinates,size and status of star
starPic=image.load("images/star.png")   #Loading in star image
powerTimer=0                            #This timer runs when you have your power
powerPicsFish=[]                        #Holds the fish's power pics
powerPicsSquid=[]                       #Holds the squids's power pics
colourInd=0                             #Holds the ind for what color to display

#This loads in all the power pic images
for i in range(5):
    powerPicsFish.append("images/powerFish"+str(i)+".png")

for i in range(5):
    powerPicsSquid.append("images/powerSquid"+str(i)+".png")

pause=0                         #Status of the pause screen
pauseMenu=Rect(300,200,200,20)  #Pause button to go to menu
pauseRetry=Rect(300,300,200,20) #Pause button to retry

#These lines of code loads in all the images and scale them to the screen
backgroundPics=[]
backgroundInd=0
for i in range(5):
    backgroundLoad=image.load("images/background"+str(i)+".jpg").convert()
    background=transform.scale(backgroundLoad,(width,height))
    backgroundPics.append(background)

fishyBackgroundLoad=image.load("images/fishyBackground.jpg").convert()
fishyBackground=transform.scale(fishyBackgroundLoad,(width,height))

squidBackgroundLoad=image.load("images/squidBackground.jpg").convert()
squidBackground=transform.scale(squidBackgroundLoad,(width,height))

arrowKeysPic=image.load("images/arrowKeys.png")
arrowKeysImage=transform.scale(arrowKeysPic,(100,100))

cursorPic=image.load("images/cursor.png")
cursorImage=transform.scale(cursorPic,(50,50))

enemyPics=[]
for i in range(11):
    enemyPics.append("images/enemy"+str(i)+".png")


font.init()

mixer.init()
mixer.music.load("songs/FISHY! - Main Music.mp3") #loads song
mixer.music.play(loops=-1) #Plays song

sound_effect = mixer.Sound("songs/Burp.wav")

def menu():
    '''
This fuction is used to create the menu and setup its functions
    '''
    if player=="fish":
        screen.blit(fishyBackground,(0,0))
        myfont=font.SysFont("Comic Sans MS",40)
        title = myfont.render("FISHY", False, WHITE)
        screen.blit(title,(350,10))
        
    if player=="squid":
        screen.blit(squidBackground,(0,0))
        myfont=font.SysFont("Comic Sans MS",40)
        title = myfont.render("SQUIDY", False, WHITE)
        screen.blit(title,(325,10))

##This block of code displays the diffrent buttons which take you to diffrent
##screens
    draw.rect(screen,(255,255,255),start,1)       # Starts game
    myfont=font.SysFont("Comic Sans MS",20)
    startText = myfont.render(str("START"), False, (255, 255, 255))
    screen.blit(startText,(115,150))
    draw.rect(screen,(255,255,255),rules,1)       # Instruction screen
    instructionsText = myfont.render(str("Instructions"), False, (255, 255, 255))
    screen.blit(instructionsText,(95,300))
    draw.rect(screen,(255,255,255),character,1)   # Character and control screen
    characterSelectText = myfont.render(str("Character Select"), False, (255, 255, 255))
    screen.blit(characterSelectText,(70,450))

    if start.collidepoint(mx,my):
        draw.rect(screen,BLACK,start,1)
    if rules.collidepoint(mx,my):
        draw.rect(screen,BLACK,rules,1)
    if character.collidepoint(mx,my):
        draw.rect(screen,BLACK,character,1)
   
##This block checks if a button was pressed and changes the game mode to that
##screens name
    if click==True and start.collidepoint(mx,my):
        return "levels"
    if click==True and rules.collidepoint(mx,my):
        return "instructions"
    if click==True and character.collidepoint(mx,my):
        return "character"
    return "menu"

def instructions():
    '''
    This function displays the instructions of the game
    '''
    screen.fill((10,192,205))
    if player=="fish":
        myfont=font.SysFont("Comic Sans MS",15)
        fishyOb = myfont.render(str("The goal of Fishy is to eat as many fish as possible, the bigger the fish the higher you score"), False, (255, 255, 255))
        fishyRu = myfont.render(str("But make sure they aren't too big, if they are bigger or the same size as you they will gobble you up!"), False, (255, 255, 255))
        fishyLim = myfont.render(str("There is a limit to how many fish you can eat per level, the higher the level the more fish you need to eat"), False, (255, 255, 255))
        fishyPow = myfont.render(str("Once in a while a power up will drop down, it will allow you to cross bigger fish without getting eaten"), False, (255, 255, 255))
        fishyBoss =  myfont.render(str("Be careful! There is a shark lurking about and it loves fish!"), False, (255, 255, 255))
        fishyCon = myfont.render(str("To move the fish use the arrow keys, press the space bar to pause"), False, (255, 255, 255))
        screen.blit(fishyOb,(50,100))
        screen.blit(fishyRu,(50,125))
        screen.blit(fishyLim,(50,150))
        screen.blit(fishyPow,(50,175))
        screen.blit(fishyBoss,(50,200))
        screen.blit(fishyCon,(50,225))
        screen.blit(arrowKeysImage,(350,260))
        screen.blit(fishyPic,(250,400))
        

    if player=="squid":
        myfont=font.SysFont("Comic Sans MS",15)
        squidyOb = myfont.render(str("The goal of Squidy is to eat as many fish as possible, the bigger the fish the higher you score"), False, (255, 255, 255))
        squidyRu = myfont.render(str("But make sure they aren't too big, if they are bigger or the same size as you they will gobble you up!"), False, (255, 255, 255))
        squidyLim = myfont.render(str("There is a limit to how many fish you can eat per level, the higher the level the more fish you need to eat"), False, (255, 255, 255))
        squidyPow = myfont.render(str("Once in a while a power up will drop down, it will allow you to cross bigger fish without getting eaten"), False, (255, 255, 255))
        squidyBoss =  myfont.render(str("Be careful! There is a shark lurking about and it loves squid!"), False, (255, 255, 255))
        squidyCon = myfont.render(str("To move the squid use the mouse and click anywhere, press the space bar to pause"), False, (255, 255, 255))
        screen.blit(squidyOb,(50,100))
        screen.blit(squidyRu,(50,125))
        screen.blit(squidyLim,(50,150))
        screen.blit(squidyPow,(50,175))
        screen.blit(squidyBoss,(50,200))
        screen.blit(squidyCon,(50,225))
        screen.blit(cursorImage,(100,400))
        screen.blit(squidPic,(350,305))
        
## This block of code displays the instructions and the return button
    myfont=font.SysFont("Comic Sans MS",40)
    iTitle = myfont.render("Instructions", False, WHITE)
    screen.blit(iTitle,(300,20))
    screen.blit(homeImage,(10,10))

## IF the return button is pressed you are taken back to the menu screen    
    if click==True and rMenu.collidepoint(mx,my):
        return "menu"
    return "instructions"

def controls():
    '''
    This function displays the character select screen and the controls for each
    '''
    screen.fill((10,192,205))
## This block of code displays the characters and the return button    
    myfont=font.SysFont("Comic Sans MS",40)
    cTitle = myfont.render("Character Select", False, WHITE)
    screen.blit(cTitle,(250,20))
    screen.blit(homeImage,(10,10))

## If this button is pressed you are taken back to the menu screen
    if click==True and rMenu.collidepoint(mx,my):
        return "menu"
    return "character"

def characterSelect(char):
    '''
    This function checks what character the user has selected and return "fish"
    or "squid" and then that value is placed in the player variable
    '''
    #Displays the buttos to select the character
    selectFishImage=transform.scale(fishyPic,(300,150))
    screen.blit(selectFishImage,(75,250))
    selectSquidImage=transform.scale(squidLoad,(150,400))
    screen.blit(selectSquidImage,(500,150))

    if player=="fish":
        draw.rect(screen,(255,255,255),selectFishImage.get_rect(center=(225,325)),1)
    
    if player=="squid":
        draw.rect(screen,(255,255,255),selectSquidImage.get_rect(center=(575,350)),1)
        
    #If the button is clicked it return the player
    if click==True and selectFishImage.get_rect(center=(225,325)).collidepoint(mx,my):
        return "fish"
    if click==True and selectSquidImage.get_rect(center=(575,350)).collidepoint(mx,my):
        return "squid"
    return char
   
def moveFish():
    '''moveFish is used to move the main character. In this function, we
    accelerate to 10 and add that to the velocity which then moves the fish
    '''
   
##  These lines of code accelerate and decelerate the fish, When the number hits
##  10 or -10 depending on its direction, it will not accelerate further than
##  that. If the key is not pressed and the acceleration is not zero it will
##  push it down to zero    
    keys=key.get_pressed()
    if keys[K_RIGHT] and accel[X]<10:
        accel[X]=accel[X]+.5
    if not keys[K_RIGHT] and accel[X]>0:
        accel[X]=accel[X]-.25
       
    if keys[K_LEFT] and accel[X]>-10:
        accel[X]=accel[X]-.5
    if not keys[K_LEFT] and accel[X]<0:
        accel[X]=accel[X]+.25
       
    if keys[K_DOWN] and accel[Y]<10:
        accel[Y]=accel[Y]+.5
    if not keys[K_DOWN] and accel[Y]>0:
        accel[Y]=accel[Y]-.25
       
    if keys[K_UP] and accel[Y]>-10:
        accel[Y]=accel[Y]-.5
    if not keys[K_UP] and accel[Y]<0:
        accel[Y]=accel[Y]+.25
       
##  This part adds the acceleration to the velocity. Then adds the velocity
##  to thefish's coordinate
    vel[X] = round(accel[X])
    fish[X] += round(vel[X])
    vel[Y] = round(accel[Y])
    fish[Y] += round(vel[Y])
   
##  This Block of code makes the fish stay within the screen, If he crosses the
##  horizontal limit, he goes to the other side. If he crosses the vertical
##  limit, its gets blocked
    if fish[X]>width:
        fish[X]=-fish[W]
    if fish[X]<-fish[W]:
        fish[X]=width

    if fish[Y]<0:
        fish[Y]=0
    if fish[Y]+fish[H]>height:
        fish[Y]=height-fish[H]
                                 
def createEnemy():
    '''
    This fucntion creates the enem fish, when there are less than 10 on the
    screen. It assigns the fish a random size, starting coordinate and speed.
    appends all these values to muliple lists.
    '''
    if player =="fish":
        ani=fish
    if player=="squid":
        ani=squid
    if len(enemy)<10:                       #Only runs if less than 10 enemies
        r=randint(0,1)                      #What side it will start from
        ew=randint(ani[W]-10,ani[W]+10)   #Random width
        eh=int(ew/2)                        #Width divided by two
        ex=0                                #x value
        ey=randint(0,height-eh)             #random y value
       
##    This block of code decides what side the fish starts on, and appends its
##    random speed and size to lists. Which are are paralel to one another
        if r==0:    
           ex=-ew
           side.append(0)
           eSpeed.append(randint(1,15))
           eSize.append(ew*eh)
        else:
            ex=width
            side.append(1)
            eSpeed.append(randint(1,15))
            eSize.append(ew*eh)
        enemy.append([ex,ey,ew,eh,randint(0,10)])

def moveEnemy():
    '''
    This function moves the enemy in a linear fashion
    '''

##    This block of code checks what side the fish is on, and moves the fish
##    accordingly. By adding or substrating the speed which corresponds to it.
    for i in range(len(enemy)):
        if side[i]==0:
            enemy[i][X]=enemy[i][X]+eSpeed[i]
        if side[i]==1:
            enemy[i][X]=enemy[i][X]-eSpeed[i]

def eRemove(i):
    '''
    This function is called when contact is made or the enemy has left the
    screen. It will remove all aspect of the enemy. Like its coordinate
    size and speed
    '''
   
##    This block is removing every aspect of the enemy
    enemy.pop(i)
    side.pop(i)
    eSpeed.pop(i)
    eSize.pop(i)
    if sharkComp!="incomplete":
        createEnemy()

def enemyLimit():
    '''
    This function removes the enemy once it crosses the screen, so that more
    enemies can be made
    '''

##    This block of code checks to see what side the fish came from, if it crossed
##    the screen. Then removes it. Create enemy is imediatly called to create
##    a new fish. So the the list is not out of range
    for i in range(len(enemy)):
        if side[i]==0 and enemy[i][X]>width:
            eRemove(i)
        if side[i]==1 and enemy[i][X]<-enemy[i][W]:
            eRemove(i)

def checkContact(i):
    '''
    This function checks if there was contact between the fish and the enemy
    '''
   
##    This block of code get every pixel of the fish and checks if it has collided
##    with the enemy. I check every pixel because it makes the collision detection
##    more precise
    if player=="fish":
        eRect=Rect(enemy[i][X],enemy[i][Y],enemy[i][W],enemy[i][H])
        for x in range(fish[W]):
            for y in range(fish[H]):
                if eRect.collidepoint(fish[X]+x,fish[Y]+y):
                    return True
    if player=="squid":
        squidContactScale=transform.scale(squidPic,(fish[W],fish[H]))
        squidContact= transform.rotate(squidContactScale,squidAngle())
        sRect=squidContact.get_rect(center=(squid[X]+(round(squid[W]/2)),squid[Y]+(round(squid[H]/2))))
        for x in range(enemy[i][W]):
            for y in range(enemy[i][H]):
                if sRect.collidepoint(enemy[i][X]+x,enemy[i][Y]+y):
                    return True
                   
def scorer():
    '''
    This function checks if there was contact with a fish smaller than you then
    adds to your score accordingly
    '''
    worth=0                                   #How much the enemy fish is worth

##  This block of code checks for contact with a smaller fish than you,
##  than returns it's worth, which is then added to score down below.
##  Also worth is inputed to growth, growth will be explained below
    for i in range(len(enemy)):
        if checkContact(i) and size>eSize[i]:
            worth+=int(eSize[i]/10)
            growth(worth)
            return worth                      # Returning worth of enemy
    return worth                              # Returns 0

def level():
    '''
    Adds a constant number to your limit bar, it is diffrent per level
    '''
   
##This block checks for contact and returns a value which will then be added to
##the limit bar
    for i in range(len(enemy)):
        if checkContact(i) and size>eSize[i]:
            eRemove(i)
            return int(10/stage)
    return 0

def levelAni(x):
    '''
    This function runs a timer for 100 frames and displays the level you are on
    '''

    #If the next level has been reached the timer runs for 100 frames
    if x>=50:
        timer[0]=1

    if timer[0]==1 and timer[1]<100:
        timer[1]+=1

    if timer[0]==1 and timer[1]>=100:
        timer[0]=0
        timer[1]=0
       

def levelUp(x,lev):
    '''
    This function checks if you reached the next level, then increases it if
    true
    '''

## pushes all enemies back and places fish in the middle, then the new level
## begins
    if x>=50:
        fish[X]=400
        fish[Y]=300
        squid[X]=400
        squid[Y]=300
        star[X]=0
        star[Y]=-50
        star[5]=0
        star[6]=0
        vel[X],vel[Y]=0,0              
        accel[X],accel[Y]=0,0            
        del enemy[:]              
        del side[:]                  
        del eSpeed[:]              
        del eSize[:]
        del destination[:]
        del squidStart[:]
        return 0,lev+1,True              # returns numbers that Resets the level bar and add 1 to your level
    return x,lev,False                    # Returns original values

def growth(num):
    '''
    This function recieves the worth of the enemy from points then checks if
    the score is high enough for the fish to grow
    '''
   
    curr=int(score/(size/10))       #Checks the current score proportional to size
    prev=int((score-num)/(size/10)) #Checks the previous score proportional to size

##    This block of code checks if the previous score proportional to size is
##    not equal to to current score poroprtional to size. It will then grow the
##    fish by adding 5 to the width, and to keep the fish looking like a fish
##    the height is equal to half of the width
    if prev != curr and player=="fish":
        fish[W]=fish[W]+1
        fish[H]=int(fish[W]/2)
    if prev != curr and player=="squid":
        squid[W]=squid[W]+1
        squid[H]=int(squid[W]/2)

def boss():
    '''
    This function moves the boss
    '''

    #Checks what character is in use
    if player=="fish":
        ani=fish
    if player=="squid":
        ani=squid

    #Gets the angle to the player then moves the shark accordingly using trig
    sharkAngle=atan2(ani[Y]-shark[Y],ani[X]-shark[X])
    shark[X]+=round(7*cos(sharkAngle))
    shark[Y]+=round(7*sin(sharkAngle))
   
def checkBossContact():
    '''
    This function checks if the shark has made contact with the player
    '''

    #If the player is a fish is will check contact witht he fish
    if player=="fish":
        sharkRect=Rect(shark[X],shark[Y],shark[W],shark[H])
        for x in range(fish[W]):
            for y in range(fish[H]):
                if sharkRect.collidepoint(fish[X]+x,fish[Y]+y):
                        return True
                   
    #If the player is squid it checks contact with squid
    if player=="squid":
        squidContactScale=transform.scale(squidPic,(fish[W],fish[H]))
        squidContact= transform.rotate(squidContactScale,squidAngle())
        sRect=squidContact.get_rect(center=(squid[X]+(round(squid[W]/2)),squid[Y]+(round(squid[H]/2))))
        for x in range(shark[W]):
            for y in range(shark[H]):
                if sRect.collidepoint(shark[X]+x,shark[Y]+y):
                        return True
                   
def bossStatus(status):
    '''
    The boss runs for 1000 frames if you reach the end of the timer you have
    completed the shark
    '''

    #returns complete or incomplete to the shark comp status holder
    if sharkTimer==500:
        return "complete"
    return "incomplete"


def bossTimer(num):
    '''
    Runs the timer for the boss it returns an added value to the shark timer
    '''

    # if the timer isnt completed then it adds one to the timer and once
    #completed it returns 1000
    if num<500 and pause!=1:
        st=num+1
        return st
    if pause==1:
        return num
    return 500

def checkStarContact():
    '''
    This function checks if the player has made contact with the power up
    '''

    #If the player is fish it checks contact with the fish
    if player=="fish":
        starRect=Rect(star[X],star[Y],star[H],star[W])
        for x in range(fish[W]):
            for y in range(fish[H]):
                if starRect.collidepoint(fish[X]+x,fish[Y]+y):
                        return True
        return False

    #If the player is a squid then it checks contact with the squid
    if player=="squid":
        squidContactScale=transform.scale(squidPic,(fish[W],fish[H]))
        squidContact= transform.rotate(squidContactScale,squidAngle())
        sRect=squidContact.get_rect(center=(squid[X]+(round(squid[W]/2)),squid[Y]+(round(squid[H]/2))))
        for x in range(star[W]):
            for y in range(star[H]):
                if sRect.collidepoint(star[X]+x,star[Y]+y):
                        return True
        return False

def power(num):
    '''
    This function runs when the player has colected the power up and runs a 300
    frame timer
    '''

    #If contact has been made then the timer is run, and the star[6]=1
    #once the timer is run through star[6]=0 and the timer is then turned to
    #0
    if checkStarContact():
        star[6]=1
    if star[6]==1 and num<300 and pause!=1:
        pt=num+1
        return pt
    if pause==1:
        return num
    if num>=300:
        star[6]=0
    return 0

def powerUp(nl,x):
    '''
    This function moves the powerup star, and when it is collected it moves away
    or when it reaches the bottom
    '''

    #This code checks if the next level has been reached, and resets the power up
    #You can only get one power up per level
    if nl==True and star[5]==0:
        star[5]=1
        star[4]=randint(10,40)
        star[X]=randint(0,770)
    if star[5]==1 and x>=star[4] and star[Y]<height+100 and pause!=1:
        star[Y]+=1
    if star[Y]>=height+100 or star[6]==1:
        star[Y]=-50
        star[5]=0

def colourIndex(num):
    '''
    If the power up has been colected this runs an index so tat it ca shuffle
    though a bunch of colors to give a cool animation
    '''

    #Runs through 0-4 and is used as an index to go though the power pics list
    if powerTimer>0 and pause!=1:
        if num==4:
            return 0
        else:
            ci=num+1
            return ci
    if pause==1:
        return num
    return 0
     
def checkLoss(mode):
    '''
    This function checks if you touched a fish bigger than you, if you did than
    it returns zero and game is equal to 1. When game equals 1, that means you
    lost and the game is over
    '''

##    This block of code checks if you made contact with a fish bigger than you
##    if you did it returns 1, if not it return 0 and you keep playing.
    for i in range(len(enemy)):
        if checkContact(i) and size<=eSize[i] and powerTimer==0:
            return "end"
    if sharkComp=="incomplete":
        if checkBossContact():
            return "end"  
    return mode
   
def end():
    '''
    This function displays the gameover screen
    '''
    screen.blit(background,(0,0))
    myfont=font.SysFont("Comic Sans MS",25)
    points = myfont.render("Score: "+str(score), False, WHITE) #Creates text
    levDisplay = myfont.render("Level: "+str(stage), False, WHITE) #Creates text
    screen.blit(points,(350,300))                    #Displays points
    screen.blit(levDisplay,(350,275))                    #Displays points
    screen.blit(restartImage,(375,365))
    screen.blit(homeImage,(10,10))                   #Displays menu button
    screen.blit(bones,(350,bonesAni(yBones)))

def bonesAni(num):
    '''
    If the player dies then the bone animation is run this just makes it look
    like the bone is floating
    '''

    #Starts at 50 then goes down so that the y value does as well, moving the
    #bone image up
    if num!=50:
        y=num-1
        return y
    return 50

def restart():
    '''
This function restarts every value in the game
    '''

##    This block of code restarts all values, and is called when wanting to
##    restart the game
    fish[X]=400
    fish[Y]=300
    fish[W]=30
    fish[H]=15
    squid[X]=400
    squid[Y]=300
    squid[W]=30
    squid[H]=15
    shark[X]=-50
    shark[Y]=-25
    star[X]=0
    star[Y]=-50
    star[4]=0
    star[5]=0
    star[6]=0
    vel[X],vel[Y]=0,0              
    accel[X],accel[Y]=0,0
    del destination[:]
    del squidStart[:]
    del enemy[:]              
    del side[:]                  
    del eSpeed[:]              
    del eSize[:]

def gameover(mode,points,limit,lev,Fclick,ybo,p,st,sc,pt):
    '''
    This function restarts all the values in the game so that the player can
    start from scratch
    '''
   
##    This block of code restarts all the values, when the retry button is
##    pressedthen it returns level 1, so that the game mode is level 1. And
##    it returns 0 to restart the score.
    if click==True and retry.collidepoint(mx,my):
        restart()
        return "levels",0,0,1,1,300,0,0,"pending",0
    if click==True and rMenu.collidepoint(mx,my):
        restart()
        return "menu",0,0,1,0,300,0,0,"pending",0
    return mode,score,limit,lev,Fclick,ybo,p,st,sc,pt


################################################################################
def squidAngle():
    '''
    This function gets the angle at which the squid's coordinates are to the
    mouse. Then it returns it. This angle will be used to then rotate the
    image so that it looks as though the squid is facing the mouse
    '''
##    This block of code gets all the neccesarry measurments, which will be used
##    to calculate the angle. Such as the x-Component, y-Component and the
##    hypotneuse
    xComp = mx-squid[X]
    yComp= my-(squid[Y]+squid[H]/2)
    hyp=sqrt(xComp**2 + yComp**2)

##    Then we calculate what the angle will be using trignometric functions. If
##    the hypotneuse if zero, you will get an error. So I used the try and pass
##    functions to then return the angle
    try:
        if xComp<0 and yComp>0:
            angle=degrees(asin(yComp/hyp))
        if xComp>=0:
            angle=(degrees(asin(yComp/hyp))-180)*-1
        if xComp<0 and yComp<0:
            angle=degrees(asin(yComp/hyp))+360
        return angle
    except:
        return 0

def moveSquid():
    '''
    This funtion is used to move the squid around the screen
    '''

##    If the player has clicked then the destination at staring pos gets set
    if mb[0]==1 and sqrt((mx-squid[X])**2 + (my-squid[Y])**2)>squid[W]+20:
        del destination[:]
        del squidStart[:]

##    If the length of the destination list is full then this won't run
##    If it is empty then all the values to move the squid are added in
##    Such as the angle from the squid to destination, the coordinates of
##    of the destination and start
        if len(destination)==0 :
            destination.append(mx)
            destination.append(my)
            squidStart.append(squid[X])
            squidStart.append(squid[Y])
            destination.append(atan2(destination[Y]-squidStart[Y],destination[X]-squidStart[X]))

    if len(destination) != 0 :
       
##      This block uses trig to move the squid towards were the user clicked
##      it uses the angle and hen the speed is 10 so that te squid moves
        squid[X]+=round(10*cos(destination[2]))
        squid[Y]+=round(10*sin(destination[2]))
           
##        Once the squid reaches, the old coordinate is erased, and the user
##        can then move the squid again
        if squid[X]<destination[X]+20 and squid[X]>destination[X]-20 and squid[Y]<destination[Y]+20 and squid[Y]>destination[Y]-20:
            del destination[:]
            del squidStart[:]
           
def pauseScreen(mode,score,limit,lev,fClick,ybo,p,st,sc,pc):        
    if click==True and pauseMenu.collidepoint(mx,my):
        restart()
        return "menu",0,0,1,0,300,0,0,"pending",0
    if click==True and pauseRetry.collidepoint(mx,my):
        restart()
        return "levels",0,0,1,1,300,0,0,"pending",0
    return mode,score,limit,lev,fClick,ybo,p,st,sc,pc

def sounds():
    for i in range(len(enemy)):
        if checkContact(i)==True and powerTimer==0:
                sound_effect.play()
        if checkContact(i)==True and powerTimer>0:
            if size>eSize[i]:
                sound_effect.play()
            
def backgroundIndex(num):
    if num==4:
        return 0
    elif pause==1:
        return num
    else:
        bi=num+1
        return bi

def drawScene():
    '''
    This draw the background and the fish
    '''
    screen.blit(backgroundPics[backgroundInd],(0,0))
    myfont=font.SysFont("Comic Sans MS",10)
    scr = myfont.render("SCORE", False, WHITE)
    screen.blit(scr,(390,5))
    myfont=font.SysFont("Comic Sans MS",25)
    points = myfont.render(str(score), False, WHITE)
    screen.blit(points,(400,15))
    myfont=font.SysFont("Comic Sans MS",10)
    levDisplay = myfont.render("LEVEL "+str(stage), False, WHITE)
    screen.blit(levDisplay,(70,7))
       
    draw.rect(screen,GREEN,(10,10,50,10),1)
    draw.rect(screen,GREEN,(10,10,bx,10))
   
    for i in range(len(enemy)):             #This draws all the enemies
        enemyPic=image.load(enemyPics[enemy[i][S]])
        if side[i]==0:
            enemyImage=transform.scale(enemyPic,(enemy[i][W],enemy[i][H]))
            screen.blit(enemyImage,(enemy[i][X],enemy[i][Y]))
        if side[i]==1:
            enemyFlip=transform.flip(enemyPic,True,False)
            enemyImage=transform.scale(enemyFlip,(enemy[i][W],enemy[i][H]))
            screen.blit(enemyImage,(enemy[i][X],enemy[i][Y]))    

    if player=="fish":
        keys=key.get_pressed()
        if keys[K_RIGHT] and keys[K_LEFT] and pause!=1:
            if accel[X]>0:
                fish[S]=1
            if accel[X]<0:
                fish[S]=0
        if keys[K_LEFT] and not keys[K_RIGHT] and pause!=1:
            fish[S]=0
        if fish[S]==0 and powerTimer==0:
            fishyFlip=transform.flip(fishyPic,True,False)
            fishyImage=transform.scale(fishyFlip,(fish[W],fish[H]))
            screen.blit(fishyImage,(fish[X],fish[Y]))
        if keys[K_RIGHT] and not keys[K_LEFT] and pause!=1:
            fish[S]=1
        if fish[S]==1 and powerTimer==0:
            fishyImage=transform.scale(fishyPic,(fish[W],fish[H]))
            screen.blit(fishyImage,(fish[X],fish[Y]))

        if powerTimer>0:
            powerPic=image.load(powerPicsFish[colourInd])
            if fish[S]==0:
                powerFlip=transform.flip(powerPic,True,False)
                powerImage=transform.scale(powerFlip,(fish[W],fish[H]))
                screen.blit(powerImage,(fish[X],fish[Y]))

            if fish[S]==1:
                powerImage=transform.scale(powerPic,(fish[W],fish[H]))
                screen.blit(powerImage,(fish[X],fish[Y]))
           
    if player=="squid":
       
##        This block of code is loading the image then blitting it on the screen
        if powerTimer==0:
            squidScale=transform.scale(squidPic,(squid[W],squid[H]))
            if pause==0:
                squidImage= transform.rotate(squidScale,squidAngle())
            if pause==1:
                squidImage= transform.rotate(squidScale,0)
            screen.blit(squidImage,(squid[X],squid[Y]))

        if powerTimer>0:
            powerPic=image.load(powerPicsSquid[colourInd])
            powerRot=transform.rotate(powerPic,(90))
            powerSquidScale=transform.scale(powerRot,(squid[W],squid[H]))
            if pause==0:
                powerSquidImage= transform.rotate(powerSquidScale,squidAngle())
            if pause==1:
                powerSquidImage= transform.rotate(powerSquidScale,0)
            screen.blit(powerSquidImage,(squid[X],squid[Y]))
       
    if sharkComp=="incomplete":
        if player=="fish":
            ani=fish
        if player=="squid":
            ani=squid
        if ani[X]-shark[X]<0:
            shark[S]=0
        if ani[X]-shark[X]>0:
            shark[S]=1
        if shark[S]==0:
            screen.blit(sharkImage,(shark[X],shark[Y]))
        if shark[S]==1:
            sharkFlip=transform.flip(sharkImage,True,False)
            screen.blit(sharkFlip,(shark[X],shark[Y]))

    starImage=transform.scale(starPic,(star[W],star[H]))
    screen.blit(starImage,(star[X],star[Y]))

    if timer[1]>0:
        myfont=font.SysFont("Comic Sans MS",40)
        nextLevelText = myfont.render("LEVEL "+str(stage), False, (255,255,255))
        screen.blit(nextLevelText,(350,250))
       
    if pause==1:
        draw.rect(screen,(255,255,255),(200,100,400,400))
        draw.rect(screen,(255, 188, 125),(200,100,400,400),4)
        draw.rect(screen,(255, 188, 125),pauseMenu,1)
        draw.rect(screen,(255, 188, 125),pauseRetry,1)
        myfont=font.SysFont("Comic Sans MS",15)
        pauseMenuText = myfont.render(str("MENU"), False, (255, 188, 125))
        pauseRestartText = myfont.render(str("RESTART"), False, (255, 188, 125))
        pauseResumeText = myfont.render(str("PRESS SPACE TO RESUME"), False, (255, 188, 125))
        screen.blit(pauseMenuText,(378,199))
        screen.blit(pauseRestartText,(368,299))
        screen.blit(pauseResumeText,(305,399))
        myfont=font.SysFont("Comic Sans MS",25)
        pauseTitle = myfont.render(str("PAUSE"), False, (255, 188, 125))
        screen.blit(pauseTitle,(367,107))
       

running=True
click=False
myClock = time.Clock()
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            click=True
        if evt.type == KEYUP :
            if evt.key == K_SPACE and pause==0 :
                pause=1
            elif evt.key == K_SPACE and pause==1:
                pause=0
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

##    Calling all functions
    if game=="menu":
        game=menu()
           
       
    if game=="instructions":
        game=instructions()

    if game=="character":
        game=controls()
        player=characterSelect(player)
       
    if game=="levels":
        if player == "fish":
            size=fish[W]*fish[H]    #Size of the fish
            if pause!=1:
                moveFish()
            if sharkComp!="incomplete":
                createEnemy()
            if pause != 1 and sharkComp!="incomplete":
                moveEnemy()
            enemyLimit()
            score+=scorer()
            sounds()
            bx+=level()
            levelAni(bx)
            bx,stage,nextLevel=levelUp(bx,stage)
            if stage==3:
                sharkComp=bossStatus(sharkComp)
            if stage==3 and sharkComp=="incomplete":
                for i in range(len(enemy)):
                    eRemove(i)
                if pause!=1:
                    boss()
                sharkTimer=bossTimer(sharkTimer)
            powerTimer=power(powerTimer)
            powerUp(nextLevel,bx)
            game=checkLoss(game)
            if pause==1:
                game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer=pauseScreen(game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer)
            colourInd=colourIndex(colourInd)
            backgroundInd=backgroundIndex(backgroundInd)
            drawScene()

        if player == "squid":
            size=squid[W]*squid[H]    #Size of the fish
            if click== True and firstClick<2:
                firstClick+=1
            if firstClick==2 and pause!=1:
                moveSquid()
            createEnemy()
            if pause!=1:
                moveEnemy()
            enemyLimit()
            score+=scorer()
            sounds()
            bx+=level()
            levelAni(bx)
            bx,stage,nextLevel=levelUp(bx,stage)
            if stage==3:
                sharkComp=bossStatus(sharkComp)
            if stage==3 and sharkComp=="incomplete":
                for i in range(len(enemy)):
                    eRemove(i)
                if pause!=1:
                    boss()
                sharkTimer=bossTimer(sharkTimer)
            powerTimer=power(powerTimer)
            powerUp(nextLevel,bx)
            game=checkLoss(game)
            if pause==1:
                game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer=pauseScreen(game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer)
            colourInd=colourIndex(colourInd)
            backgroundInd=backgroundIndex(backgroundInd)
            drawScene()
        myClock.tick(25)
    if game=="end":
        end()
        yBones=bonesAni(yBones)
        game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer=gameover(game,score,bx,stage,firstClick,yBones,pause,sharkTimer,sharkComp,powerTimer)
       
    display.flip()
    click=False
           
quit()
