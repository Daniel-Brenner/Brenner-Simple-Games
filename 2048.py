from cmu_graphics import *

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
    app.curScore = 0

def boardGen(app):
    res = []
    for _ in range(app.rows):
        newRow = [None] * app.cols
        res.append(newRow)
    return res

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
    drawRect(cellLeft,cellTop,cellWidth,cellHeight,fill=None,border='black')

def getCellLeftTop(app,row,col,cellWidth,cellHeight):
    return app.boardLeft + col * cellWidth,app.boardTop + row * cellHeight

def getCellSize(app):
    return app.boardWidth / app.cols, app.boardHeight/app.rows
    
def drawOutline(app):
    drawRect(app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight,fill=None,border='black',borderWidth=4)

def main():
    runApp()

main()