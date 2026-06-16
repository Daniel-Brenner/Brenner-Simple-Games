from cmu_graphics import *

def onAppStart(app):
    resetApp(app)

def resetApp(app):
    #select
    app.p1ColorSelected = False
    app.colors = ['red','orange','yellow','green','blue','indigo','violet']
    app.colorSelectIndex = 0
    app.p1Color = None
    app.p2Color = None
    app.dim = 7
    app.colorSelectDone = False
    app.gridSizeSelectDone = False
    app.instruction = False
    #game
    app.p1Turn = True
    app.boardLeft, app.boardTop = (50/400) * app.width, (50/400) * app.height
    app.boardWidth, app.boardHeight = (300/400) * app.width, (300/400) * app.height
    app.boardStatus = boardGen(app)
    app.hoverX,app.hoverY = app.width, app.height
    app.p1Score, app.p2Score = 0, 0
    app.gameOver = False

def boardGen(app):
    res = []
    numExits = 2
    for _ in range(app.dim + 1):
        newRow = []
        for _ in range(app.dim + 1):
            newEntry = [None]
            for _ in range(numExits):
                newEntry.append(None)
            newRow.append(newEntry)
        res.append(newRow)
    return res

################################################
#__selectScreen___
################################################

def select_redrawAll(app):
    drawBGAndLabels(app)
    drawColorSelectCircles(app)
    if app.colorSelectDone:
        drawSmallDots(app)
    if app.instruction:
        drawInstruction(app)

def drawBGAndLabels(app):
    drawRect(0,0,app.width,app.height,fill='maroon')
    drawLabel('Welcome to Lines and Boxes!',app.width/2,(1/4)*app.height,size=24,bold=True,fill='yellow')
    adj = (24/400) * app.height
    drawLabel("Press 'i' to view instructions",app.width/2,(1/4)*app.height + adj,size=15,fill='yellow')

def drawColorSelectCircles(app):
    circleRadius = (30/400) * app.width
    selectRectWidth,selectRectHeight = (60/400)*app.width,(20/400)*app.height
    adj = (3/400) * app.width
    labelAdj = (3/400) * app.height
    drawLabel('Player 1',(1/4)*app.width,(21/32)*app.height - labelAdj,size=14,bold=True)
    if app.p1Color == None:
        drawCircle((1/4)*app.width,(3/4)*app.height,circleRadius,fill=app.colors[app.colorSelectIndex],border='black',opacity=40)
    else:
        drawCircle((1/4)*app.width,(3/4)*app.height,circleRadius,fill=app.p1Color,border='black')
        drawRect((1/4)*app.width,(3/4)*app.height,selectRectWidth,selectRectHeight,fill='darkGreen',border='black',align='left')
        drawLabel('selected',(1/4)*app.width + adj,(3/4)*app.height,size=14,align='left')
    if app.p1ColorSelected:
        drawLabel('Player 2',(2/4)*app.width,(21/32)*app.height - labelAdj,size=14,bold=True)
        if app.p2Color == None:
            drawCircle((2/4)*app.width,(3/4)*app.height,circleRadius,fill=app.colors[app.colorSelectIndex],border='black',opacity=40)
        else:
            drawCircle((2/4)*app.width,(3/4)*app.height,circleRadius,fill=app.p2Color,border='black')
            drawRect((2/4)*app.width,(3/4)*app.height,selectRectWidth,selectRectHeight,fill='darkGreen',border='black',align='left')
            drawLabel('selected',(2/4)*app.width + adj,(3/4)*app.height,size=14,align='left')

def drawSmallDots(app):
    squareOffset = (30/400) * app.width
    squareSize = squareOffset * 2
    difference = squareSize / (app.dim - 1)
    squareCenterX,squareCenterY = (3/4)*app.width,(3/4)*app.height
    squareLeft,squareTop = squareCenterX - squareOffset,squareCenterY - squareOffset
    smallDotRadius = (1/400) * app.width
    labelAdj = (4/400) * app.height
    drawLabel('grid size',(3/4)*app.width,(21/32)*app.height - labelAdj,size=14,bold=True)
    for i in range(app.dim):
        x = squareLeft + i * difference
        for j in range(app.dim):
            y = squareTop + j * difference
            drawCircle(x,y,smallDotRadius)
    if app.gridSizeSelectDone:
        selectRectWidth,selectRectHeight = (60/400)*app.width,(20/400)*app.height
        adj = (3/400) * app.width
        drawRect((3/4)*app.width,(3/4)*app.height,selectRectWidth,selectRectHeight,fill='darkGreen',border='black',align='left')
        drawLabel('selected',(3/4)*app.width + adj,(3/4)*app.height,size=14,align='left')

def drawInstruction(app):
    allInstructions = ['Instructions for Lines and Boxes!',
                       '',
                       "Press 'i' to exit instructions",
                       'Left and right arrow keys to select',
                       'Enter key to advance to next step',
                       'Move mouse over line that you want to place',
                       'Click to place the ghost piece',
                       'Score by placing the line that completes a box',
                       'If you score, you get another turn, else opponent gets turn',
                       'Game is over when all boxes are filled',
                       '']
    rectWidth,rectHeight = (7/8) * app.width, (1/2)*app.height
    drawRect(app.width/2,app.height/2,rectWidth,rectHeight,fill='purple',border='black',align='center')
    boxTop = (app.height/2) - (1/2) * (rectHeight)
    boxBot = (app.height/2) + (1/2) * (rectHeight)
    boxHeight = boxBot - boxTop
    lineDiv = boxHeight / len(allInstructions)
    for i in range(1,len(allInstructions) + 1):
        y = boxTop + i * lineDiv
        if i == 1:
            drawLabel(allInstructions[i-1],app.width/2,y,size=15,bold=True)
        else:
            drawLabel(allInstructions[i-1],app.width/2,y)

def select_onKeyPress(app,key):
    if app.instruction:
        if key == 'i':
            app.instruction = not app.instruction
    else:
        if key == 'i':
            app.instruction = not app.instruction
        if not app.colorSelectDone:
            if not app.p1ColorSelected:
                if key == 'left':
                    if app.colorSelectIndex == 0:
                        app.colorSelectIndex = len(app.colors) - 1
                    else:
                        app.colorSelectIndex -= 1
                elif key == 'right':
                    if app.colorSelectIndex == len(app.colors) - 1:
                        app.colorSelectIndex = 0
                    else:
                        app.colorSelectIndex += 1
                elif key == 'enter':
                    app.p1Color = app.colors[app.colorSelectIndex]
                    app.colors.pop(app.colorSelectIndex)
                    app.colorSelectIndex = 0
                    app.p1ColorSelected = True
            else:
                if key == 'left':
                    if app.colorSelectIndex == 0:
                        app.colorSelectIndex = len(app.colors) - 1
                    else:
                        app.colorSelectIndex -= 1
                elif key == 'right':
                    if app.colorSelectIndex == len(app.colors) - 1:
                        app.colorSelectIndex = 0
                    else:
                        app.colorSelectIndex += 1
                elif key == 'enter':
                    app.p2Color = app.colors[app.colorSelectIndex]
                    app.colorSelectDone = True
        elif not app.gridSizeSelectDone:
            if key == 'right':
                if app.dim == 9:
                    app.dim = 4
                else:
                    app.dim += 1
            elif key == 'left':
                if app.dim == 4:
                    app.dim = 9
                else:
                    app.dim -= 1
            elif key == 'enter':
                app.gridSizeSelectDone = True
        else:
            if key == 'enter':
                setActiveScreen('game')

#############################################
#__gameScreen__
#############################################

def game_redrawAll(app):
    drawBoard(app)
    drawTurnLabel(app)
    drawScores(app)
    drawGhostPiece(app)
    drawGameStatus(app)
    if app.gameOver:
        drawGameOver(app)
   
def drawBoard(app):
    if app.dim > 6:
        circleRad = (5/400) * app.width
    else:
        circleRad = (10/400) * app.width
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    for i in range(app.dim):
        y = app.boardTop + diff * i
        for j in range(app.dim):
            x = app.boardLeft + diff * j
            drawCircle(x,y,circleRad)

def drawTurnLabel(app):
    if app.p1Turn:
        msg = "Player 1's Turn"
    else:
        msg = "Player 2's Turn"
    drawLabel(msg,app.width/2,(2/32)*app.height,size=16,bold=True)

def drawScores(app):
    drawLabel(f'Player 1 Score: {app.p1Score}',(2/12)*app.width,(2/32)*app.height,size=14,bold=True)
    drawLabel(f'Player 2 Score: {app.p2Score}',(10/12)*app.width,(2/32)*app.height,size=14,bold=True)

def drawGhostPiece(app):
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    adj = diff / 3
    for i in range(app.dim):
        y = app.boardTop + diff * i
        for j in range(app.dim):
            x = app.boardLeft + diff * j
            if j < app.dim - 1:
                if (x <= app.hoverX <= x + diff and 
                    y - adj <= app.hoverY <= y + adj and
                    isLegal(app,app.hoverX,app.hoverY)):
                    drawLine(x, y, x + diff, y, lineWidth=6, fill='yellow', opacity=70)
                    return
            if i < app.dim - 1:
                if (x - adj <= app.hoverX <= x + adj and 
                    y <= app.hoverY <= y + diff and
                    isLegal(app,app.hoverX,app.hoverY)):
                    drawLine(x, y, x, y + diff, lineWidth=6, fill='yellow', opacity=70)
                    return

def drawGameStatus(app):
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    for row in range(app.dim):
        y = app.boardTop + diff * row
        for col in range(app.dim):
            x = app.boardLeft + diff * col
            box,toRight,toBot = app.boardStatus[row][col]
            if box != None:
                color = getColor(app,box)
                drawRect(x,y,diff,diff,fill=color,opacity=60)
            counter = 0
            diffsList = [(diff,0),(0,diff)]
            for entry in [toRight,toBot]:
                if entry != None:
                    color = getColor(app,entry)
                    dx,dy = diffsList[counter]
                    drawLine(x,y,x+dx,y+dy,fill=color,opacity=60)
                counter += 1

def getColor(app,entry):
    if entry == 'p1':
        return app.p1Color
    else:
        return app.p2Color

def drawGameOver(app):
    adj = (13/400) * app.height
    rectWidth = (29/32) * app.width
    rectHeight = (1/5) * app.width
    drawRect(app.width/2,app.height/2,rectWidth,rectHeight,align='center',fill='gold',border='black')
    if app.p1Score > app.p2Score:
        drawLabel('Game Over! Player 1 Wins!',app.width/2,app.height/2-adj,size=14,bold=True)
    elif app.p2Score > app.p1Score:
        drawLabel('Game Over! Player 2 Wins!',app.width/2,app.height/2-adj,size=14,bold=True)
    else:
        drawLabel('Game Over! It Was a Draw',app.width/2,app.height/2-adj,size=14,bold=True)
    drawLabel('Press any key or press the mouse to return to home screen',app.width/2,(app.height/2) + adj)

def game_onMouseMove(app,mouseX,mouseY):
    if not app.gameOver:
        app.hoverX, app.hoverY = mouseX,mouseY

def game_onMousePress(app,mouseX,mouseY):
    if not app.gameOver:
        app.hoverX, app.hoverY = app.width, app.height
        if isLegal(app,mouseX,mouseY):
            if not changeBoardStatus(app,mouseX,mouseY):
                app.p1Turn = not app.p1Turn
        if app.p1Score + app.p2Score == (app.dim - 1) ** 2:
            app.gameOver = True
    else:
        resetApp(app)
        setActiveScreen('select')

def game_onKeyPress(app,key):
    if app.gameOver:
        resetApp(app)
        setActiveScreen('select')

def isLegal(app,mouseX,mouseY):
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    adj = diff / 3
    for row in range(app.dim):
        y = app.boardTop + diff * row
        for col in range(app.dim):
            x = app.boardLeft + diff * col
            if col < app.dim - 1:
                if (x <= mouseX <= x + diff and 
                    y - adj <= mouseY <= y + adj):
                    return app.boardStatus[row][col][1] == None 
            if row < app.dim - 1:
                if (x - adj <= mouseX <= x + adj and 
                    y <= mouseY <= y + diff):
                    return app.boardStatus[row][col][2] == None 
    return False

def changeBoardStatus(app, mouseX, mouseY):
    if app.p1Turn:
        curPlayer = 'p1'
    else:
        curPlayer = 'p2'
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    adj = diff / 3
    for row in range(app.dim):
        y = app.boardTop + diff * row
        for col in range(app.dim):
            x = app.boardLeft + diff * col
            if col < app.dim - 1:
                if (x <= mouseX <= x + diff and 
                    y - adj <= mouseY <= y + adj):
                    app.boardStatus[row][col][1] = curPlayer
                    closedBelow = checkSingleBox(app, row, col, curPlayer)
                    closedAbove = checkSingleBox(app, row - 1, col, curPlayer)
                    if closedAbove and closedBelow:
                        if curPlayer == 'p1':
                            app.p1Score += 2
                        else:
                            app.p2Score += 2
                        return True
                    elif closedBelow or closedAbove:
                        if curPlayer == 'p1':
                            app.p1Score += 1
                        else:
                            app.p2Score += 1
                        return True
                    else:
                        return False
            if row < app.dim - 1:
                if (x - adj <= mouseX <= x + adj and 
                    y <= mouseY <= y + diff): 
                    app.boardStatus[row][col][2] = curPlayer
                    closedRight = checkSingleBox(app, row, col, curPlayer)
                    closedLeft = checkSingleBox(app, row, col - 1, curPlayer)
                    if closedRight and closedLeft:
                        if curPlayer == 'p1':
                            app.p1Score += 2
                        else:
                            app.p2Score += 2
                        return True
                    elif closedRight or closedLeft:
                        if curPlayer == 'p1':
                            app.p1Score += 1
                        else:
                            app.p2Score += 1
                        return True
                    else:
                        return False
    return False

def checkSingleBox(app, row, col, curPlayer):
    if 0 <= row < app.dim - 1 and 0 <= col < app.dim - 1:
        if app.boardStatus[row][col][0] != None:
            return False
        if (app.boardStatus[row][col][1] != None and       
            app.boardStatus[row][col][2] != None and       
            app.boardStatus[row][col + 1][2] != None and   
            app.boardStatus[row + 1][col][1] != None):     
            app.boardStatus[row][col][0] = curPlayer
            return True
    return False

def main():
    runAppWithScreens(initialScreen='select')

main()