from cmu_graphics import *

def onAppStart(app):
    resetApp(app)

def resetApp(app):
    app.p1ColorSelected = False
    app.colors = ['red','orange','yellow','green','blue','indigo','violet']
    app.colorSelectIndex = 0
    app.p1Color = None
    app.p2Color = None
    app.dim = 7
    app.colorSelectDone = False
    app.gridSizeSelectDone = False
    app.instruction = False

################################################
#__selectScreen___
################################################

def select_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='maroon')
    drawLabel('Welcome to Lines and Boxes!',app.width/2,(1/4)*app.height,size=24,bold=True,fill='yellow')
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
    if app.colorSelectDone:
        drawSmallDots(app)
    if app.instruction:
        drawInstruction(app)

def drawSmallDots(app):
    squareOffset = (30/400) * app.width
    squareSize = squareOffset * 2
    difference = squareSize / app.dim
    squareCenterX,squareCenterY = (3/4)*app.width,(3/4)*app.height
    squareLeft,squareTop = squareCenterX - squareOffset,squareCenterY - squareOffset
    smallDotRadius = (1/400) * app.width
    for i in range(app.dim):
        x = squareLeft + i * difference
        for j in range(app.dim):
            y = squareTop + j * difference
            drawCircle(x,y,smallDotRadius)

def drawInstruction(app):
    allInstructions = ['Instructions for Lines and Boxes!',
                       '',
                       "press 'i' to exit instructions",
                       'left and right arrow keys to select',
                       'enter key to advance to next step',
                       'move mouse over line that you want to place',
                       'click to place the ghost piece',
                       'score by placing the line that completes a box',
                       'if you score, you get another turn, else opponent gets turn',
                       'game is over when all boxes are filled',
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
                if app.dim == 10:
                    app.dim = 4
                else:
                    app.dim += 1
            elif key == 'left':
                if app.dim == 4:
                    app.dim = 10
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
    drawRect(10,10,10,10)

def main():
    runAppWithScreens(initialScreen='select')

main()