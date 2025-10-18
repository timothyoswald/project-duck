from cmu_graphics import *
import random

class Duck():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 2
        self.vy = 0
        self.gravity = 1
        self.jumpPower = 10
        self.spriteIndex = 0
        self.stillRightSprites = ["Images/duckstand1_good.png",
                                  r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand2_good.png",
                                  r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand3_good.png",
                                  r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand4_good.png"]
        self.stillLeftSprites = [r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand1_goodopp.png",
                                 r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand2_goodopp.png",
                                 r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand3_goodopp.png",
                                 r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckstand4_goodopp.png"]
        self.moveLeftSprites = [r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove1_good.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove2_good.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove3_good.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove4_good.png"]
        self.moveRightSprites = [r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove1_goodopp.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove2_goodopp.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove3_goodopp.png",
                            r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\duckmove4_goodopp.png"]
        self.sleeping = r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\sleepingduck.png"
        self.onCharHead = False
        # -1 for moving left, 0 for still, 1 for moving right
        self.state = 0.1
        self.onGround = False

    def draw(self):
        if not self.onCharHead:
            if self.state == 1:
                drawImage(self.moveRightSprites[self.spriteIndex], self.x, self.y, 
                        width = self.width, height = self.height)
            elif self.state == -1:
                drawImage(self.moveLeftSprites[self.spriteIndex], self.x, self.y, 
                        width = self.width, height = self.height)
            elif self.state == -0.1:
                drawImage(self.stillLeftSprites[self.spriteIndex], self.x, self.y, 
                        width = self.width, height = self.height)
            elif self.state == 0.1:
                drawImage(self.stillRightSprites[self.spriteIndex], self.x, self.y, 
                        width = self.width, height = self.height)
        
    def move(self, dir, terrain):
        dx = -self.speed if dir == -1 else self.speed
        self.x += dx
        for col in terrain:
            for block in col:
                if self.touchesBlock(block):
                    if dir == -1:
                        self.x = block.x + block.width
                        self.jump()
                    else:
                        self.x = block.x - self.width
                        self.jump()
                    return

    def fall(self, terrain):
        self.vy += self.gravity
        self.y += self.vy
        for col in terrain:
            for block in col:
                if self.touchesBlock(block):
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
    
    def touchesBlock(self, block):
        return ((self.x + self.width > block.x) and 
                (self.x < block.x + block.width) and
                (self.y + self.height > block.y) and 
                (block.y + block.height > self.y))
    
    def touchesChar(self, char):
        return ((self.x + self.width > char.x) and 
                (self.x < char.x + char.width) and
                (self.y + self.height > char.y) and 
                (char.y + char.height > self.y))

class DuckFamily:
    def __init__(self):
        self.family = [[]]
    
    def spawn(self, terrain, frame):
        randCol = random.choice(list(range(len(terrain.blocks[frame]))))
        xVal = terrain.blocks[frame][randCol][-1].x
        yVal = terrain.blocks[frame][randCol][-1].y
        width = 0.9 * terrain.screenWidth / terrain.cols
        height = 0.9 * terrain.screenHeight / terrain.rows
        self.family[frame].append(Duck(xVal, yVal - height, width, height))

    def newFrame(self, frame):
        self.family.insert(frame, [])