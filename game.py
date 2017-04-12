import beatmap as bm
import game_objects as gob

import numpy
from sys import exit
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *
from PIL import Image

songLoaded = False
songPlaying = False
songStartTime = 0

#Variables to calculate delta frame time
prevFrameTime = 0
frameTime = 1000/60 #fps

beatmap = [] #Spawn times of the blocks

#Variables to calculate block positions based on frame time
prevBlockTime = 0
deltaDistance = 0
speed = 1.5 #The travel speed of the blocks
beginPoint = -30 #Spawn point of the blocks
endPoint = 9 #Despawn point of the blocks
blockPositions = [[],[],[],[]] #The current positions of the active blocks on each lane
blockPos = [-3.6,-1.2,1.2,3.6] #The positions of the 4 different lanes
blocksOnField = 0 #Total active blocks

gameEnded = False
score = 0 #score += hitsScore * combo
hitPercentage = 100.00 
grades = ["D","C","B","A","S","S+"]
combo = 0
maxCombo = 0
totalHits = 0
hitNaming = ["Excellent", "Good", "Bad", "Miss"]
hitScore = [200,100,50,0]
hits = [0,0,0,0] #Total count of Excellent,Good,Bad,Miss
lastHit = 0

##Object drawing

#This function is used to cap the framerate at 60 fps
def animate():
    global prevFrameTime
    if glutGet(GLUT_ELAPSED_TIME) - prevFrameTime >= frameTime:
        prevFrameTime = glutGet(GLUT_ELAPSED_TIME)
        glutPostRedisplay()

#The callback to draw all objects
def display():
    gameMechanics()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawGrade()
    drawCombo()
    drawScore()
    drawHitRating()
    drawHitPercentage()
    drawHitLine()
    drawLanes()

    #Only draw blocks when there are active blocks
    if blocksOnField > 0:
        drawBlocks()

    glutSwapBuffers()

#The line to indicate when to hit the blocks
def drawHitLine():
    glColor(1,1,1)
    glPushMatrix()
    glScalef(4, 0.1, 0.1)
    glTranslate(0,0,endPoint+18)
    gob.createHitLine()
    glPopMatrix()

#Draw a dark red rectangle to indicate the path of the blocks
def drawLanes():
    glPushMatrix()
    glBegin(GL_POLYGON)
    glColor(0.7,0.7,0.7)

    glVertex3f(-5, -1, 2.5)
    glVertex3f(5, -1, 2.5)
    glVertex3f(5, -1, -39)
    glVertex3f(-5, -1, -39)

    glEnd()
    glPopMatrix()

#Draw a counter of the players current combo
def drawCombo():
    glDisable(GL_LIGHTING)

    glColor(1,1,1)
    for x in range(len(str(combo))):
        glPushMatrix()
        glTranslate(5.5+x,0,-11)
        glRotate(-30,1,0,0)
        gob.createDigits(int(str(combo)[x]),1)
        glPopMatrix()

    glPushMatrix()
    glTranslate(5.5+len(str(combo)),0,-11)
    glRotate(-30,1,0,0)
    gob.createDigits('x',1)
    glPopMatrix()
    glEnable(GL_LIGHTING)

#Draw the current score count of the player
def drawScore():
    glDisable(GL_LIGHTING)

    glColor(1,1,1)
    for x in range(len(str(score))):
        glPushMatrix()
        glScalef(1.5, 1.5, 1)
        glTranslate(-8+x,0.5,-13)
        glRotate(-30,1,0,0)
        gob.createDigits(int(str(score)[x]),1)
        glPopMatrix()
    glEnable(GL_LIGHTING)

#Draw the hitRating of the last hit or missed block
def drawHitRating():
    glDisable(GL_LIGHTING)
    scale = [6.125, 3, 2.25, 2.4] #The scaling of the hitRating textures
    glColor(1,1,1)
    glPushMatrix()
    glTranslate(0-scale[lastHit]/(2/0.7),-1,3.5) #Position the texture in the center
    glRotate(-90,1,0,0)
    glScalef(0.7,0.7,0)
    gob.createHitRating(lastHit)
    glPopMatrix()
    glEnable(GL_LIGHTING)

#Draw the current hitPercentage
def drawHitPercentage():
    #Parse hitPercentage to string and remove the '.' to draw the numbers separately
    percentage = str(hitPercentage).split('.')[0]+str(hitPercentage).split('.')[1][:2]
    #Add an zero is hitPercentage == 100.0
    if percentage != "1000":
        for x in range(4-len(percentage)):
            percentage += "0"
    else:
        percentage += "0"
        
    #Draw the numbers
    glDisable(GL_LIGHTING)
    glColor(1,1,1)
    for x in range(len(percentage)):
        glPushMatrix()
        X = x
        if X >= len(percentage)-2:
            X += 0.5
        glScalef(1.5, 1.5, 1)
        glTranslate(4+X,0.5,-13)
        glRotate(-30,1,0,0)
        gob.createDigits(int(percentage[x]),1)
        glPopMatrix()

    #Draw the comma between the numbers
    glPushMatrix()
    glScalef(1.5, 1.5, 1)
    glTranslate(4+len(percentage)-2,0.5,-13)
    glRotate(-30,1,0,0)
    gob.createDigits(',',1)
    glPopMatrix()

    #Draw the '%' symbol after the numbers
    glPushMatrix()
    glScalef(1.5, 1.5, 1)
    glTranslate(4+len(percentage)+0.5,0.5,-13)
    glRotate(-30,1,0,0)
    gob.createDigits('%',1)
    glPopMatrix()
    
    glEnable(GL_LIGHTING)

#Draw the blocks
def drawBlocks():
    glColor(1,1,1)

    blockSkinIndex = [0,1,1,0]
    for lane in range(len(blockPositions)):
        for x in range(len(blockPositions[lane])):
            glPushMatrix()
            glScalef(0.8, 0.2, 0.3)
            glTranslate(blockPos[lane],0,blockPositions[lane][x])
            gob.createCube(blockSkinIndex[lane])
            glPopMatrix()

#Draw the current Grade of the player based on the current hitPercentage
def drawGrade():
    glColor(1,1,1)

    glDisable(GL_LIGHTING)

    glPushMatrix()
    glTranslate(3,1.5,0)
    glRotate(-30,1,0,0)
    gob.createGrade(calculateGrade())
    glPopMatrix()

    glEnable(GL_LIGHTING)


##The game

def gameMechanics():
    spawnFromBeatmap()
    calculateBlockPosition()
    scroller()
    gameEnd()

#Calculate the new positions of the blocks based on the passed frame time
def calculateBlockPosition():
    global prevBlockTime, speed, deltaDistance

    now = glutGet(GLUT_ELAPSED_TIME)
    passedTime = now - prevBlockTime
    prevBlockTime = glutGet(GLUT_ELAPSED_TIME)

    deltaDistance = (speed * 39) * (passedTime/1000) #The value to be added to the previous block positions
    
#Increase all block positions with the deltaDistance
def scroller():
    global blockPositions, blocksOnField, combo, hits, lastHit, hitPercentage

    popPositions = [[],[],[],[]] #The positions of the blocks that need to be deleted from the blockPositions list
    for lane in range(len(blockPositions)):
        for x in range(len(blockPositions[lane])):
            blockPositions[lane][x] += deltaDistance

            #Add the block to popPositions if the block has gone beyond the point of "missing"
            if blockPositions[lane][x] >= (endPoint + 5):
                popPositions[lane].append(x)
                blocksOnField -= 1
                combo = 0 #Reset the combo to 0 because of missing the block
                hits[3] += 1
                lastHit = 3
                hitPercentage = (hits[0]*100 + hits[1]*1/3 + hits[2]*1/6)/(hits[0]+hits[1]+hits[2]+hits[3]) #calculate new hitPercentage

                print("Miss Combo:", combo)

    #Pop blocks in blockPositions using the popPositions
    for lane in range(len(popPositions)):
        for x in range(len(popPositions[lane])):
            blockPositions[lane].pop(0)

#Append block to blockPositions if the it's time to spawn a block
#The spawnTimes of the blocks are in the list: beatmap
def spawnFromBeatmap():
    if len(beatmap) > 0:
        if glutGet(GLUT_ELAPSED_TIME) < int(beatmap[0][1]):
            return
        else:
            popPositions = []
            for x in range(len(beatmap)):
                if glutGet(GLUT_ELAPSED_TIME) >= int(beatmap[x][1]):
                    spawnBlock(int(beatmap[x][0]))
                    popPositions.append(x)
                else:
                    break
            for x in range(len(popPositions)): #Remove the spawn time from the beatmap list if the block has been spawned
                beatmap.pop(0)

#Append block the blockPositions
def spawnBlock(lane):
    global blocksOnField
    blocksOnField += 1

    if lane is 0:
        blockPositions[0].append(beginPoint)
    elif lane is 1:
        blockPositions[1].append(beginPoint)
    elif lane is 2:
        blockPositions[2].append(beginPoint)
    elif lane is 3:
        blockPositions[3].append(beginPoint)

#Play the song of the chosen beatmap
def startSong():
    global songPlaying, beatmap, songStartTime, songLoaded
    if not songLoaded: 
        beatmap, audioFile = bm.loadBeatmap()
        pygame.mixer_music.load('./songs/'+audioFile)
        songStartTime = glutGet(GLUT_ELAPSED_TIME)
        print("SongStartTime:",songStartTime)
        songLoaded = True

    if not songPlaying:
        delay = 2000
        for x in range(len(beatmap)):
                beatmap[x][1] = int(beatmap[x][1]) + songStartTime + delay +350
        glutTimerFunc(int(1/speed*1000)+delay, pygame.mixer_music.play, 1)
        songPlaying = True

#This function is called when the song has ended
def gameEnd():
    global gameEnded
    #Print the score and hits of the player
    if not gameEnded and len(blockPositions[0]) + len(blockPositions[1]) + len(blockPositions[2]) + len(blockPositions[3]) is 0 and len(beatmap) is 0:
        print("Game results:\nMax combo:",maxCombo,"TotalHits:",totalHits)
        for x in range(4):
            print(hitNaming[x],hits[x])
        print("Grade:",grades[calculateGrade()])
        gameEnded = True

#Calculate the grade using the current hitPercentage
def calculateGrade():
    if hitPercentage < 70:
        return 0
    elif hitPercentage < 80:
        return 1
    elif hitPercentage < 90:
        return 2
    elif hitPercentage < 95:
        return 3
    elif hitPercentage < 100:
        return 4
    else:
        return 5
    
##User input

#The callback to handle keyboard input
def controls(key, x, y):
    if key == b"\x1b": #ESC
        exit()

    elif blocksOnField > 0:
        if key == b's':
            hitDetection(0)
        if key == b'd':
            hitDetection(1)
        if key == b'k':
            hitDetection(2)
        if key == b'l':
            hitDetection(3)

#This function determines if the user has hit a block
def hitDetection(key):
    global combo, blocksOnField, totalHits, hits, maxCombo, score, lastHit, hitPercentage
    if len(blockPositions[key]) > 0 and abs(blockPositions[key][0] - endPoint) <= 10:
        pos = blockPositions[key][0] - endPoint
        hitRate = int(abs(pos/2.5))
        hits[hitRate] += 1
        blocksOnField -= 1
        blockPositions[key].pop(0)
        lastHit = hitRate
        if hitRate == 3:
            combo = 0
        else:
            combo += 1
            totalHits += 1
            if combo > maxCombo:
                maxCombo = combo

            score += combo * hitScore[hitRate]
        hitPercentage = (hits[0]*100 + hits[1]*1/3 + hits[2]*1/6)/(hits[0]+hits[1]+hits[2]+hits[3])
        print(hitNaming[hitRate],"Combo:",combo,"Score:",score)

##OpenGL settings
glutInit()
pygame.init() #init pygame to play a song
startSong()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)
glutCreateWindow("Perspective view".encode("ascii"))
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
glEnable(GL_LINE_SMOOTH)
glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION) 
gluPerspective(80, (640/480), 1,20)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, 4, 4, 0, 0, 0, 0, 1, 0)


glEnable(GL_LIGHTING)
glEnable(GL_RESCALE_NORMAL) #Fix the lighting of scaled objects
glEnable(GL_LIGHT0) # Create light source
glEnable(GL_COLOR_MATERIAL)
glLight(GL_LIGHT0, GL_POSITION, [0, 5, 1.5]) #Position light source
glLight(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1]) #Diffuse light at 1,1,1


glutDisplayFunc(display)
glutKeyboardFunc(controls)
glutIdleFunc(animate)

gob.loadTextures() #Load textures of the objects

glutMainLoop()
