from PIL import Image as PilImage  # Import with an alias to avoid conflicts
import os
from cmu_graphics import *


def loadAndSliceImage(app, imagePath):
    # Check if the image file exists
    if not os.path.exists(imagePath):
        raise FileNotFoundError(f"The file {imagePath} does not exist.")

    # Open the image using the alias
    image = PilImage.open(imagePath)
    image = image.resize((app.boardWidth, app.boardHeight))  # Resize the image to fit the board
    app.slicedImages = []

    # Calculate the width and height of each cell
    cellWidth, cellHeight = getCellSize(app)

    # Slice the image into smaller pieces
    for row in range(app.rows):
        for col in range(app.cols):
            left = col * cellWidth
            top = row * cellHeight
            right = left + cellWidth
            bottom = top + cellHeight
            sliced = image.crop((left, top, right, bottom))
            app.slicedImages.append(sliced)  # Store PIL image slices

    if app.slicedImages:
        app.slicedImages[0], app.slicedImages[-1] = app.slicedImages[-1], app.slicedImages[0]
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)


def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    imageIndex = row * app.cols + col
    sliced = app.slicedImages[imageIndex]


    drawRect(cellLeft, cellTop, cellWidth, cellHeight, border='black', borderWidth=app.cellBorderWidth)


    tempImagePath = f'temp_slice_{imageIndex}.png'
    sliced.save(tempImagePath)


    drawImage(tempImagePath, cellLeft + app.cellBorderWidth, cellTop + app.cellBorderWidth,
              width=cellWidth - 2 * app.cellBorderWidth, height=cellHeight - 2 * app.cellBorderWidth)


def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def onAppStart(app):
    app.rows = 3
    app.cols = 3
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2

    # Load and slice the image
    loadAndSliceImage(app, 'mancity.png')


def redrawAll(app):
    # Draw a specific cell as an example
    # drawBoard(app)
    drawCell(app, 0,0)
    drawCell(app, 0, 2)
    drawCell(app, 1, 1)


def main():
    runApp(400, 400)  # Set the window size if needed


main()
