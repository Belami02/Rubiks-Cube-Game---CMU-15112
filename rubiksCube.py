#################################################
# Rubik's cube game - Functions and features file
#################################################

from cmu_graphics import *
from PIL import Image as PilImage
import os
import random
import tempfile
import csv


class Button:
    def __init__(self, x, y, width, height, label=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height,
                 align="center", fill="lightgray",
                 border="black", borderWidth=2)
        drawLabel(self.label, self.x, self.y, size=15,
                  font='monospace', bold=True)

    def isClicked(self, mouseX, mouseY):
        return ((self.x - self.width // 2 <= mouseX <= self.x + self.width // 2)
                and (self.y - self.height // 2 <= mouseY <= self.y + self.height // 2))


def gameDimensions():
    # each face of the Rubik's cube is 3x3
    faceSize = 3
    cellSize = 30
    marginX = 80
    marginY = 150
    # the cube is spread in a cross pattern with 
    # a maximum width of 4 faces and height of 3
    cols = faceSize * 4
    rows = faceSize * 3
    return rows, cols, cellSize, marginX, marginY


def getFaceStart(faceIndex):
    # mapping assumes the following layout for the unfolded cube:
    #   0
    # 1 2 3 4
    #   5
    # where '0' is the top, '1' is the left,'2' is the front face,
    # '3' is the right, '4' is the back, '5' is the bottom
    mapping = {0: (0, 3),
               1: (3, 0),
               2: (3, 3),
               3: (3, 6),
               4: (3, 9),
               5: (6, 3)}

    return mapping.get(faceIndex, (None, None))


def onAppStart(app):
    app.scrambleBtn = Button(610, 230, 90, 50, label="Scramble")
    app.solveCubeBtn = Button(610, 290, 90, 50, label="Solve")
    app.dimension = Button(610, 350, 120, 50, label="Change View")
    app.reset = Button(610, 410, 90, 50, label='Reset')

    app.rotFrontClock = Button(50, 550, 50, 50, label='F')
    app.rotLeftClock = Button(110, 550, 50, 50, label='L')
    app.rotBottomClock = Button(170, 550, 50, 50, label='D')
    app.rotUpClock = Button(230, 550, 50, 50, label='U')
    app.rotRightClock = Button(290, 550, 50, 50, label='R')
    app.rotBackClock = Button(350, 550, 50, 50, label='B')
    app.rotMiddleClock = Button(410, 550, 50, 50, label='M')
    app.rotEquatorClock = Button(470, 550, 50, 50, label='E')

    app.rotFrontAntiClock = Button(50, 610, 50, 50, label="F'")
    app.rotLeftAntiClock = Button(110, 610, 50, 50, label="L'")
    app.rotBottomAntiClock = Button(170, 610, 50, 50, label="D'")
    app.rotUpAntiClock = Button(230, 610, 50, 50, label="U'")
    app.rotRightAntiClock = Button(290, 610, 50, 50, label="R'")
    app.rotBackAntiClock = Button(350, 610, 50, 50, label="B'")
    app.rotMiddleAntiClock = Button(410, 610, 50, 50, label="M'")
    app.rotEquatorAntiClock = Button(470, 610, 50, 50, label="E'")

    app.leftBtn = Button(570, 580, 70, 50, label="Left")
    app.rightBtn = Button(710, 580, 70, 50, label="Right")
    app.upBtn = Button(640, 530, 70, 50, label="Up")
    app.downBtn = Button(640, 630, 70, 50, label="Down")

    app.rows, app.cols, app.cellSize, app.marginX, app.marginY = gameDimensions()
    app.boardWidth = app.cols * app.cellSize
    app.boardHeight = app.rows * app.cellSize
    app.faceSize = 3
    app.cellBorderWidth = 1
    app.emptyColor = "white"
    app.color = "white"
    app.movesMade = 0
    app.image2 = 'rubiks6.png'
    app.image3 = 'rubiks4.png'
    app.image4 = 'rubiks8.png'
    app.image5 = 'leaderboard.png'
    app.image6 = 'menu.png'
    app.image7 = 'cancel.png'
    app.image8 = 'left.png'
    app.timerTicks = 0
    app.gameOver = False
    app.rubiksIsSolved = False
    app.timerRunning = False
    app.gameDim = False
    app.isSolving = False
    app.instructions = False
    app.displayScore = False
    app.boardState = 'color'
    app.movesLog = []  # keep the moves made
    app.initialBoard = [[app.emptyColor for col in range(app.cols)] for row in range(app.rows)]
    app.board = [[app.emptyColor for col in range(app.cols)] for row in range(app.rows)]
    colors = ["white", "orange", "blue", "red", "green", "yellow"]  # colors for each face
    for i in range(6):  # the colors for each face on the board
        faceRow, faceCol = getFaceStart(i)
        for row in range(faceRow, faceRow + 3):
            for col in range(faceCol, faceCol + 3):
                app.board[row][col] = colors[i]
                app.initialBoard[row][col] = colors[i]  # the initial state

    # added feature still under development
    # doesn't work for all functions like isometric cube(TRIAL MODE)
    app.faceImages = [
        loadAndSliceImage('barca.png', 3, 3, app.cellSize),
        loadAndSliceImage('psg.png', 3, 3, app.cellSize),
        loadAndSliceImage('manu.png', 3, 3, app.cellSize),
        loadAndSliceImage('mancity.png', 3, 3, app.cellSize),
        loadAndSliceImage('chelsea.png', 3, 3, app.cellSize),
        loadAndSliceImage('arsenal.png', 3, 3, app.cellSize),
    ]
    app.scores = readScores()


def readScores(filename='scores.csv'):  # reading the scores
    scores = []
    with open(filename) as file:
        for line in file:
            strippedLine = line.strip()
            scores.append(float(strippedLine))
    return scores


def writeScores(scores, filename='scores.csv'):  # updating the score function
    with open(filename, 'w') as file:
        for i in scores:
            file.write(str(i) + '\n')


def loadAndSliceImage(imagePath, rows, cols, faceSize):  # slicing the images
    try:
        image = PilImage.open(imagePath)
        image = image.resize((faceSize * cols, faceSize * rows))
        imageSlices = []
        for row in range(rows):
            for col in range(cols):
                left = col * faceSize
                top = row * faceSize
                right = left + faceSize
                bottom = top + faceSize
                slice = image.crop((left, top, right, bottom))
                imageSlices.append(slice)

        return imageSlices
    except IOError:
        print(f"Error: Unable to load the image at {imagePath}")
        return None


def drawImageSlice(app, imageSlice, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)  # converting row and column to pixel coordinates
    # save the image slice to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tempFile:
        imageSlice.save(tempFile, format='PNG')
        tempFilePath = tempFile.name

    try:
        drawImage(tempFilePath, cellLeft, cellTop, width=app.cellSize, height=app.cellSize)
    finally:
        # delete the temporary file
        os.remove(tempFilePath)

    borderWidth = 1
    borderColor = 'black'
    drawRect(cellLeft, cellTop, app.cellSize, app.cellSize,
             border=borderColor, borderWidth=borderWidth, fill=None)


def drawBackground(app):  # drawing the background of this main page
    drawRect(0, 0, app.width, app.height, fill="lightBlue")
    imageWidth1, imageHeight1 = getImageSize(app.image2)
    imageWidth2, imageHeight2 = getImageSize(app.image3)
    imageWidth3, imageHeight3 = getImageSize(app.image4)
    imageWidth4, imageHeight4 = getImageSize(app.image5)
    imageWidth5, imageHeight5 = getImageSize(app.image6)
    drawImage(app.image6, 140, 35, width=imageWidth5 // 16, height=imageHeight5 // 16)
    drawImage(app.image5, 80, 35, width=imageWidth4 // 18, height=imageHeight4 // 18)
    drawImage(app.image4, 20, 35, width=imageWidth3 // 10, height=imageHeight3 // 10)
    drawImage(app.image3, 620, 35, width=imageWidth2 // 9, height=imageHeight2 // 9)
    drawImage(app.image2, 700, 25, width=imageWidth1 // 6, height=imageHeight1 // 6)


def drawBorder(app):  # the border of the planar Rubik's Cube
    drawRect(app.marginX - 5, app.marginY - 5, app.boardWidth + 10,
             app.boardHeight + 10, fill="white", border='black', borderWidth=5)


def playRubiks():
    rows, cols, cellSize, marginX, marginY = gameDimensions()
    width = cols * cellSize + 2 * marginX
    height = rows * cellSize + 2 * marginY
    runApp(width=width, height=height)

def drawRubiksCube(app):  # the 2d Rubik's cube layout
    if app.boardState == 'image':
        for faceIndex in range(6):  # 6 faces for the cube
            faceRowStart, faceColStart = getFaceStart(faceIndex)
            for row in range(3):
                for col in range(3):
                    drawImageSlice(app, app.board[faceRowStart + row][faceColStart + col],
                                   faceRowStart + row, faceColStart + col)

    else:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell(app, row, col)


def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    if app.gameState == 'image':
        faceIndex, faceRow, faceCol = determineFaceAndPosition(row, col)
        imageSlice = app.faceImages[faceIndex][faceRow * 3 + faceCol]
        drawImageSlice(app, imageSlice, cellLeft, cellTop)
    else:
        color = app.board[row][col] if isPartOfFace(app, row, col) else app.emptyColor
        borderWidth = app.cellBorderWidth if isPartOfFace(app, row, col) else 0
        drawRect(cellLeft, cellTop, app.cellSize, app.cellSize,
                 fill=color, border="black", borderWidth=borderWidth)


def isPartOfFace(app, row, col):
    # Top face is from rows 0 to 2 and columns 3 to 5
    # Bottom face is from rows 6 to 8 and columns 3 to 5
    # Left face is from rows 3 to 5 and columns 0 to 2
    # Front face is from rows 3 to 5 and columns 3 to 5
    # Right face is from rows 3 to 5 and columns 6 to 8
    # Back face is from rows 3 to 5 and columns 9 to 11
    if ((0 <= row <= 2 and 3 <= col <= 5)
            or (6 <= row <= 8 and 3 <= col <= 5)
            or (3 <= row <= 5 and 0 <= col <= 2)
            or (3 <= row <= 5 and 3 <= col <= 5)
            or (3 <= row <= 5 and 6 <= col <= 8)
            or (3 <= row <= 5 and 9 <= col <= 11)):
        return True
    else:
        return False


def getCellLeftTop(app, row, col):
    cellLeft = app.marginX + col * app.cellSize
    cellTop = app.marginY + row * app.cellSize
    return cellLeft, cellTop


def rotateFrontFaceClockwise(app):  # rotating the front face 90 degrees clockwise
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    for r in range(3):
        for c in range(3):
            app.board[3 + r][3 + c] = frontFace[2 - c][r]

    if app.boardState == 'image':
        tempFrontFace = [[None for _ in range(3)] for _ in range(3)]

        # Copy the current front face to the temporary storage
        for r in range(3):
            for c in range(3):
                tempFrontFace[r][c] = app.board[3 + r][3 + c]

        # Rotate the front face clockwise
        for r in range(3):
            for c in range(3):
                app.board[3 + r][3 + c] = tempFrontFace[2 - c][r]

    topEdge = app.board[2][3:6]
    rightEdge = [app.board[3][6], app.board[4][6], app.board[5][6]]
    bottomEdge = app.board[6][3:6]
    leftEdge = [app.board[3][2], app.board[4][2], app.board[5][2]]

    # rotations
    app.board[2][3:6] = leftEdge[::-1]
    for i in range(3):
        app.board[i + 3][6] = topEdge[i]
    app.board[6][3:6] = rightEdge[::-1]
    for i in range(3):
        app.board[i + 3][2] = bottomEdge[i]


def rotateFrontFaceAntiClockwise(app):  # rotating the front face 90 degrees anti-clockwise
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    for r in range(3):
        for c in range(3):
            app.board[3 + r][3 + c] = frontFace[c][2 - r]

    topEdge = app.board[2][3:6]
    leftEdge = [app.board[3][2], app.board[4][2], app.board[5][2]]
    bottomEdge = app.board[6][3:6]
    rightEdge = [app.board[3][6], app.board[4][6], app.board[5][6]]

    # rotations
    for i in range(3):
        app.board[i + 3][2] = topEdge[2 - i]
    app.board[6][3:6] = leftEdge
    for i in range(3):
        app.board[i + 3][6] = bottomEdge[2 - i]
    app.board[2][3:6] = rightEdge


def rotateTopFaceClockwise(app):  # rotation of the top face 90 degrees clockwise
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    newTopFace = [
        [topFace[2][0], topFace[1][0], topFace[0][0]],
        [topFace[2][1], topFace[1][1], topFace[0][1]],
        [topFace[2][2], topFace[1][2], topFace[0][2]],
    ]
    for r in range(3):
        app.board[r][3:6] = newTopFace[r]

    frontEdge = app.board[3][3:6]
    leftEdge = app.board[3][0:3]
    backEdge = app.board[3][9:12]
    rightEdge = app.board[3][6:9]

    # rotations
    app.board[3][0:3] = frontEdge
    app.board[3][9:12] = leftEdge
    app.board[3][6:9] = backEdge
    app.board[3][3:6] = rightEdge


def rotateTopFaceAntiClockwise(app):  # rotation of the top face 90 degrees anti-clockwise
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    newTopFace = [
        [topFace[0][2], topFace[1][2], topFace[2][2]],
        [topFace[0][1], topFace[1][1], topFace[2][1]],
        [topFace[0][0], topFace[1][0], topFace[2][0]],
    ]
    for r in range(3):
        app.board[r][3:6] = newTopFace[r]

    frontEdge = app.board[3][3:6]
    rightEdge = app.board[3][6:9]
    backEdge = app.board[3][9:12]
    leftEdge = app.board[3][0:3]

    # rotations
    app.board[3][3:6] = leftEdge
    app.board[3][6:9] = frontEdge
    app.board[3][9:12] = rightEdge
    app.board[3][0:3] = backEdge


def rotateRightFaceClockwise(app):  # rotation of the right face 90 degrees clockwise
    rightFace = [app.board[r][6:9] for r in range(3, 6)]
    newRightFace = [
        [rightFace[2][0], rightFace[1][0], rightFace[0][0]],
        [rightFace[2][1], rightFace[1][1], rightFace[0][1]],
        [rightFace[2][2], rightFace[1][2], rightFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 3][6:9] = newRightFace[r]

    topEdge = [app.board[0][5], app.board[1][5], app.board[2][5]]
    frontEdge = [app.board[3][5], app.board[4][5], app.board[5][5]]
    backEdge = [app.board[3][9], app.board[4][9], app.board[5][9]]
    bottomEdge = [app.board[6][5], app.board[7][5], app.board[8][5]]

    # rotate the edges
    for i in range(3):
        app.board[i][5] = frontEdge[i]
        app.board[i + 3][9] = topEdge[2 - i]
        app.board[i + 6][5] = backEdge[2 - i]
        app.board[i + 3][5] = bottomEdge[i]


def rotateRightFaceAntiClockwise(app):  # rotating the right face 90 degrees anti-clockwise
    rightFace = [app.board[r][6:9] for r in range(3, 6)]
    newRightFace = [
        [rightFace[0][2], rightFace[1][2], rightFace[2][2]],
        [rightFace[0][1], rightFace[1][1], rightFace[2][1]],
        [rightFace[0][0], rightFace[1][0], rightFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 3][6:9] = newRightFace[r]

    # the edges that will be replaced
    topEdge = [app.board[0][5], app.board[1][5], app.board[2][5]]
    frontEdge = [app.board[3][5], app.board[4][5], app.board[5][5]]
    backEdge = [app.board[3][9], app.board[4][9], app.board[5][9]]
    bottomEdge = [app.board[6][5], app.board[7][5], app.board[8][5]]

    # rotate the edges
    for i in range(3):
        app.board[i + 3][5] = topEdge[i]
        app.board[i][5] = backEdge[2 - i]
        app.board[i + 6][5] = frontEdge[i]
        app.board[i + 3][9] = bottomEdge[2 - i]


def rotateBottomFaceClockwise(app):  # rotation of the bottom face 90 degrees clockwise
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]

    newBottomFace = [
        [bottomFace[2][0], bottomFace[1][0], bottomFace[0][0]],
        [bottomFace[2][1], bottomFace[1][1], bottomFace[0][1]],
        [bottomFace[2][2], bottomFace[1][2], bottomFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 6][3:6] = newBottomFace[r]

    # the edges
    frontEdge = app.board[5][3:6]
    rightEdge = app.board[5][6:9]
    backEdge = app.board[5][9:12]
    leftEdge = app.board[5][0:3]

    # rotation 
    app.board[5][6:9] = frontEdge
    app.board[5][9:12] = rightEdge
    app.board[5][0:3] = backEdge
    app.board[5][3:6] = leftEdge


def rotateBottomFaceAntiClockwise(app):  # rotating the bottom face 90 degrees anti-clockwise
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]

    newBottomFace = [
        [bottomFace[0][2], bottomFace[1][2], bottomFace[2][2]],
        [bottomFace[0][1], bottomFace[1][1], bottomFace[2][1]],
        [bottomFace[0][0], bottomFace[1][0], bottomFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 6][3:6] = newBottomFace[r]

    # the edges that will be replaced
    frontEdge = app.board[5][3:6]
    leftEdge = app.board[5][0:3]
    backEdge = app.board[5][9:12]
    rightEdge = app.board[5][6:9]

    # rotating the edges 
    app.board[5][6:9] = backEdge
    app.board[5][3:6] = rightEdge
    app.board[5][0:3] = frontEdge
    app.board[5][9:12] = leftEdge


def rotateLeftFaceClockwise(app):
    leftFace = [app.board[r][0:3] for r in range(3, 6)]

    newLeftFace = [
        [leftFace[2][0], leftFace[1][0], leftFace[0][0]],
        [leftFace[2][1], leftFace[1][1], leftFace[0][1]],
        [leftFace[2][2], leftFace[1][2], leftFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 3][0:3] = newLeftFace[r]

    # the edges
    frontEdge = [app.board[3][3], app.board[4][3], app.board[5][3]]
    bottomEdge = [app.board[6][3], app.board[7][3], app.board[8][3]]
    backEdge = [app.board[3][11], app.board[4][11], app.board[5][11]]
    topEdge = [app.board[0][3], app.board[1][3], app.board[2][3]]

    # rotations
    for i in range(3):
        app.board[6 + i][3] = frontEdge[i]
        app.board[3 + i][11] = bottomEdge[2 - i]
        app.board[i][3] = backEdge[2 - i]
        app.board[3 + i][3] = topEdge[i]


def rotateLeftFaceAntiClockwise(app):  # rotating the left face 90 degrees anti-clockwise
    leftFace = [app.board[r][0:3] for r in range(3, 6)]

    newLeftFace = [
        [leftFace[0][2], leftFace[1][2], leftFace[2][2]],
        [leftFace[0][1], leftFace[1][1], leftFace[2][1]],
        [leftFace[0][0], leftFace[1][0], leftFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 3][0:3] = newLeftFace[r]

    # the edges
    frontEdge = [app.board[3][3], app.board[4][3], app.board[5][3]]
    topEdge = [app.board[0][3], app.board[1][3], app.board[2][3]]
    backEdge = [app.board[3][11], app.board[4][11], app.board[5][11]]
    bottomEdge = [app.board[6][3], app.board[7][3], app.board[8][3]]

    # rotation
    for i in range(3):
        app.board[i][3] = frontEdge[i]
        app.board[3 + i][11] = topEdge[2 - i]
        app.board[6 + i][3] = backEdge[2 - i]
        app.board[3 + i][3] = bottomEdge[i]


def rotateBackFaceClockwise(app):  # rotation of the back face 90 degrees clockwise
    backFace = [app.board[r][9:12] for r in range(3, 6)]

    newBackFace = [
        [backFace[2][0], backFace[1][0], backFace[0][0]],
        [backFace[2][1], backFace[1][1], backFace[0][1]],
        [backFace[2][2], backFace[1][2], backFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 3][9:12] = newBackFace[r]

    # the edges
    topEdge = app.board[0][3:6]
    rightEdge = [app.board[3][8], app.board[4][8], app.board[5][8]]
    bottomEdge = app.board[8][3:6]
    leftEdge = [app.board[3][0], app.board[4][0], app.board[5][0]]

    # rotation 
    app.board[8][3:6] = leftEdge
    for i in range(3):
        app.board[i + 3][8] = bottomEdge[2 - i]
    app.board[0][3:6] = rightEdge
    for i in range(3):
        app.board[i + 3][0] = topEdge[2 - i]


def rotateBackFaceAntiClockwise(app):  # rotating the back face 90 degrees anti-clockwise
    backFace = [app.board[r][9:12] for r in range(3, 6)]

    newBackFace = [
        [backFace[0][2], backFace[1][2], backFace[2][2]],
        [backFace[0][1], backFace[1][1], backFace[2][1]],
        [backFace[0][0], backFace[1][0], backFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 3][9:12] = newBackFace[r]

    # the edges
    topEdge = app.board[0][3:6]
    leftEdge = [app.board[3][0], app.board[4][0], app.board[5][0]]
    bottomEdge = app.board[8][3:6]
    rightEdge = [app.board[3][8], app.board[4][8], app.board[5][8]]

    # rotations
    for i in range(3):
        app.board[i + 3][0] = bottomEdge[i]
    app.board[8][3:6] = rightEdge[::-1]
    for i in range(3):
        app.board[i + 3][8] = topEdge[i]
    app.board[0][3:6] = leftEdge[::-1]


def rotateEquatorClockwise(app):  # rotate the equator slice
    frontEdge = app.board[4][3:6]
    rightEdge = app.board[4][6:9]
    backEdge = app.board[4][9:12]
    leftEdge = app.board[4][0:3]

    # rotation
    app.board[4][6:9] = frontEdge
    app.board[4][9:12] = rightEdge
    app.board[4][0:3] = backEdge
    app.board[4][3:6] = leftEdge


def rotateEquatorAntiClockwise(app):  # rotate the equator slice anti-clockwise
    frontEdge = app.board[4][3:6]
    rightEdge = app.board[4][6:9]
    backEdge = app.board[4][9:12]
    leftEdge = app.board[4][0:3]

    # rotations
    app.board[4][0:3] = frontEdge
    app.board[4][3:6] = rightEdge
    app.board[4][6:9] = backEdge
    app.board[4][9:12] = leftEdge


def rotateMiddleClockwise(app):  # rotate the middle vertical slice
    bottomEdge = [app.board[i][4] for i in range(6, 9)]
    frontEdge = [app.board[i][4] for i in range(3, 6)]
    topEdge = [app.board[i][4] for i in range(0, 3)]
    backEdge = [app.board[i][10] for i in range(3, 6)]

    # rotations
    for i in range(3):
        app.board[i + 3][4] = bottomEdge[i]
        app.board[i][4] = frontEdge[i]
        app.board[i + 3][10] = topEdge[2 - i]
        app.board[6 + i][4] = backEdge[2 - i]


def rotateMiddleAntiClockwise(app):  # rotate the middle vertical slice anti-clockwise
    bottomEdge = [app.board[i][4] for i in range(6, 9)]
    frontEdge = [app.board[i][4] for i in range(3, 6)]
    topEdge = [app.board[i][4] for i in range(0, 3)]
    backEdge = [app.board[i][10] for i in range(3, 6)]

    # rotation
    for i in range(3):
        app.board[i + 3][4] = topEdge[i]
        app.board[6 + i][4] = frontEdge[i]
        app.board[i + 3][10] = bottomEdge[2 - i]
        app.board[i][4] = backEdge[2 - i]


def rotateCubeClockwise(app):  # rotate the cube clockwise
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    rightFace = [[app.board[r][c] for c in range(6, 9)] for r in range(3, 6)]
    backFace = [[app.board[r][c] for c in range(9, 12)] for r in range(3, 6)]
    leftFace = [[app.board[r][c] for c in range(0, 3)] for r in range(3, 6)]
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]

    # rotate side faces
    for r in range(3):
        for c in range(3):
            app.board[r + 3][c + 6] = frontFace[r][c]  # front to right
            app.board[r + 3][c + 9] = rightFace[r][c]  # right to back
            app.board[r + 3][c] = backFace[r][c]  # back to left
            app.board[r + 3][c + 3] = leftFace[r][c]  # left to front

    # rotate top and bottom faces
    newTopFace = [
        [topFace[0][2], topFace[1][2], topFace[2][2]],
        [topFace[0][1], topFace[1][1], topFace[2][1]],
        [topFace[0][0], topFace[1][0], topFace[2][0]],
    ]
    for r in range(3):
        app.board[r][3:6] = newTopFace[r]

    newBottomFace = [
        [bottomFace[2][0], bottomFace[1][0], bottomFace[0][0]],
        [bottomFace[2][1], bottomFace[1][1], bottomFace[0][1]],
        [bottomFace[2][2], bottomFace[1][2], bottomFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 6][3:6] = newBottomFace[r]


def rotateCubeAntiClockwise(app):  # rotate cube anticlockwise
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    rightFace = [[app.board[r][c] for c in range(6, 9)] for r in range(3, 6)]
    backFace = [[app.board[r][c] for c in range(9, 12)] for r in range(3, 6)]
    leftFace = [[app.board[r][c] for c in range(0, 3)] for r in range(3, 6)]
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]

    # rotate side faces
    for r in range(3):
        for c in range(3):
            app.board[r + 3][c + 3] = rightFace[r][c]  # right to front
            app.board[r + 3][c] = frontFace[r][c]  # front to left
            app.board[r + 3][c + 9] = leftFace[r][c]  # left to back
            app.board[r + 3][c + 6] = backFace[r][c]  # back to right

    # rotate top and bottom faces
    newTopFace = [
        [topFace[2][0], topFace[1][0], topFace[0][0]],
        [topFace[2][1], topFace[1][1], topFace[0][1]],
        [topFace[2][2], topFace[1][2], topFace[0][2]],
    ]
    for r in range(3):
        app.board[r][3:6] = newTopFace[r]

    newBottomFace = [
        [bottomFace[0][2], bottomFace[1][2], bottomFace[2][2]],
        [bottomFace[0][1], bottomFace[1][1], bottomFace[2][1]],
        [bottomFace[0][0], bottomFace[1][0], bottomFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 6][3:6] = newBottomFace[r]


def rotateCubeUp(app):  # rotate cube up
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    backFace = [[app.board[r][c] for c in range(9, 12)] for r in range(3, 6)]
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]
    rightFace = [[app.board[r][c] for c in range(6, 9)] for r in range(3, 6)]
    leftFace = [[app.board[r][c] for c in range(0, 3)] for r in range(3, 6)]

    # rotate the cube up by shifting the faces
    for r in range(3):
        for c in range(3):
            app.board[r + 3][c + 9] = topFace[2 - r][2 - c]  # top to back
            app.board[r + 6][c + 3] = backFace[2 - r][2 - c]  # back to bottom
            app.board[r + 3][c + 3] = bottomFace[r][c]  # bottom to front
            app.board[r][c + 3] = frontFace[r][c]  # front to top

    # rotate right and left faces
    newRightFace = [
        [rightFace[2][0], rightFace[1][0], rightFace[0][0]],
        [rightFace[2][1], rightFace[1][1], rightFace[0][1]],
        [rightFace[2][2], rightFace[1][2], rightFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 3][6:9] = newRightFace[r]

    newLeftFace = [
        [leftFace[0][2], leftFace[1][2], leftFace[2][2]],
        [leftFace[0][1], leftFace[1][1], leftFace[2][1]],
        [leftFace[0][0], leftFace[1][0], leftFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 3][0:3] = newLeftFace[r]


def rotateCubeDown(app):  # rotating the cube down
    frontFace = [[app.board[r][c] for c in range(3, 6)] for r in range(3, 6)]
    topFace = [app.board[r][3:6] for r in range(0, 3)]
    backFace = [[app.board[r][c] for c in range(9, 12)] for r in range(3, 6)]
    bottomFace = [app.board[r][3:6] for r in range(6, 9)]
    rightFace = [[app.board[r][c] for c in range(6, 9)] for r in range(3, 6)]
    leftFace = [[app.board[r][c] for c in range(0, 3)] for r in range(3, 6)]

    # rotate the cube down by shifting the faces
    for r in range(3):
        for c in range(3):
            app.board[r + 6][c + 3] = frontFace[r][c]  # front to bottom
            app.board[r + 3][c + 9] = bottomFace[2 - r][2 - c]  # bottom to back
            app.board[r][c + 3] = backFace[2 - r][2 - c]  # back to top
            app.board[r + 3][c + 3] = topFace[r][c]  # top to front

    # rotate right and left faces
    newRightFace = [
        [rightFace[0][2], rightFace[1][2], rightFace[2][2]],
        [rightFace[0][1], rightFace[1][1], rightFace[2][1]],
        [rightFace[0][0], rightFace[1][0], rightFace[2][0]],
    ]
    for r in range(3):
        app.board[r + 3][6:9] = newRightFace[r]

    newLeftFace = [
        [leftFace[2][0], leftFace[1][0], leftFace[0][0]],
        [leftFace[2][1], leftFace[1][1], leftFace[0][1]],
        [leftFace[2][2], leftFace[1][2], leftFace[0][2]],
    ]
    for r in range(3):
        app.board[r + 3][0:3] = newLeftFace[r]


def drawIsometricCube(app):  # the isometric view of the cube
    # Bottom Face 
    startX, startY = 230, 355
    horizOffset = 30
    vertOffset = 20
    for row in range(3):
        for col in range(3):
            topX = startX + (col - row) * horizOffset
            topY = startY + (row + col) * vertOffset
            drawPolygon(topX, topY, topX + horizOffset, topY + vertOffset,
                        topX, topY + 2 * vertOffset, topX - horizOffset,
                        topY + vertOffset, fill=app.board[8 - row][col + 3],
                        opacity=20, border='black')

    for startX, startY, stepY in [(70, 210, -20), (300, 150, +20)]:
        for i in range(3):
            for j in range(3):
                topX = startX + i * 30
                topY = startY + j * 40
                if startX == 70:  # Left Face 
                    drawPolygon(topX, topY, topX + 30,
                                topY - 20, topX + 30,
                                topY + 20, topX, topY + 40,
                                fill=app.board[j + 3][2 - i],
                                opacity=20, border="black")

                else:  # Back Face
                    drawPolygon(topX, topY, topX + 30,
                                topY + 20, topX + 30, topY + 60,
                                topX, topY + 40, fill=app.board[j + 3][11 - i],
                                opacity=20, border="black")
            startY += stepY

    # Top Face
    startX, startY = 230, 145
    horizOffset = 30
    vertOffset = 20
    for row in range(3):
        for col in range(3):
            topX = startX + (col - row) * horizOffset
            topY = startY + (row + col) * vertOffset

            drawPolygon(topX, topY, topX + horizOffset, topY + vertOffset,
                        topX, topY + 2 * vertOffset, topX - horizOffset,
                        topY + vertOffset, fill=app.board[row][col + 3],
                        border='black')

    for startX, startY, stepY in [(140, 205, 20), (230, 265, -20)]:
        for i in range(3):
            for j in range(3):
                topX = startX + i * 30
                topY = startY + j * 40

                if startX == 140:  # Front Face
                    drawPolygon(topX, topY, topX + 30,
                                topY + 20, topX + 30,
                                topY + 60, topX, topY + 40,
                                fill=app.board[j + 3][i + 3],
                                border="black")

                else:  # Right Face
                    drawPolygon(topX, topY, topX + 30,
                                topY - 20, topX + 30,
                                topY + 20, topX, topY + 40,
                                fill=app.board[j + 3][i + 6],
                                border="black")
            startY += stepY


def scrambleCube(app, numMoves):  # scrambling function
    moves = {
        rotateFrontFaceClockwise: "F",
        rotateFrontFaceAntiClockwise: "f",
        rotateTopFaceClockwise: "T",
        rotateTopFaceAntiClockwise: "t",
        rotateRightFaceClockwise: "R",
        rotateRightFaceAntiClockwise: "r",
        rotateBottomFaceClockwise: "B",
        rotateBottomFaceAntiClockwise: "b",
        rotateLeftFaceClockwise: "L",
        rotateLeftFaceAntiClockwise: "l",
        rotateBackFaceClockwise: "A",
        rotateBackFaceAntiClockwise: "a",
        rotateMiddleClockwise: "M",
        rotateMiddleAntiClockwise: "m",
        rotateEquatorClockwise: "E",
        rotateEquatorAntiClockwise: "e",
    }

    for i in range(numMoves):
        # select a random move function and execute it
        moveFunction = random.choice(list(moves.keys()))
        moveFunction(app)
        # finding the corresponding key
        key = moves[moveFunction]
        app.movesLog.append(key)

    app.movesMade = 0
    app.timerTicks = 0
    app.timerRunning = True


def checkIfSolved(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] != app.initialBoard[row][col]:
                return False
    app.timerRunning = False
    app.gameOver = True
    return True


def solveCube(app):
    app.solverIndex = len(app.movesLog) - 1
    app.isSolving = True


def redraw(app):
    drawBackground(app)
    formatTime(app)
    if app.boardState == 'color':
        app.scrambleBtn.draw()
        app.solveCubeBtn.draw()
        app.reset.draw()
        app.dimension.draw()

    if app.boardState == 'image':
        drawLabel("This "
                  "Feature "
                  "Is Under "
                  "Development", 625, 150,
                  font='monospace',
                  size=16,
                  fill='red',
                  bold=True)

    app.rotFrontClock.draw()
    app.rotLeftClock.draw()
    app.rotBottomClock.draw()
    app.rotUpClock.draw()
    app.rotRightClock.draw()
    app.rotBackClock.draw()
    app.rotMiddleClock.draw()
    app.rotEquatorClock.draw()

    app.rotFrontAntiClock.draw()
    app.rotLeftAntiClock.draw()
    app.rotBottomAntiClock.draw()
    app.rotUpAntiClock.draw()
    app.rotRightAntiClock.draw()
    app.rotBackAntiClock.draw()
    app.rotMiddleAntiClock.draw()
    app.rotEquatorAntiClock.draw()

    app.leftBtn.draw()
    app.rightBtn.draw()
    app.upBtn.draw()
    app.downBtn.draw()

    if app.gameDim == True:  # draw the isometric cube (3D view)
        drawIsometricCube(app)

    if app.gameDim == False:  # draw the regular Rubik's cube (2D view)
        drawBorder(app)
        drawRubiksCube(app)

    if app.instructions == True:
        displayInstructions(app)

    if app.displayScore == True:
        displayMaxScores(app)


def displayInstructions(app):  # menu pop-up function
    imageWidth6, imageHeight6 = getImageSize(app.image7)
    drawRect(90, 85, 600, 545, fill='lightGray', border='black', borderWidth=2)
    drawLabel("HELP", app.width / 2,
              100, font='monospace', size=25, bold=True)
    drawImage(app.image7, 650, 85, width=imageWidth6 // 16, height=imageHeight6 // 16)
    instruct1 = "***************#### BUTTONS ####**************"
    instruct2 = "***************# Clockwise Buttons #**************"
    instruct2a = "R: Right, L: left, F: Front, B: Back, U: Up"
    instruct2b = "D: Down, E: Equator, M: Middle"
    instruct3 = "***************# Anticlockwise Buttons #**************"
    instruct3a = "R': Right, L': left, F': Front, B': Back"
    instruct3b = "U': Up, D': Down, E': Equator, M': Middle"
    instruct4 = "***************# Other Buttons #**************"
    instruct4a = "Left arrow: rotates cube to the left"
    instruct4b = "Right arrow: rotates cube to the right"
    instruct4c = "Up arrow: rotates cube upwards"
    instruct4d = "Down arrow: rotates cube to downwards"
    instructions = [instruct1, " ", instruct2, instruct2a, instruct2b, " ",
                    instruct3, instruct3a, instruct3b, " ", instruct4,
                    instruct4a, instruct4b, instruct4c, instruct4d]
    y = 140
    for instr in instructions:
        drawLabel(f"{instr}", 130, y, fill="black", font='monospace',
                  bold=True, size=16, align="left")
        y += 30


def displayMaxScores(app):  # leader score function
    drawRect(50, 85, 200, 245, fill='lightGray', border='black', borderWidth=2)
    drawLabel("Leaderscores", 150,
              100, font='monospace', size=20, bold=True)
    y = 140
    i = 5
    for score in sorted(app.scores[:5], reverse=True):
        seconds = int(score) // 9  # 9 times per second
        minutes = seconds // 60
        seconds = seconds % 60
        drawLabel(f"{i}) {minutes:02d}:{seconds:02d}", 100, y, fill="black", font='monospace',
                  bold=True, size=16, align="left")
        y += 30
        i -= 1


def formatTime(app):
    seconds = app.timerTicks // 9  # 9 times per second
    minutes = seconds // 60
    seconds = seconds % 60
    if app.gameOver == True:
        drawLabel(f"TIME: {minutes:02d}:{seconds:02d}", app.width / 2, 50,
                  font='monospace', size=20, bold=True)
    else:
        drawRect(app.width / 2 - 150, 0, 300, 140, fill='white')
        drawLabel(f"Congratulations You Did It!", app.width / 2, 50,
                  size=20, fill="blue", font="monospace", bold=True)


def onKeyPress(app, key):
    if key == "T":
        rotateTopFaceClockwise(app)

    elif key == "t":
        rotateTopFaceAntiClockwise(app)

    elif key == "F":
        rotateFrontFaceClockwise(app)

    elif key == "f":
        rotateFrontFaceAntiClockwise(app)

    elif key == "R":
        rotateRightFaceClockwise(app)

    elif key == "r":
        rotateRightFaceAntiClockwise(app)

    elif key == "L":
        rotateLeftFaceClockwise(app)

    elif key == "l":
        rotateLeftFaceAntiClockwise(app)

    elif key == "B":
        rotateBottomFaceClockwise(app)

    elif key == "b":
        rotateBottomFaceAntiClockwise(app)

    elif key == "A":
        rotateBackFaceClockwise(app)

    elif key == "a":
        rotateBackFaceAntiClockwise(app)

    elif key == "E":
        rotateEquatorClockwise(app)

    elif key == "e":
        rotateEquatorAntiClockwise(app)

    elif key == "M":
        rotateMiddleClockwise(app)

    elif key == "m":
        rotateMiddleAntiClockwise(app)

    elif key == "right":
        rotateCubeClockwise(app)

    elif key == "left":
        rotateCubeAntiClockwise(app)

    elif key == "up":
        rotateCubeUp(app)

    elif key == "down":
        rotateCubeDown(app)

    if key in ['F', 'f', 'R', 'r', 'T', 't', 'L', 'l',
               'E', 'e', 'B', 'b', 'A', 'a', 'M', 'm',
               'up', 'down', 'left', 'right']:
        app.movesMade += 1
        app.movesLog.append(key)

    if key == 'space':
        solveCube(app)

    # Do not press this key unless in 2D planar view,
    # otherwise the code will crash
    # This part is still under development
    # Once pressed you can play with rotations
    # but the pictures are not correctly rotated
    if key == 'n':
        if app.boardState == 'color':
            app.boardState = 'image'
            for faceIndex in range(6):  # 6 faces for the cube
                faceRowStart, faceColStart = getFaceStart(faceIndex)
                faceImageSlices = app.faceImages[faceIndex]
                for row in range(3):
                    for col in range(3):
                        sliceIndex = row * 3 + col
                        app.initialBoard[faceRowStart + row][faceColStart + col] = faceImageSlices[sliceIndex]
                        app.board[faceRowStart + row][faceColStart + col] = faceImageSlices[sliceIndex]

        else:
            onAppStart(app)


def onStep(app):
    if app.timerRunning:
        app.timerTicks += 1

    if app.isSolving:
        if app.solverIndex >= 0:  # there are moves left to solve
            move = app.movesLog[app.solverIndex]
            if move == 'up':
                reverseMove = 'down'
            elif move == 'down':
                reverseMove = 'up'
            elif move == 'left':
                reverseMove = 'right'
            elif move == 'right':
                reverseMove = 'left'
            else:
                reverseMove = move.upper() if move.islower() else move.lower()
            onKeyPress(app, reverseMove)  # perform the move
            app.solverIndex -= 1  # move to the next move

        else:
            app.isSolving = False  # solving process is complete
            app.movesLog = []

    else:
        if checkIfSolved(app):
            app.rubiksIsSolved = True
            app.gameOver = True

            # if current time larger than ranking, add it in this place
            for i in range(len(app.scores)):
                if app.timerTicks > app.scores[0]:
                    app.scores.insert(0, app.timerTicks)
                    break

            # if not larger than anything, add to the end of the leaderboard
            else:
                app.scores.append(app.timerTicks)

            # updating the file
            writeScores(app.scores)


def onMousePress(app, mouseX, mouseY):
    imageWidth3, imageHeight3 = getImageSize(app.image4)
    imageWidth4, imageHeight4 = getImageSize(app.image5)
    imageWidth5, imageHeight5 = getImageSize(app.image6)
    imageWidth6, imageHeight6 = getImageSize(app.image7)
    if app.rotFrontClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "F")

    elif app.rotLeftClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "L")

    elif app.rotBottomClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "B")

    elif app.rotUpClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "T")

    elif app.rotRightClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "R")

    elif app.rotBackClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "A")

    elif app.rotMiddleClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "M")

    elif app.rotEquatorClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "E")

    elif app.rotFrontAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "f")

    elif app.rotLeftAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "l")

    elif app.rotBottomAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "b")

    elif app.rotUpAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "t")

    elif app.rotRightAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "r")

    elif app.rotBackAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "a")

    elif app.rotMiddleAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "m")

    elif app.rotEquatorAntiClock.isClicked(mouseX, mouseY):
        onKeyPress(app, "e")

    elif app.leftBtn.isClicked(mouseX, mouseY):
        onKeyPress(app, "left")

    elif app.rightBtn.isClicked(mouseX, mouseY):
        onKeyPress(app, "right")

    elif app.upBtn.isClicked(mouseX, mouseY):
        onKeyPress(app, "up")

    elif app.downBtn.isClicked(mouseX, mouseY):
        onKeyPress(app, "down")

    if app.scrambleBtn.isClicked(mouseX, mouseY):
        app.rubiksGame = False
        app.levelState = False
        for level in app.levels:
            if app.levels[level].isClicked(mouseX, mouseY):
                if level == "easy":
                    rubiks.scrambleCube(app, 20)
                elif level == "medium":
                    rubiks.scrambleCube(app, 50)
                elif level == "hard":
                    rubiks.scrambleCube(app, 100)
                app.rubiksGame = True
                app.levelState = True

    if ((20 <= mouseX <= imageWidth3 // 10 + 20)
            and (35 <= mouseY <= imageHeight3 // 10 + 35)):
        app.gameState = False

    if ((80 <= mouseX <= imageWidth4 // 10 + 80)
            and (35 <= mouseY <= imageHeight4 // 10 + 35)):
        if app.displayScore == False:
            app.displayScore = True
        else:
            app.displayScore = False

    if ((140 <= mouseX <= imageWidth5 // 10 + 140)
            and (35 <= mouseY <= imageHeight5 // 25 + 35)):
        app.instructions = True

    if (app.reset.isClicked(mouseX, mouseY) or
            ((650 <= mouseX <= imageWidth6 // 10 + 650)
             and (85 <= mouseY <= imageHeight6 // 25 + 85))):
        onAppStart(app)

    if app.solveCubeBtn.isClicked(mouseX, mouseY):
        solveCube(app)

    if app.dimension.isClicked(mouseX, mouseY):
        app.gameDim = not app.gameDim
