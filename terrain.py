from opensimplex import OpenSimplex, random_seed
from cmu_graphics import *
import random

class Block:
    def __init__(self, x, y, width, height, texture):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture = texture
    
    def draw(self):
        drawImage(self.texture, self.x, self.y, 
                  width = self.width, height = self.height)

class Terrain:
    def __init__(self, screenWidth, screenHeight, rows, cols):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.rows = rows
        self.cols = cols
        self.blocks = []
        self.textureTypes = {'dirt': r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\dirt.png",
                             'grass': r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\grass.png",
                             'stone': r"C:\Users\Nathan Xie\Desktop\Python Stuff\15-112 N25 Spicy Recis\Project Duck\Images\stone.png"}
        self.makeTerrain(0)

    def makeTerrain(self, index):
        # the number passed in is called a Seed
        # computers do seeded random number generation
        # kind of like a Minecraft seed
        seed = random.randint(0, 10 ** 10)
        noiseGenerator = OpenSimplex(seed = seed)

        # we generate the terrain column by column
        # each entry represents how many blocks will be in a column
        heightMap = []
        for i in range(self.cols):
            # this generates a value between -1.0 and 1.0
            # the two inputs determine how varied your noise is
            noise = noiseGenerator.noise2(i * 0.05, 0)
            # you need to figure out what to do with the noise value
            blockCount = int(abs(noise) * 10) + 2
            assert(blockCount <= self.cols)
            heightMap.append(blockCount)

        # now we generate the blocks according to height map
        blockWidth = self.screenWidth / self.cols
        blockHeight = self.screenHeight / self.rows
        frame = []
        for i in range(len(heightMap)):
            blockCount = heightMap[i]
            temp = []
            for block in range(blockCount):
                texture = self.textureTypes['dirt']
                # if the block is on the surface make it grass
                if block == blockCount - 1:
                    texture = self.textureTypes['grass']
                # if it's too far down make it stone
                elif block < blockCount / 3:
                    texture = self.textureTypes['stone']
                newBlock = Block(blockWidth * i, 
                                 self.screenHeight - blockHeight * (block + 1), 
                                 blockWidth, blockHeight, texture)
                temp.append(newBlock)
            frame.append(temp)
        self.blocks.insert(index, frame)

    def drawTerrain(self, frame):
        for col in self.blocks[frame]:
            for block in col:
                block.draw()