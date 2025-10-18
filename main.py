from cmu_graphics import *
from char import Character
from terrain import Terrain
from duck import * 
import random

def start_onAppStart(app):
    app.width = 800
    app.height = 600

def start_redrawAll(app):
    drawLabel("what the duck!", app.width / 2, app.height / 2 - 25, size = 60, 
              bold = True, fill = 'yellow', border = 'black')
    drawLabel("press space to play", app.width / 2, app.height / 2 + 25,
              size = 40, bold = True, fill = 'yellow', border = 'black')
    
def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')

def game_onScreenActivate(app):
    app.char = Character(app.width / 2, 100)
    app.terrain = Terrain(app.width, app.height, 15, 18)
    app.frame = 0
    app.stepsPerSecond = 25
    app.spawningDucks = False
    app.ducksPerSecond = 100
    app.ducks = DuckFamily()
    app.steps = 0

def game_redrawAll(app):
    drawLabel(f"Duck Count: {len(app.char.ducksOnHead)}", app.width / 2, 25, 
              size = 25, bold = True)
    drawLabel("Run into Ducks to Collect Them!", app.width / 2, 75, 
              size = 25, bold = True)
    drawLabel("Press space to release collected ducks!", app.width / 2, 100, 
              size = 25, bold = True)
    if app.spawningDucks:
        drawLabel("Ducks are now spawning!", app.width / 2, 50, 
                  size = 25, bold = True)
    else:
        drawLabel("Press d for ducks!", app.width / 2, 50,
                  size = 25, bold = True)
    app.terrain.drawTerrain(app.frame)
    for duck in app.ducks.family[app.frame]:
        duck.draw()
    app.char.draw()

def game_onKeyPress(app, key):
    if key == 'up' and app.char.onGround:
        app.char.jump()
    elif key == 'd':
        app.spawningDucks = not app.spawningDucks
    elif key == 'space':
        app.char.releaseDuck(app)

def game_onKeyHold(app, keys):
    if 'left' in keys:
        app.char.move('left', app.terrain.blocks[app.frame])
        app.char.lastDir = 'left'
        app.char.isMoving = True
    elif 'right' in keys:
        app.char.move('right', app.terrain.blocks[app.frame])
        app.char.lastDir = 'right'
        app.char.isMoving = True

def game_onKeyRelease(app, key):
    if key == 'left' or key == 'right':
        app.char.isMoving = False

def game_onStep(app):
    app.steps += 1
    if app.char.isMoving:
        app.char.spriteIndex = (app.char.spriteIndex + 1) % 3
    for duck in app.ducks.family[app.frame]:
        if not duck.onCharHead:
            # update their state every once in a while
            if app.steps % 50 == 0:
                duck.state = random.choices([-1, -0.1, 0.1, 1], weights = [0.15, 0.35, 0.35, 0.15], k=1)[0]
            if duck.state != -0.1 and duck.state != 0.1:
                duck.spriteIndex = (duck.spriteIndex + 1) % 4
                duck.move(duck.state, app.terrain.blocks[app.frame])
    if (app.spawningDucks and 
        app.steps % (app.stepsPerSecond / app.ducksPerSecond) == 0):
        app.ducks.spawn(app.terrain, app.frame)
    if app.char.x + app.char.width < 0:
        app.frame -= 1
        if app.frame < 0:
            app.frame = 0
            app.terrain.makeTerrain(app.frame)
            app.ducks.newFrame(app.frame)
        app.char.x = app.width - app.char.width
        app.char.y = min(app.terrain.blocks[app.frame][-1][-1].y - app.char.height, app.char.y)
    elif app.char.x > app.width:
        app.frame += 1
        if app.frame > len(app.terrain.blocks) - 1:
            app.terrain.makeTerrain(app.frame)
            app.ducks.newFrame(app.frame)
        app.char.x = 0
        app.char.y = min(app.terrain.blocks[app.frame][0][-1].y - app.char.height, app.char.y)
    app.char.fall(app.terrain.blocks[app.frame])
    i = 0
    while i < len(app.ducks.family[app.frame]):
        duck = app.ducks.family[app.frame][i]
        if (duck.x + duck.width < 0 or duck.x > app.width):
            app.ducks.family[app.frame].pop(i)
        elif duck.touchesChar(app.char):
            app.char.ducksOnHead.append(app.ducks.family[app.frame].pop(i))
        else:
            i += 1
            duck.fall(app.terrain.blocks[app.frame])

def main():
    runAppWithScreens(initialScreen = 'start')

main()