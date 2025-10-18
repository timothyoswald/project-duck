from cmu_graphics import *
from duck import *

def onAppStart(app):
    app.width = 800
    app.height = 600

def redrawAll(app):
    drawLabel("what the duck!", app.width / 2, app.height / 2 - 25, size = 60, 
              bold = True, fill = 'yellow', border = 'black')
    drawLabel("press space to play", app.width / 2, app.height / 2 + 25,
              size = 40, bold = True, fill = 'yellow', border = 'black')
    
def onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')

def main():
    runApp()

main()