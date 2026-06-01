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
        addRandom(app)

def isLegal(app,key):
    if key not in {'up','down','left','right'}:
        return False
    if key == 'up':
        colsCheck = [False] * app.cols
        for col in range(app.cols):
            colFound = False
            colNum = None
            for row in range(app.rows - 1,-1,-1):
                if app.boardStatus[row][col] == None:
                    colsCheck[col] = True
                elif app.boardStatus[row][col] != None and not colFound:
                    colFound = True
                    colNum = app.boardStatus[row][col]
                else: #app.boardStatus[row][col] != None and colFound
                    if app.boardStatus[row][col] == colNum:
                        colsCheck[col] = True
        return colsCheck == ([True] * app.cols)
    elif key == 'down':
        pass
    elif key == 'left':
        pass
    else: #key = 'right'
        pass

def makeMove(app,key):
    if key == 'up':
        allCols = []
        for col in range(app.cols):
            newCol = []
            for row in range(app.rows):
                newCol.append(app.boardStatus[row][col])
            allCols.append(newCol)
        temps = manageShift(allCols)
        app.boardStatus = switchRowsCol(temps)
        # for col in range(app.cols):
        #     colFound = False
        #     for row in range(app.rows - 1,-1,-1):
        #         if app.boardStatus[row][col] == None and not colFound:
        #             continue
        #         elif app.boardStatus[row][col] == None and colFound:
        #             app.boardStatus[row][col] = colNum
        #             app.boardStatus[storeRow][storeCol] = None
        #             storeRow,storeCol = row,col
        #         elif app.boardStatus[row][col] != None and not colFound:
        #             colFound = True
        #             colNum = app.boardStatus[row][col]
        #             storeRow,storeCol = row, col
        #         else: #app.boardStatus[row][col] != None and colFound:
        #             if app.boardStatus[row][col] == colNum:
        #                 app.boardStatus[row][col] = app.boardStatus[row][col] * 2
        #                 app.boardStatus[storeRow][storeCol] = None
        #             else:
        #                 colNum = app.boardStatus[row][col]
        #                 storeRow,storeCol = row,col

def manageShift(L):
    res = []
    for entry in L:
        res.append(shift(entry))
    return res

def shift(L):
    newL = removeWhiteSpace(L)
    res = []
    skip = False
    for i in range(len(newL) - 1):
        if skip:
            skip = False
            continue
        else:
            if newL[i] != newL[i + 1]:
                res.append(newL[i])
            else:
                res.append(newL[i] * 2)
                skip = True
    if not skip and len(newL) > 0:
        res.append(newL[-1])
    return addWhiteSpace(res)

def removeWhiteSpace(L):
    res = []
    for entry in L:
        if entry != None:
            res.append(entry)
    return res

def addWhiteSpace(L):
    res = L
    gridLengthVariable = 4
    while len(res) < gridLengthVariable:
        res.append(None)
    return res

def switchRowsCol(L):
    res = []
    for col in range(len(L[0])):
        newCol = []
        for row in range(len(L)):
            newCol.append(L[row][col])
        res.append(newCol)
    return res
    
def main():
    runApp(width=500,height=500)

main()