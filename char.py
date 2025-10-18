from cmu_graphics import *
from helper import getIMGpath

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.vy = 0
        self.jumpPower = 10
        self.gravity = 1
        self.onGround = False
        self.stillRight = getIMGpath("rightstill.png")
        self.stillLeft = getIMGpath("leftstill.png")
        self.spriteIndex = 0
        self.moveRightSprites = [getIMGpath("right1.png"),
                                 getIMGpath("right2.png"),
                                 getIMGpath("right3.png")]
        self.moveLeftSprites = [getIMGpath("left1.png"),
                                getIMGpath("left2.png"),
                                getIMGpath("left3.png")]
        self.width, self.height = getImageSize(self.stillRight)
        self.ducksOnHead = []
        self.lastDir = 'right'
        self.isMoving = False

    def draw(self):
        if self.isMoving:
            if self.lastDir == 'right':
                drawImage(self.moveRightSprites[self.spriteIndex], 
                          self.x, self.y, width = self.width, 
                          height = self.height, visible = True)
            else:
                drawImage(self.moveLeftSprites[self.spriteIndex], 
                          self.x, self.y, width = self.width, 
                          height = self.height, visible = True)
        else:
            if self.lastDir == 'right':
                drawImage(self.stillRight, 
                          self.x, self.y, width = self.width, 
                          height = self.height, visible = True)
            else:
                drawImage(self.stillLeft, 
                          self.x, self.y, width = self.width, 
                          height = self.height, visible = True)
        for i in range(len(self.ducksOnHead)):
            duck = self.ducksOnHead[i]
            drawImage(duck.sleeping, self.x, self.y - self.width / 2 - self.width * i / 6 , width = self.width, height = self.width / 2)

    def move(self, dir, terrain):
        dx = -self.speed if dir == 'left' else self.speed
        self.x += dx
        for col in terrain:
            for block in col:
                if self.intersects(block):
                    if dir == 'left':
                        self.x = block.x + block.width
                    else:
                        self.x = block.x - self.width
                    return

    def fall(self, terrain):
        self.vy += self.gravity
        self.y += self.vy
        for col in terrain:
            for block in col:
                if self.intersects(block):
                    if self.vy > 0:
                        self.y = block.y - self.height
                        self.vy = 0
                        self.onGround = True
                    elif self.vy < 0:
                        self.y = block.y + block.height
                        self.vy = 0
                    return
        self.onGround = False

    def jump(self):
        if self.onGround:
            self.vy = -self.jumpPower
            self.onGround = False
    
    def releaseDuck(self, app):
        if self.ducksOnHead != []:
            duck = self.ducksOnHead.pop()
            duck.x = self.x
            duck.x += 3 * self.width if self.lastDir == 'right' else -3 * self.width
            duck.y = min(self.y, Character.getColHeight(app, duck.x) - duck.height)
            app.ducks.family[app.frame].append(duck)

    @staticmethod
    def getColHeight(app, x):
        colWidth = app.terrain.screenWidth / app.terrain.cols
        col = int(x // colWidth)
        if col >= app.terrain.cols:
            col = app.terrain.cols - 1
        return app.terrain.blocks[app.frame][col][-1].y
    
    def intersects(self, block):
        return ((self.x + self.width > block.x) and 
                (self.x < block.x + block.width) and
                (self.y + self.height > block.y) and 
                (block.y + block.height > self.y))