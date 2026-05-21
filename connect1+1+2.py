from cmu_graphics import *
import random

globalRowVar = 5

def onAppStart(app):
    resetApp(app)

def resetApp(app):
    #selectScreen
    app.firstColorSelected = False
    app.colors = ['red','orange','yellow','green','blue','indigo','violet']
    app.secondColors = ['red','orange','yellow','green','blue','indigo','violet']
    app.playerOneColorIndex = random.randrange(len(app.colors) - 1)
    app.playerTwoColorIndex = random.randrange(len(app.colors) - 2)
    #gameScreen
    app.boardLeft = (25/400) * app.width
    app.boardTop = (50/400) * app.height
    app.rows = 6
    app.cols = 7
    app.boardWidth = (350/400) * app.width
    app.boardHeight = (300/400) * app.height
    app.boardStatus = boardGen(app)
    app.p1Turn = True
    app.p1Col = 0
    app.p2Col = 0
    app.gameOver = False
    app.someoneWon = False

def boardGen(app):
    res = []
    for _ in range(app.rows):
        newRow = [None] * app.cols
        res.append(newRow)
    return res

def select_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='yellow')
    drawLabel('welcome to connect 1+1+2!',(1/2)*app.width,(1/3)*app.height,size=18,bold=True)
    drawLabel('select your colors!',(1/2)*app.width,(1/2)*app.height,size=14)
    drawColors(app)

def drawColors(app):
    drawPlayerOneCircle(app)
    if app.firstColorSelected:
        drawPlayerTwoCircle(app)

def drawPlayerOneCircle(app):
    color = app.colors[app.playerOneColorIndex]
    if color == 'yellow':
        drawCircle((1/4)*app.width,(3/4)*app.height,(40/400)*app.width,fill=color,border='black')
    else:
        drawCircle((1/4)*app.width,(3/4)*app.height,(40/400)*app.width,fill=color)
    drawLabel('Player 1',(1/4)*app.width,(3/4)*app.height)
    if app.firstColorSelected:
        rectWidth = (75/400) * app.width
        rectHeight = (25/400) * app.height
        drawRect((1/4)*app.width,(25/32)*app.height,rectWidth,rectHeight,fill='green',border='black')
        xAdj = 2/400 * app.width
        yAdj = 3/400 * app.width
        drawLabel('selected',(1/4)*app.width+xAdj,(25/32)*app.height+yAdj,align='top-left',size=19)

def drawPlayerTwoCircle(app):
    color = app.secondColors[app.playerTwoColorIndex]
    if color == 'yellow':
        drawCircle((3/4)*app.width,(3/4)*app.height,(40/400)*app.width,fill=color,border='black')
    else:
        drawCircle((3/4)*app.width,(3/4)*app.height,(40/400)*app.width,fill=color)
    drawLabel('Player 2',(3/4)*app.width,(3/4)*app.height)

def select_onKeyPress(app,key):
    if key == 'enter' and not app.firstColorSelected:
        app.secondColors.pop(app.playerOneColorIndex)
        app.firstColorSelected = True
    elif key == 'enter' and app.firstColorSelected:
        setActiveScreen('game')
    if not app.firstColorSelected:
        if key == 'left':
            if app.playerOneColorIndex == 0:
                app.playerOneColorIndex = len(app.colors) - 1
            else:
                app.playerOneColorIndex -= 1
        elif key == 'right':
            if app.playerOneColorIndex == len(app.colors) - 1:
                app.playerOneColorIndex = 0
            else:
                app.playerOneColorIndex += 1
    else:
        if key == 'left':
            if app.playerTwoColorIndex == 0:
                app.playerTwoColorIndex = len(app.secondColors) - 1
            else:
                app.playerTwoColorIndex -= 1
        elif key == 'right':
            if app.playerTwoColorIndex == len(app.secondColors) - 1:
                app.playerTwoColorIndex = 0
            else:
                app.playerTwoColorIndex += 1

def game_redrawAll(app):
    drawTurn(app)
    drawBoard(app)
    
def drawTurn(app):
    if app.p1Turn:
        string = "Player 1's Turn"
    else:
        string = "Player 2's Turn"
    drawLabel(string,app.width/2,app.height/11,size=13)

def drawBoard(app):
    drawGrid(app)
    drawOutline(app)
    drawGhost(app)
    if app.gameOver:
        if app.someoneWon:
            drawGameOverWithVictory(app)
        else:
            drawGameOverWithTie(app)

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app,row,col)

def drawCell(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col,cellWidth,cellHeight)
    drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill=None,border='black')
    circleCx,circleCy = cellLeft + cellWidth/2,cellTop + cellHeight/2
    if app.boardStatus[row][col] == None:
        color = None
    elif app.boardStatus[row][col] == 'p1':
        color = app.colors[app.playerOneColorIndex]
    else: #p2
        color = app.secondColors[app.playerTwoColorIndex]
    drawCircle(circleCx,circleCy,cellWidth/2.7,fill=color)

def getCellLeftTop(app,row,col,cellWidth,cellHeight):
    return app.boardLeft + col * cellWidth,app.boardTop + row * cellHeight

def getCellSize(app):
    return app.boardWidth / app.cols, app.boardHeight/app.rows
    
def drawOutline(app):
    drawRect(app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight,fill=None,border='black',borderWidth=4)

def drawGhost(app):
    if app.p1Turn:
        drawP1Ghost(app)
    else:
        drawP2Ghost(app)

def drawP1Ghost(app,row=globalRowVar):
    color = app.colors[app.playerOneColorIndex]
    col = app.p1Col
    if row < 0:
        drawGhostAboveGrid(app,col,color)
    elif app.boardStatus[row][col] == None:
        drawGhostCircle(app,row,col,color)
    else:
        drawP1Ghost(app,row-1)

def drawP2Ghost(app,row=globalRowVar):
    color = app.secondColors[app.playerTwoColorIndex]
    col = app.p2Col
    if row < 0:
        drawGhostAboveGrid(app,col,color)
    elif app.boardStatus[row][col] == None:
        drawGhostCircle(app,row,col,color)
    else:
        drawP2Ghost(app,row-1)

def drawGhostCircle(app,row,col,color):
    opacityPercentage = 50
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col,cellWidth,cellHeight)
    circleCx,circleCy = cellLeft + cellWidth/2,cellTop + cellHeight/2
    drawCircle(circleCx,circleCy,cellWidth/2.7,fill=color,opacity=opacityPercentage)

def drawGhostAboveGrid(app,col,color):
    opacityPercentage = 50
    row = -1
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col,cellWidth,cellHeight)
    circleCx,circleCy = cellLeft + cellWidth/2,cellTop + cellHeight/2
    drawCircle(circleCx,circleCy,cellWidth/2.7,fill=color,opacity=opacityPercentage)

def drawGameOverWithVictory(app):
    drawLabel('Game Over!',app.width/2,(10/11)*app.height,size=18,bold=True)
    x1,y1 = app.solutionBeginning
    x2,y2 = app.solutionEnding
    drawLine(x1,y1,x2,y2,fill='red',lineWidth=3)

def drawGameOverWithTie(app):
    drawLabel('Game Over! It was a tie!',app.width/2,(10/11)*app.height,size=18,bold=True)
    

def game_onKeyPress(app,key):
    if not app.gameOver:
        if app.p1Turn:
            if key == 'left':
                if app.p1Col == 0:
                    app.p1Col = app.cols - 1
                else:
                    app.p1Col -= 1
            elif key == 'right':
                if app.p1Col == app.cols - 1:
                    app.p1Col = 0
                else:
                    app.p1Col += 1
            elif key == 'enter':
                if isLegal(app):
                    placePiece(app)
                    app.p1Turn = not app.p1Turn
        else:
            if key == 'left':
                if app.p2Col == 0:
                    app.p2Col = app.cols - 1
                else:
                    app.p2Col -= 1
            elif key == 'right':
                if app.p2Col == app.cols - 1:
                    app.p2Col = 0
                else:
                    app.p2Col += 1
            elif key == 'enter':
                if isLegal(app):
                    placePiece(app)
                    app.p1Turn = not app.p1Turn
        checkIfWin(app)
    else:
        resetApp(app)
        setActiveScreen('select')

def isLegal(app):
    if app.p1Turn:
        col = app.p1Col
    else:
        col = app.p2Col
    return app.boardStatus[0][col] == None

def placePiece(app,row=globalRowVar):
    if app.p1Turn:
        col = app.p1Col
    else:
        col = app.p2Col
    if app.boardStatus[row][col] == None:
        app.boardStatus[row][col] = 'p1' if app.p1Turn else 'p2'
    else:
        placePiece(app,row-1)

def checkIfWin(app):
    curIterationHasNone = False
    for i in range(app.rows):
        for j in range(app.cols):
            if app.boardStatus[i][j] != None:
                curPlayer = app.boardStatus[i][j]
                if winFromCurPosition(app,i,j,curPlayer):
                    app.gameOver = True
                    app.someoneWon = True
                    return
            else:
                curIterationHasNone = True
    if not curIterationHasNone:
        app.gameOver = True

def winFromCurPosition(app,row,col,player):
    dir = [(-1,-1),(0,-1),(1,-1),
           (-1,0),        (1,0),
           (-1,1), (0,1), (1,1)]
    connectFour = 4 #Win condition is connect 4
    for drow, dcol in dir:
        endRow = row + connectFour * drow
        endCol = col + connectFour * dcol
        if endRow < 0 or endRow >= app.rows or endCol < 0 or endCol >= app.cols:
            continue
        else:
            for i in range(connectFour):
                curRow, curCol = row + i * drow, col + i * dcol
                if app.boardStatus[curRow][curCol] != player:
                    break
                if i == connectFour - 1 and app.boardStatus[curRow][curCol] == player:
                    app.solutionBeginning = getCellCenter(app,row,col)
                    app.solutionEnding = getCellCenter(app,curRow,curCol)
                    return True
    return False

def getCellCenter(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col,cellWidth,cellHeight)
    return cellLeft + cellWidth/2, cellTop + cellHeight/2

def main():
    runAppWithScreens(initialScreen='select')

main()