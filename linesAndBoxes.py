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

def boardGen(app):
    res = []
    numExits = 4
    for _ in range(app.dim):
        newRow = []
        for _ in range(app.dim):
            newEntry = []
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
    drawGhostPiece(app)
    # drawGameStatus(app)

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

def drawGhostPiece(app):
    diff = ((app.boardWidth / (app.dim - 1))/400) * app.width
    adj = diff / 3
    for i in range(app.dim):
        y = app.boardTop + diff * i
        for j in range(app.dim):
            x = app.boardLeft + diff * j
            # Check Horizontal Line (to the right of the current dot)
            if j < app.dim - 1:
                if (x <= app.hoverX <= x + diff and 
                    y - adj <= app.hoverY <= y + adj):
                    drawLine(x, y, x + diff, y, lineWidth=6, fill='yellow', opacity=70)
                    return # Exit early once a valid line is found
                    
            # Check Vertical Line (below the current dot)
            if i < app.dim - 1:
                if (x - adj <= app.hoverX <= x + adj and 
                    y <= app.hoverY <= y + diff):
                    drawLine(x, y, x, y + diff, lineWidth=6, fill='yellow', opacity=70)
                    return # Exit early
    return
                    
def game_onMouseMove(app,mouseX,mouseY):
    app.hoverX, app.hoverY = mouseX,mouseY

def game_onMousePress(app,mouseX,mouseY):
    app.hoverX, app.hoverY = app.width, app.height

def main():
    runAppWithScreens(initialScreen='select')

main()