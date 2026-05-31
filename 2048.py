from cmu_graphics import *
import random

def onAppStart(app):
    app.bestScore = 0
    resetApp(app)

def resetApp(app):
    app.boardLeft = (50/400) * app.width
    app.boardTop = (75/400) * app.height
    app.rows = 4
    app.cols = 4
    app.boardWidth = (300/400) * app.width
    app.boardHeight = (300/400) * app.height
    app.boardStatus = boardGen(app)
    addRandom(app)
    addRandom(app)
    app.curScore = 0

def boardGen(app):
    res = []
    for _ in range(app.rows):
        newRow = [None] * app.cols
        res.append(newRow)
    return res

def addRandom(app):
    randNum = random.randrange(101)
    if randNum >= 90:
        nextNum = 4
    else:
        nextNum = 2
    added = False
    while added == False:
        randRow,randCol = random.randrange(app.rows),random.randrange(app.cols)
        if app.boardStatus[randRow][randCol] == None:
            app.boardStatus[randRow][randCol] = nextNum
            added = True

def redrawAll(app):
    drawBoard(app)
    drawScore(app)

def drawScore(app):
    drawLabel('Welcome to 2048!',app.width/2,(1/12)*app.height,size=14,bold=True)
    drawLabel(f'Current Score = {app.curScore}',(3/16)*app.width,(9/64)*app.height)
    drawLabel(f'Best Score = {app.bestScore}',(13/16)*app.width,(9/64)*app.height)

def drawBoard(app):
    drawGrid(app)
    drawOutline(app)

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app,row,col)

def drawCell(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col,cellWidth,cellHeight)
    cellMidX,cellMidY = getCellMid(cellLeft,cellTop,cellWidth,cellHeight)
    cellNum = app.boardStatus[row][col]
    if cellNum == None:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill=None,border='black')
    elif cellNum == 2:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='yellow',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 4:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='orange',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 8:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='pink',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 16:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='blue',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 32:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='maroon',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 64:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='crimson',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 128:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='cyan',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 256:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='lightGreen',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 512:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='violet',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    elif cellNum == 1024:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='indigo',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)
    else:
        drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill='brown',border='black')
        drawLabel(str(cellNum),cellMidX,cellMidY)

def getCellLeftTop(app,row,col,cellWidth,cellHeight):
    return app.boardLeft + col * cellWidth,app.boardTop + row * cellHeight

def getCellSize(app):
    return app.boardWidth / app.cols, app.boardHeight/app.rows
    
def drawOutline(app):
    drawRect(app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight,fill=None,border='black',borderWidth=4)

def getCellMid(cellLeft,cellTop,cellWidth,cellHeight):
    return cellLeft + cellWidth / 2, cellTop + cellHeight / 2

def onKeyPress(app,key):
    if isLegal(app,key):
        makeMove(app,key)

def isLegal(app,key):
    if key not in {'up','down','left','right'}:
        return False
    if key == 'up':
        colsCheck = [False] * app.cols
        for col in range(app.cols):
            colFound = False
            colNum = None
            for row in range(app.rows - 1,-1,-1):
                if row == 0 and app.boardStatus[row][col] == None and not colFound:
                    colsCheck[col] = True
                elif app.boardStatus[row][col] != None and not colFound:
                    colFound = True
                    colNum = app.boardStatus[row][col]
                #function NOT complete
        return colsCheck == ([True] * app.cols)
    elif key == 'down':
        pass

def makeMove(app):
    pass
    
def main():
    runApp(width=500,height=500)

main()