from cmu_graphics import *
import rubiksCube as rubiks

def onAppStart(app):
    rubiks.onAppStart(app)

def drawIsometricCube(app): 
    ###### Bottom Face ######
    startX, startY = 230, 355
    # offsets for horizontal and vertical steps
    horizOffset = 30  # horizontal step size
    vertOffset = 20   # vertical step size
    
    for row in range(3):
        for col in range(3):
            # dimensions of the top point of the current polygon
            topX = startX + (col - row) * horizOffset
            topY = startY + (row + col) * vertOffset

            drawPolygon(
                topX, topY, 
                topX + horizOffset, topY + vertOffset, 
                topX, topY + 2 * vertOffset, 
                topX - horizOffset, topY + vertOffset,
                fill= rubiks.app.board[8 - row][col + 3], opacity = 20, border='black'
            )
            
            
    for startX, startY, stepY in [(70, 210, -20), (300, 150, +20)]:
        for i in range(3):
            for j in range(3):
                topX = startX + i * 30
                topY = startY + j * 40
                ###### Left Face ######
                if startX == 70:
                    drawPolygon(
                        topX, topY,
                        topX + 30, topY - 20,
                        topX + 30, topY + 20,
                        topX, topY + 40,
                        fill= rubiks.app.board[j+3][2-i], opacity = 20,  border="black"
                    )
                    
                ###### Back Face ######
                else:
                    drawPolygon(
                        topX, topY,
                        topX + 30, topY + 20,
                        topX + 30, topY + 60,
                        topX, topY + 40,
                        fill= rubiks.app.board[j+3][11-i], opacity = 20, border="black"
                    )
            startY += stepY
            
    ###### Top Face ######
    startX, startY = 230, 145

    # offsets for horizontal and vertical steps
    horizOffset = 30  # horizontal step size
    vertOffset = 20   # vertical step size
    
    for row in range(3):
        for col in range(3):
            # dimensions of the top point of the current polygon
            topX = startX + (col - row) * horizOffset
            topY = startY + (row + col) * vertOffset

            drawPolygon(
                topX, topY, 
                topX + horizOffset, topY + vertOffset, 
                topX, topY + 2 * vertOffset, 
                topX - horizOffset, topY + vertOffset,
                fill= rubiks.app.board[row][col + 3], border='black'
            )
    
    for startX, startY, stepY in [(140, 205, 20), (230, 265, -20)]:
        for i in range(3):
            for j in range(3):
                topX = startX + i * 30
                topY = startY + j * 40
                ###### Front Face ######
                if startX == 140:
                    drawPolygon(
                        topX, topY,
                        topX + 30, topY + 20,
                        topX + 30, topY + 60,
                        topX, topY + 40,
                        fill= rubiks.app.board[j+3][i+3], border="black"
                    )
                ###### Right Face ######
                else:
                    drawPolygon(
                        topX, topY,
                        topX + 30, topY - 20,
                        topX + 30, topY + 20,
                        topX, topY + 40,
                        fill= rubiks.app.board[j+3][i+6], border="black"
                    )
            startY += stepY
            
def solveCube(app):
    rubiks.solveCube(app)

def onKeyPress(app, key):
    rubiks.onKeyPress(app, key)
    
def redrawCube(app):
    drawIsometricCube(app)


