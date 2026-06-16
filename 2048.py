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
    drawBack(app)
    drawBoard(app)
    drawScore(app)
    if app.gameOver:
        drawGameOver(app)
    if app.gameWon:
        drawWin(app)

def drawBack(app):
    drawRect(0,0,app.width,app.height,fill=rgb(187, 173, 160))
 
def drawScore(app):
    drawLabel('Welcome to 2048!', app.width/2, (1/12)*app.height, size=14, bold=True)
    drawLabel(f'Current Score = {app.curScore}', (3/16)*app.width, (9/64)*app.height)
    drawLabel(f'Best Score = {app.bestScore}', (13/16)*app.width, (9/64)*app.height)
 
def drawGameOver(app):
    drawRect(app.width/2, app.height/2, (300/400) * app.width, (150/400) * app.height,
             fill='black', opacity=80, align='center')
    adjustment = (20/400) * app.height
    drawLabel('Game Over!', app.width/2, app.height/2 - adjustment,
              size=24, bold=True, fill='white')
    drawLabel('Press R to Restart', app.width/2, app.height/2 + adjustment,
              size=16, fill='white')
 
def drawWin(app):
    drawRect(app.width/2, app.height/2, (300/400) * app.width, (150/400) * app.height,
             fill='gold', opacity=80, align='center')
    adjustment = (20/400) * app.height
    drawLabel('You Reached 2048!', app.width/2, app.height/2 - adjustment,
              size=20, bold=True, fill='white')
    drawLabel('Press R to Restart', app.width/2, app.height/2 + adjustment,
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
    colors = {2: rgb(238, 228, 218),
              4: rgb(237, 224, 200),
              8: rgb(242, 177, 121),
              16: rgb(245, 149, 99),
              32: rgb(246, 124, 95),
              64: rgb(246, 94, 59),
              128: rgb(237, 207, 114),
              256: rgb(237, 204, 97),
              512: rgb(237, 200, 80),
              1024: rgb(237, 197, 63),
              2048: rgb(237, 194, 46)}
    if cellNum in colors:
        curColor = colors[cellNum]
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=curColor, border='black')
        drawLabel(str(cellNum), cellMidX, cellMidY)
    if cellNum == None:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=rgb(205, 192, 180), border='black')
 
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
    if not app.gameWon:
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
            if shift(colList)[0] != colList:
                return True
    elif key == 'down':
        for col in range(app.cols):
            colList = [app.boardStatus[row][col] for row in range(app.rows - 1, -1, -1)]
            if shift(colList)[0] != colList:
                return True
    elif key == 'left':
        for row in range(app.rows):
            rowList = app.boardStatus[row][:]
            if shift(rowList)[0] != rowList:
                return True
    else:  # key == 'right'
        for row in range(app.rows):
            rowList = app.boardStatus[row][::-1]
            if shift(rowList)[0] != rowList:
                return True
    return False
 
def makeMove(app, key):
    totalScore = 0
    if key == 'up':
        allCols = []
        for col in range(app.cols):
            colList = []
            for row in range(app.rows):
                colList.append(app.boardStatus[row][col])
            allCols.append(colList)
        temps, score = manageShift(allCols)
        totalScore += score
        app.boardStatus = switchRowsCol(temps)
    elif key == 'down':
        allCols = []
        for col in range(app.cols):
            colList = []
            for row in range(app.rows - 1, -1, -1):
                colList.append(app.boardStatus[row][col])
            allCols.append(colList)
        temps, score = manageShift(allCols)
        totalScore += score
        reversedTemps = []
        for colList in temps:
            reversedTemps.append(colList[::-1])
        app.boardStatus = switchRowsCol(reversedTemps)
    elif key == 'left':
        app.boardStatus, score = manageShift(app.boardStatus)
        totalScore += score
    else:  # key == 'right'
        allRows = []
        for row in range(app.rows):
            rowList = app.boardStatus[row][::-1]
            allRows.append(rowList)
        temps, score = manageShift(allRows)
        totalScore += score
        app.boardStatus = []
        for rowList in temps:
            app.boardStatus.append(rowList[::-1])
    app.curScore += totalScore
    if app.curScore > app.bestScore:
        app.bestScore = app.curScore
 
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
    totalScore = 0
    for entry in L:
        shifted, score = shift(entry)
        res.append(shifted)
        totalScore += score
    return res, totalScore
 
def shift(L):
    targetLen = len(L)
    newL = removeWhiteSpace(L)
    res = []
    score = 0
    skip = False
    for i in range(len(newL) - 1):
        if skip:
            skip = False
            continue
        else:
            if newL[i] != newL[i + 1]:
                res.append(newL[i])
            else:
                merged = newL[i] * 2
                res.append(merged)
                score += merged * 5
                skip = True
    if not skip and len(newL) > 0:
        res.append(newL[-1])
    return addWhiteSpace(res, targetLen), score
 
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