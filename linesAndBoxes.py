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

################################################
#__selectScreen___
################################################

def select_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='maroon')
    drawLabel('Welcome to Lines and Boxes!',app.width/2,(1/4)*app.height,size=24,bold=True,fill='yellow')
    circleRadius = 30
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

def select_onKeyPress(app,key):
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

def main():
    runAppWithScreens(initialScreen='select')

main()