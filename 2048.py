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
    app.gameOver = False
    app.gameWon = False
 
def boardGen(app):
    res = []
    for _ in range(app.rows):
        newRow = [None] * app.cols
        res.append(newRow)
    return res
 
def addRandom(app):
    emptyCells = []
    for row in range(app.rows):
        for col in range(app.cols):
            if app.boardStatus[row][col] == None:
                emptyCells.append((row, col))
    if emptyCells == []:
        return
    randNum = random.randrange(101)
    if randNum >= 90:
        nextNum = 4
    else:
        nextNum = 2
    randRow, randCol = random.choice(emptyCells)
    app.boardStatus[randRow][randCol] = nextNum
 
def redrawAll(app):
    drawBoard(app)
    drawScore(app)
    if app.gameOver:
        drawGameOver(app)
    if app.gameWon:
        drawWin(app)
 
def drawScore(app):
    drawLabel('Welcome to 2048!', app.width/2, (1/12)*app.height, size=14, bold=True)
    drawLabel(f'Current Score = {app.curScore}', (3/16)*app.width, (9/64)*app.height)
    drawLabel(f'Best Score = {app.bestScore}', (13/16)*app.width, (9/64)*app.height)
 
def drawGameOver(app):
    drawRect(app.width/2, app.height/2, 300, 150,
             fill='black', opacity=80, align='center')
    drawLabel('Game Over!', app.width/2, app.height/2 - 20,
              size=24, bold=True, fill='white')
    drawLabel('Press R to Restart', app.width/2, app.height/2 + 20,
              size=16, fill='white')
 
def drawWin(app):
    drawRect(app.width/2, app.height/2, 300, 150,
             fill='gold', opacity=80, align='center')
    drawLabel('You Reached 2048!', app.width/2, app.height/2 - 20,
              size=20, bold=True, fill='white')
    drawLabel('R to Restart or Keep Playing!', app.width/2, app.height/2 + 20,
              size=14, fill='white')
 
def drawBoard(app):
    drawGrid(app)
    drawOutline(app)
 
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
 
def drawCell(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft, cellTop = getCellLeftTop(app, row, col, cellWidth, cellHeight)
    cellMidX, cellMidY = getCellMid(cellLeft, cellTop, cellWidth, cellHeight)
    cellNum = app.boardStatus[row][col]
    colors = {2: 'yellow',
              4: 'orange',
              8: 'pink',
              16: 'blue',
              32: 'maroon',
              64: 'crimson',
              128: 'cyan',
              256: 'lightGreen',
              512: 'violet',
              1024: 'indigo',
              2048: 'brown'}
    if cellNum in colors:
        curColor = colors[cellNum]
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=curColor, border='black')
        drawLabel(str(cellNum), cellMidX, cellMidY)
    if cellNum == None:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=None, border='black')
 
def getCellLeftTop(app, row, col, cellWidth, cellHeight):
    return app.boardLeft + col * cellWidth, app.boardTop + row * cellHeight
 
def getCellSize(app):
    return app.boardWidth / app.cols, app.boardHeight / app.rows
 
def drawOutline(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black', borderWidth=4)
 
def getCellMid(cellLeft, cellTop, cellWidth, cellHeight):
    return cellLeft + cellWidth / 2, cellTop + cellHeight / 2
 
def onKeyPress(app, key):
    if key == 'r':
        resetApp(app)
        return
    if app.gameOver:
        return
    if key in {'up', 'down', 'left', 'right'} and isLegal(app, key):
        makeMove(app, key)
        addRandom(app)
        if not app.gameWon:
            app.gameWon = checkWin(app)
        if isGameOver(app):
            app.gameOver = True
 
def isLegal(app, key):
    if key not in {'up', 'down', 'left', 'right'}:
        return False
    if key == 'up':
        for col in range(app.cols):
            colList = [app.boardStatus[row][col] for row in range(app.rows)]
            if shift(colList) != colList:
                return True
    elif key == 'down':
        for col in range(app.cols):
            colList = [app.boardStatus[row][col] for row in range(app.rows - 1, -1, -1)]
            if shift(colList) != colList:
                return True
    elif key == 'left':
        for row in range(app.rows):
            rowList = app.boardStatus[row][:]
            if shift(rowList) != rowList:
                return True
    else:  # key == 'right'
        for row in range(app.rows):
            rowList = app.boardStatus[row][::-1]
            if shift(rowList) != rowList:
                return True
    return False
 
def makeMove(app, key):
    if key == 'up':
        allCols = []
        for col in range(app.cols):
            colList = []
            for row in range(app.rows):
                colList.append(app.boardStatus[row][col])
            allCols.append(colList)
        temps = manageShift(allCols)
        app.boardStatus = switchRowsCol(temps)
    elif key == 'down':
        allCols = []
        for col in range(app.cols):
            colList = []
            for row in range(app.rows - 1, -1, -1):
                colList.append(app.boardStatus[row][col])
            allCols.append(colList)
        temps = manageShift(allCols)
        reversedTemps = []
        for colList in temps:
            reversedTemps.append(colList[::-1])
        app.boardStatus = switchRowsCol(reversedTemps)
    elif key == 'left':
        app.boardStatus = manageShift(app.boardStatus)
    else:  # key == 'right'
        allRows = []
        for row in range(app.rows):
            rowList = app.boardStatus[row][::-1]
            allRows.append(rowList)
        temps = manageShift(allRows)
        app.boardStatus = []
        for rowList in temps:
            app.boardStatus.append(rowList[::-1])
 
def checkWin(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.boardStatus[row][col] == 2048:
                return True
    return False
 
def isGameOver(app):
    for key in ['up', 'down', 'left', 'right']:
        if isLegal(app, key):
            return False
    return True
 
def manageShift(L):
    res = []
    for entry in L:
        res.append(shift(entry))
    return res
 
def shift(L):
    targetLen = len(L)
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
    return addWhiteSpace(res, targetLen)
 
def removeWhiteSpace(L):
    res = []
    for entry in L:
        if entry != None:
            res.append(entry)
    return res
 
def addWhiteSpace(L, targetLen):
    res = L[:]
    while len(res) < targetLen:
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
    runApp(width=500, height=500)
 
main()