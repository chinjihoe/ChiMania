from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from sys import exit
from PIL import Image

texture = 0
imgScaling = [6.125, 3, 2.25, 2.4] #image scaling used for hitRating

#Create a cube using vertexes
def createCube(skin):
    global texture
    glBindTexture(GL_TEXTURE_2D, texture[skin])

    glBegin(GL_QUADS)
    # Top face (y = 1)
    glNormal(0, 1, 0)
    glTexCoord(0, 0); glVertex( 1, 1, -1)
    glTexCoord(1, 0); glVertex(-1, 1, -1)
    glTexCoord(1, 0.5); glVertex(-1, 1,  1)
    glTexCoord(0, 0.5); glVertex( 1, 1,  1)

    # Bottom face (y = -1)
    glNormal(0, -1, 0)
    glTexCoord(0,1); glVertex( 1, -1,  1) 
    glTexCoord(0,0); glVertex(-1, -1,  1)
    glTexCoord(1,0.5); glVertex(-1, -1, -1)
    glTexCoord(1,0.5); glVertex( 1, -1, -1)
    
    #Front face  (z = 1)
    glNormal3f(0, 0, 1)
    glTexCoord(0, 0.5); glVertex( 1,  1, 1) 
    glTexCoord(1, 0.5); glVertex(-1,  1, 1) 
    glTexCoord(1, 1); glVertex(-1, -1, 1)
    glTexCoord(0, 1); glVertex( 1, -1, 1)
    
    # Back face (z = -1)
    glNormal3f(0, 0, -1)
    glTexCoord(1,0.5); glVertex( 1, -1, -1) 
    glTexCoord(0,0.5); glVertex(-1, -1, -1)
    glTexCoord(0,0); glVertex(-1,  1, -1)
    glTexCoord(1,0); glVertex( 1,  1, -1)
    
    # Left face (x = -1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glBegin(GL_QUADS)


    glNormal(-1, 0, 0)
    glVertex(-1,  1,  1) 
    glVertex(-1,  1, -1)
    glVertex(-1, -1, -1)
    glVertex(-1, -1,  1)

    #Right face (x = 1)
    glNormal(1, 0, 0)
    glVertex(1,  1, -1) 
    glVertex(1,  1,  1)
    glVertex(1, -1,  1)
    glVertex(1, -1, -1)

    glEnd() 

def createHitLine():
    global texture
    glBindTexture(GL_TEXTURE_2D, texture[2]) 

    glBegin(GL_QUADS)
    # Top face (y = 1)
    glNormal(0, 1, 0)
    glTexCoord(0.1, 1/3); glVertex( 1, 1, -1)
    glTexCoord(0.9, 1/3); glVertex(-1, 1, -1)
    glTexCoord(0.9, 2/3); glVertex(-1, 1,  1)
    glTexCoord(0.1, 2/3); glVertex( 1, 1,  1)

    #Front face  (z = 1)
    glNormal3f(0, 0, 1)
    glTexCoord(0.1, 1/3); glVertex( 1,  1, 1) 
    glTexCoord(0.9, 1/3); glVertex(-1,  1, 1) 
    glTexCoord(0.9, 0.7); glVertex(-1, -1, 1)
    glTexCoord(0.1, 0.7); glVertex( 1, -1, 1)
    
    # Back face (z = -1)
    glNormal3f(0, 0, -1)
    glTexCoord(0.9,0.7); glVertex( 1, -1, -1) 
    glTexCoord(0.1,0.7); glVertex(-1, -1, -1)
    glTexCoord(0.1,0.5); glVertex(-1,  1, -1)
    glTexCoord(0.9,0.5); glVertex( 1,  1, -1)
    
    # Left face (x = -1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glBegin(GL_QUADS)

    glNormal(-1, 0, 0)
    glVertex(-1,  1,  1) 
    glVertex(-1,  1, -1)
    glVertex(-1, -1, -1)
    glVertex(-1, -1,  1)

    #Right face (x = 1)
    glNormal(1, 0, 0)
    glVertex(1,  1, -1) 
    glVertex(1,  1,  1)
    glVertex(1, -1,  1)
    glVertex(1, -1, -1)

    glEnd() 

def createDigits(digit, skin):
    skins = [3,13]
    w = 1
    if str(digit) is 'x':
            glBindTexture(GL_TEXTURE_2D, texture[23])
    elif str(digit) is ',':
            glBindTexture(GL_TEXTURE_2D, texture[28])
            w = 25/95
    elif str(digit) is '%':
        glBindTexture(GL_TEXTURE_2D, texture[29])
    else:
        glBindTexture(GL_TEXTURE_2D, texture[skins[skin]+digit])
        
    glBegin(GL_QUADS)
    glNormal(1, 0, 0)
    glTexCoord(0, 1); glVertex(0, 0, 0)
    glTexCoord(1, 1); glVertex(w, 0, 0)
    glTexCoord(1, 0); glVertex(w, 1, 0)
    glTexCoord(0, 0); glVertex(0, 1, 0)
    glEnd()

def createHitRating(hit):
    glBindTexture(GL_TEXTURE_2D, texture[24+hit])
    glBegin(GL_QUADS)
    glNormal(1, 0, 0)
    glTexCoord(0, 1); glVertex(0, 0, 0)
    glTexCoord(1, 1); glVertex(imgScaling[hit], 0, 0)
    glTexCoord(1, 0); glVertex(imgScaling[hit], 1, 0)
    glTexCoord(0, 0); glVertex(0, 1, 0)
    glEnd()    

def createGrade(grade):
    glBindTexture(GL_TEXTURE_2D, texture[30+grade])
    glBegin(GL_QUADS)
    glNormal(1, 0, 0)
    glTexCoord(0, 1); glVertex(0, 0, 0)
    glTexCoord(1, 1); glVertex(1, 0, 0)
    glTexCoord(1, 0); glVertex(1, 1, 0)
    glTexCoord(0, 0); glVertex(0, 1, 0)
    glEnd()  

def loadTextures():
    global texture
    imagePaths = [
        "./skins/mania-note1.png",
        "./skins/mania-note2.png",
        "./skins/scorebar-colour.png",
        "./skins/mn-0.png",
        "./skins/mn-1.png",
        "./skins/mn-2.png",
        "./skins/mn-3.png",
        "./skins/mn-4.png",
        "./skins/mn-5.png",
        "./skins/mn-6.png",
        "./skins/mn-7.png",
        "./skins/mn-8.png",
        "./skins/mn-9.png",
        "./skins/score-0.png",
        "./skins/score-1.png",
        "./skins/score-2.png",
        "./skins/score-3.png",
        "./skins/score-4.png",
        "./skins/score-5.png",
        "./skins/score-6.png",
        "./skins/score-7.png",
        "./skins/score-8.png",
        "./skins/score-9.png",
        "./skins/score-x.png",
        "./skins/mania-hit200.png",
        "./skins/mania-hit100.png",
        "./skins/mania-hit50.png",
        "./skins/mania-hit0.png",
        "./skins/score-comma.png",
        "./skins/score-percent.png",
        "./skins/ranking-D.png",
        "./skins/ranking-C.png",
        "./skins/ranking-B.png",
        "./skins/ranking-A.png",
        "./skins/ranking-S.png",
        "./skins/ranking-X.png",
    ]
    texture = glGenTextures(len(imagePaths)) #Maak ID's aan

    for x in range(len(imagePaths)):
        with Image.open(imagePaths[x]) as img:
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1) # voor plaatjes met oneven aantal pixels
            glBindTexture(GL_TEXTURE_2D, texture[x]) # gebruik de ID
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # specificeer hoe de textuur geschaald moet worden
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes()) # laad het plaatje
            glEnable(GL_TEXTURE_2D) # zet textuur aan
    