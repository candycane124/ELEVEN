import pygame, sys
from pygame.locals import *
from easier import *
import random

#SETUP
pygame.init()
WIDTH, HEIGHT = 600,650
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Eleven!')

class Block():
    def __init__(self,value) -> None:
        self.val = value
        # self.img = pygame.image.load(f"assets/{image}.png")
        pass
    
    def __str__(self) -> str:
        return str(self.val) + " block"
    
    def setVal(self,value) -> None:
        self.val = value
    
    def addVal(self) -> None:
        self.val += 1

class gameContainer():
    '''
    List of 4 lists, each with 4 items

    [
    [0,0,0,0]
    [0,0,0,0]
    [0,0,0,0]
    [0,0,0,0]
    ]

    '''
    def __init__(self) -> None:
        grid = [[],[],[],[]]
        empty = Block(0)
        for row in range(4):
            grid[row] = [empty,empty,empty,empty]
        self.grid = grid
        self.score = 0
        pass

    def display(self,screen,images):
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[row])):
                screen.blit(images[self.grid[row][cell].val],(85+cell*110,35+row*110))

    def new(self,number) -> bool:
        openLocations = []
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[row])):
                if self.grid[row][cell].val == 0:
                    # print(f"added [{row},{cell}]")
                    openLocations.append([row,cell])
        if openLocations:
            chosen = random.randint(0,len(openLocations)-1)
            location = openLocations[chosen]
            self.grid[location[0]][location[1]] = Block(number)
            return True
        else:
            return False
    
    def squish(self, direction):
        oldGrid = self.grid.copy()
        if direction == "right":
            flipGrid = self.grid.copy()
            for row in flipGrid:
                for cell in row:
                    if cell.val == 0:
                        row.remove(cell)
                        row.insert(0,Block(0))
            self.grid = flipGrid
        elif direction == "left":
            flipGrid = self.grid.copy()
            for row in flipGrid:
                for cell in reversed(row):
                    if cell.val == 0:
                        row.remove(cell)
                        row.insert(3,Block(0))
            self.grid = flipGrid
        elif direction == "down":
            flipGrid = self.flipped(self.grid)
            for col in flipGrid:
                for cell in col:
                    if cell.val == 0:
                        col.remove(cell)
                        col.insert(0,Block(0))
            self.grid = self.flipped(flipGrid)
        elif direction == "up":
            flipGrid = self.flipped(self.grid)
            for col in flipGrid:
                for cell in reversed(col):
                    if cell.val == 0:
                        col.remove(cell)
                        col.insert(3,Block(0))
            self.grid = self.flipped(flipGrid)
        # for row in range(4):
        #     for cell in range(4):
        #         print(row, cell, oldGrid[row][cell].val)
        #         print(self.grid[row][cell].val)
        #         if oldGrid[row][cell].val != self.grid[row][cell].val:
        #             return True
        return True

    def right(self):
        valid = False
        if self.squish("right"):
            valid = True
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[row])-1,0,-1):
                if self.grid[row][cell].val != 0 and self.grid[row][cell].val == self.grid[row][cell-1].val:
                    self.grid[row][cell].addVal()
                    self.grid[row][cell-1].setVal(0)
        if self.squish("right"):
            valid = True
        return valid      

    def left(self):
        valid = False
        if self.squish("left"):
            valid = True
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[row])-1):
                if self.grid[row][cell].val != 0 and self.grid[row][cell].val == self.grid[row][cell+1].val:
                    self.grid[row][cell].addVal()
                    self.grid[row][cell+1].setVal(0)
        if self.squish("left"):
            valid = True
        return valid
    
    def down(self):
        valid = False
        if self.squish("down"):
            valid = True
        flipGrid = self.flipped(self.grid)
        for col in range(len(flipGrid)):
            for cell in range(len(flipGrid[col])-1,0,-1):
                if flipGrid[col][cell].val != 0 and flipGrid[col][cell].val == flipGrid[col][cell-1].val:
                    flipGrid[col][cell].addVal()
                    flipGrid[col][cell-1].setVal(0)
        self.grid = self.flipped(flipGrid)
        if self.squish("down"):
            valid = True
        return valid

    def up(self):
        valid = False
        if self.squish("up"):
            valid = True
        flipGrid = self.flipped(self.grid)
        for col in range(len(flipGrid)):
            for cell in range(len(flipGrid[col])-1):
                if flipGrid[col][cell].val != 0 and flipGrid[col][cell].val == flipGrid[col][cell+1].val:
                    flipGrid[col][cell].addVal()
                    flipGrid[col][cell+1].setVal(0)
        self.grid = self.flipped(flipGrid)
        if self.squish("up"):
            valid = True
        return valid

    def flipped(self,toFlip):
        new = [[],[],[],[]]
        for row in toFlip:
            for i in range(4):
                new[i].append(row[i])
        return new
    
    def updateScore(self):
        score = 0
        for row in self.grid:
            for cell in row:
                if cell.val == 11:
                    return True
                score += cell.val*cell.val
        self.score = score
        return False

            

#game container set-up
grid = gameContainer()
grid.new(1)
images = []
for i in range(12):
    images.append(pygame.image.load(f"assets/{i}.png"))
win = False

backBtn = pygame.image.load("assets/back.png")
exitBtn = pygame.image.load("assets/exit.png")
continueBtn = pygame.image.load("assets/continue.png")
replayBtn = pygame.image.load("assets/replay.png")

running = True
validKey = False
nextUp = 1
scene = 1
while running:
    SCREEN.fill((0,0,0))
    if scene == 1: #GAME
        for event in pygame.event.get():
            if event.type == QUIT:
                scene = 2
            if event.type == pygame.KEYDOWN:
                validKey = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not grid.right():
                        validKey = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not grid.left():
                        validKey = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not grid.down():
                        validKey = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not grid.up():
                        validKey = False
                else:
                    validKey = False

        pygame.draw.rect(SCREEN,(150,150,150),(75,25,450,450))
        grid.display(SCREEN,images)
        genText(SCREEN,"Next Block: ",(240,240,240),20,(245,545),"top-right")
        SCREEN.blit(images[nextUp],(250,500))
        genText(SCREEN,"Score: "+str(grid.score),(240,240,240),10,(50,600),"bottom-left")

        pygame.display.update()

        if validKey:
            if grid.updateScore() and not win:
                win = True
                scene = 3
            if grid.new(nextUp) == False:
                scene = 4
            if grid.score >= 100:
                nextUp = random.choices([1,2,3],weights=(60,60,20),k=3)[0]
            else:
                nextUp = random.randint(1,2)
            validKey = False
    elif scene == 2: #LEAVE CONFIRM
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if mousePos[1] >= 230 and mousePos[1] <= 320:
                    if mousePos[0] >= 120 and mousePos[0] <= 290:
                        scene = 1
                    elif mousePos[0] >= 310 and mousePos[0] <= 480:
                        running = False
        genText(SCREEN,"Your game will not save, are you sure you want to leave?",(250,250,250),14,(300,120),"middle")
        SCREEN.blit(backBtn,(120,230))
        SCREEN.blit(exitBtn,(310,230))
        pygame.display.update()
    elif scene == 3: #WINNER
        for event in pygame.event.get():
            if event.type == QUIT:
                scene = 2
            if event.type == MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if mousePos[1] >= 230 and mousePos[1] <= 320:
                    if mousePos[0] >= 120 and mousePos[0] <= 290:
                        scene = 1
                    elif mousePos[0] >= 310 and mousePos[0] <= 480:
                        grid = gameContainer()
                        grid.new(1)
                        images = []
                        for i in range(12):
                            images.append(pygame.image.load(f"assets/{i}.png"))
                        scene = 1
                        win = False
        genText(SCREEN,"Eleven! Congrats, you won!",(250,250,250),14,(300,120),"middle")
        SCREEN.blit(continueBtn,(120,230))
        SCREEN.blit(replayBtn,(310,230))
        pygame.display.update()
    elif scene == 4: #LOSER
        for event in pygame.event.get():
            if event.type == QUIT:
                scene = 2
            if event.type == MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if mousePos[1] >= 230 and mousePos[1] <= 320:
                    if mousePos[0] >= 120 and mousePos[0] <= 290:
                        grid = gameContainer()
                        grid.new(1)
                        images = []
                        for i in range(12):
                            images.append(pygame.image.load(f"assets/{i}.png"))
                        scene = 1
                        win = False
                    elif mousePos[0] >= 310 and mousePos[0] <= 480:
                        running = False
        genText(SCREEN,"You LOST!",(250,250,250),14,(300,120),"middle")
        SCREEN.blit(replayBtn,(120,230))
        SCREEN.blit(exitBtn,(310,230))  
        pygame.display.update()

print(grid.score)

with open("scores.txt","a") as outFile:
    outFile.write(str(grid.score)+"\n")

pygame.quit()
sys.exit()