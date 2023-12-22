#################################################
#  Rubik's cube Game - Main file
#################################################

from cmu_graphics import *
import rubiksCube as rubiks
import levels as levels

def onAppStart(app):
    rubiks.onAppStart(app)
    levels.onAppStart(app)
    app.margin = 70
    app.gameState = False
    app.img = "rubiks.png"

def onKeyPress(app, key):
    rubiks.onKeyPress(app, key)

def redrawAll(app):
    imageWidth, imageHeight = getImageSize(app.img)
    drawRect(0, 0, app.width, app.height, fill="black")
    if app.gameState == False:
        drawImage(app.img, 0, 0, width=imageWidth // 1.5, height=imageHeight // 1.5)
        drawLabel("WELCOME TO RUBIK'S CUBE GAME", app.width // 2, app.height // 6,
                  fill='white', bold=True, font='monospace', size=36)
        drawLabel("Click Start to Continue...", app.width // 2, app.height // 1.3,
                  fill='lightblue', font='monospace', size=20, bold=True)
        drawRect(app.width // 2 - 35, app.height - 70, 70, 40, fill="white")
        drawLabel("Start", app.width // 2, app.height - 50, fill="black",
                  font='monospace', bold=True, size=20)

    else:
        levels.redrawLevel(app)

def onMousePress(app, mouseX, mouseY):
    if ((app.width // 2 - 35) <= mouseX <= (app.width // 2 + 35)) and (
            (app.height - 70) <= mouseY <= (app.height - 30)):
        app.gameState = True
    levels.onMousePress(app, mouseX, mouseY)

def onStep(app):
    rubiks.onStep(app)

runApp(800, 800)
