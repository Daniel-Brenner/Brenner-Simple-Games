from cmu_graphics import *
import math

def onAppStart(app):
    resetApp(app)
    
def resetApp(app):
    app.p1Turn = True
    app.rows = 3
    app.cols = 3
    app.gridLeft = 100
    app.gridTop = 100
    app.gridWidth = 200
    app.gridHeight = 200
    app.gameOver = False
    app.gridStatus = [[None,None,None],[None,None,None],[None,None,None]]
    app.solRow1,app.solRow2,app.solCol1,app.solCol2 = None,None,None,None

def redrawAll(app):
    drawGrid(app)
    if app.gameOver:
        drawGameOver(app)
    else:
        drawTurnLabel(app)

def drawTurnLabel(app):
    if app.p1Turn:
        drawLabel("X's turn",app.width/2,(1/6)*app.height)
    else:
        drawLabel("O's turn",app.width/2,(1/6)*app.height)
    drawLabel('Click to place your mark',app.width/2,(5/6)*app.height)

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app,row,col)

def drawCell(app,row,col):
    if row == 0:
        if col == 0:
            drawTopLeft(app)
        elif col == 1:
            drawTopMid(app)
        else:
            drawTopRight(app)
    elif row == 1:
        if col == 0:
            drawMidLeft(app)
        elif col == 1:
            drawMidMid(app)
        else:
            drawMidRight(app)
    else:
        if col == 0:
            drawBotLeft(app)
        elif col == 1:
            drawBotMid(app)
        else:
            drawBotRight(app)

def getCellSize(app):
    return app.gridWidth / app.cols, app.gridHeight / app.rows

def getCellLeftTop(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft = app.gridLeft + col * cellWidth
    cellTop = app.gridTop + row * cellHeight
    return cellLeft,cellTop

def getCellCenter(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    return cellLeft + cellWidth/2, cellTop + cellHeight/2

def drawCurStatus(app,row,col):
    cellCenterX,cellCenterY = getCellCenter(app,row,col)
    curStatus = app.gridStatus[row][col]
    if curStatus == 'X':
        drawLabel('X',cellCenterX,cellCenterY,size=30,bold=True)
    elif curStatus == 'O':
        drawLabel('O',cellCenterX,cellCenterY,size=30,bold=True)
    
def drawTopLeft(app):
    row, col = 0, 0
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    botLeftX, botLeftY = cellLeft,cellTop + cellHeight
    botRightX,botRightY = cellLeft + cellWidth,botLeftY
    topRightX,topRightY = botRightX,cellTop
    drawLine(botLeftX,botLeftY,botRightX,botRightY)
    drawLine(botRightX,botRightY,topRightX,topRightY)

def drawTopMid(app):
    row,col = 0, 1
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    botLeftX,botLeftY = cellLeft,cellTop + cellHeight
    botRightX,botRightY = cellLeft + cellWidth,botLeftY
    drawLine(botLeftX,botLeftY,botRightX,botRightY)

def drawTopRight(app):
    row,col = 0,2
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    botLeftX,botLeftY = cellLeft,cellTop + cellHeight
    botRightX,botRightY = cellLeft + cellWidth,botLeftY
    drawLine(cellLeft,cellTop,botLeftX,botLeftY)
    drawLine(botLeftX,botLeftY,botRightX,botRightY)

def drawMidLeft(app):
    row,col = 1,0
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    rightTopX,rightTopY = cellLeft + cellWidth,cellTop
    rightBotX,rightBotY = rightTopX,cellTop + cellHeight
    drawLine(rightTopX,rightTopY,rightBotX,rightBotY)

def drawMidMid(app):
    row, col = 1,1
    drawCurStatus(app,row,col)

def drawMidRight(app):
    row,col = 1,2
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    leftBotX,leftBotY = cellLeft,cellTop + cellHeight
    drawLine(cellLeft,cellTop,leftBotX,leftBotY)

def drawBotLeft(app):
    row,col = 2,0
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    topRightX,topRightY = cellLeft + cellWidth,cellTop
    botRightX,botRightY = topRightX,cellTop + cellHeight
    drawLine(cellLeft,cellTop,topRightX,topRightY)
    drawLine(topRightX,topRightY,botRightX,botRightY)

def drawBotMid(app):
    row,col = 2,1
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    topRightX,topRightY = cellLeft + cellWidth,cellTop
    drawLine(cellLeft,cellTop,topRightX,topRightY)

def drawBotRight(app):
    row,col = 2,2
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    drawCurStatus(app,row,col)
    botLeftX,botLeftY = cellLeft,cellTop + cellHeight
    topRightX,topRightY = cellLeft + cellWidth,cellTop
    drawLine(cellLeft,cellTop,botLeftX,botLeftY)
    drawLine(cellLeft,cellTop,topRightX,topRightY)

def drawGameOver(app):
    drawLabel('Press any key or mouse button to restart game',app.width/2,(5/6)*app.height)
    if someoneWon(app):
        drawLabel('Game over!',app.width/2,(1/6)*app.height)
        row1,row2,col1,col2 = app.solRow1,app.solRow2,app.solCol1,app.solCol2
        x1,y1 = getCellCenter(app,row1,col1)
        x2,y2 = getCellCenter(app,row2,col2)
        drawLine(x1,y1,x2,y2,fill='red')
    else:
        drawLabel("Game over! It's a tie",app.width/2,(1/6)*app.height)

def someoneWon(app):
    return not(app.solRow1 == None and app.solRow2 == None and app.solCol1 == None and app.solCol2 == None)

def onMousePress(app,mouseX,mouseY):
    if not app.gameOver:
        if app.p1Turn:
            if isLegal(app,mouseX,mouseY):
                placePiece(app,mouseX,mouseY,'X')
                app.p1Turn = False
        else:
            if isLegal(app,mouseX,mouseY):
                placePiece(app,mouseX,mouseY,'O')
                app.p1Turn = True
        checkGameOver(app)
    else:
        resetApp(app)

def isLegal(app,mouseX,mouseY):
    gridRight = app.gridLeft + app.gridWidth
    gridBot = app.gridTop + app.gridHeight
    if not (app.gridLeft <= mouseX <= gridRight and app.gridTop <= mouseY <= gridBot):
        return False
    row,col = findRowCol(app,mouseX,mouseY)
    if app.gridStatus[row][col] != None:
        return False
    else:
        return True

def placePiece(app,mouseX,mouseY,piece):
    row,col = findRowCol(app,mouseX,mouseY)
    app.gridStatus[row][col] = piece

def findRowCol(app,mouseX,mouseY):
    cellWidth,cellHeight = getCellSize(app)
    row = math.floor((mouseY - app.gridTop) / cellHeight)
    col = math.floor((mouseX - app.gridLeft) / cellWidth)
    return row,col

def checkGameOver(app):
    hasNone = False
    for row in range(app.rows):
        for col in range(app.cols):
            if connectsFromHere(app,row,col):
                app.gameOver = True
            if app.gridStatus[row][col] == None:
                hasNone = True
    if not hasNone:
        app.gameOver = True

def connectsFromHere(app,row,col):
    if app.gridStatus[row][col] == None:
        return False
    compStatus = app.gridStatus[row][col]
    directions = [(-1,-1),(0,-1),(1,-1),
                 (-1,0),        (1,0),
                 (-1,1), (0,1), (1,1)]
    for drow,dcol in directions:
        for i in range(3):
            newRow,newCol = row + drow * i,col + dcol * i
            if newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols:
                break
            if app.gridStatus[newRow][newCol] != compStatus:
                break
            if i == 2 and app.gridStatus[newRow][newCol] == compStatus:
                app.solRow1,app.solCol1 = row,col
                app.solRow2,app.solCol2 = newRow,newCol
                return True
    return False

def onKeyPress(app,key):
    if app.gameOver:
        resetApp(app)

def main():
    runApp()

main()