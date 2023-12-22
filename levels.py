#################################################
# Rubik's cube Game - Level's page
#################################################

from cmu_graphics import *
import rubiksCube as rubiks

class Button:
    def __init__(self, x, y, width, height, color, label=None):
        self.width = width
        self.height = height
        self.label = label
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        # draws button background
        drawRect(self.x, self.y, self.width, self.height,
                 align="center", fill=self.color, border="blue")
        if self.label:
            drawLabel(self.label, self.x, self.y,
                      font='fantasy', bold=True, size=50)
    def isClicked(self, x, y):
        return (self.x - self.width // 2 <= x <= self.x + self.width // 2
                and self.y - self.height // 2 <= y <= self.y + self.height // 2)

def createLevelsPage(app):
    app.levels = {"easy": Button(400, 150, 300,
                                 100, "red", label="Easy"),
                  "medium": Button(400, 350, 300,
                                   100, "orange", label="Medium"),
                  "hard": Button(400, 550, 300,
                                 100, "yellow", label="Hard")}

def onAppStart(app):
    app.image = 'rubiks2.png'
    app.rubiksGame = False
    app.levelState = False
    createLevelsPage(app)

def onMousePress(app, mouseX, mouseY):
    if app.levelState == False:
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
    rubiks.onMousePress(app, mouseX, mouseY)

def redrawLevel(app):
    imageWidth, imageHeight = getImageSize(app.image)
    if app.rubiksGame == False:
        drawImage(app.image, 0, app.height // 8,
                  width=imageWidth * 2, height=imageHeight * 2)
        drawLabel("SELECT THE LEVEL", 400, 50,
                  size=24, font='fantasy', fill="white")
        for level in app.levels:
            app.levels[level].draw()
    else:
        rubiks.redraw(app)
