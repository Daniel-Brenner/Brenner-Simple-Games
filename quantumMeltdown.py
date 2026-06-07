from cmu_graphics import *
import random

def onAppStart(app):
    app.screen = 'home'
    app.homeSelection = 0 # 0 for Play, 1 for Tutorial
    app.rows = 8
    app.cols = 8
    app.boardLeft = 20
    app.boardTop = 80
    app.boardWidth = 360
    app.boardHeight = 360
    resetGame(app)

def resetGame(app):
    app.playerRow = app.rows // 2
    app.playerCol = app.cols // 2
    app.board = [[0]*app.cols for _ in range(app.rows)] # 0 = intact, -1 = void
    app.cores = []
    app.score = 0
    app.turns = 0
    app.gameOver = False
    app.won = False
    app.paused = False
    app.deathReason = ""
    app.targetScore = 25
    spawnCore(app)
    spawnCore(app)

def spawnCore(app):
    emptyCells = []
    for r in range(app.rows):
        for c in range(app.cols):
            if app.board[r][c] == 0 and not isCoreAt(app, r, c) and (r != app.playerRow or c != app.playerCol):
                emptyCells.append((r, c))
                
    if emptyCells:
        r, c = random.choice(emptyCells)
        timer = max(6, 14 - (app.score // 2))
        app.cores.append({'row': r, 'col': c, 'timer': timer})

def isCoreAt(app, r, c):
    for core in app.cores:
        if core['row'] == r and core['col'] == c:
            return True
    return False

def onKeyPress(app, key):
    if app.screen == 'home':
        if key == 'up' or key == 'down':
            app.homeSelection = 1 - app.homeSelection
        elif key == 'enter':
            if app.homeSelection == 0:
                app.screen = 'game'
                resetGame(app)
            else:
                app.screen = 'tutorial'    
    elif app.screen == 'tutorial':
        if key == 'enter' or key == 'escape':
            app.screen = 'home'  
    elif app.screen == 'game':
        if key == 'p' and not app.gameOver and not app.won:
            app.paused = not app.paused
            return
        if key == 'r':
            resetGame(app)
            return  
        if app.paused:
            if key == 'enter':
                app.screen = 'home'
            return
        if app.gameOver or app.won:
            if key == 'enter':
                app.screen = 'home'
            return
        if key in ['up', 'down', 'left', 'right']:
            drow, dcol = 0, 0
            if key == 'up':
                drow = -1
            elif key == 'down':
                drow = 1
            elif key == 'left':
                dcol = -1
            elif key == 'right':
                dcol = 1
            newRow = app.playerRow + drow
            newCol = app.playerCol + dcol
            if 0 <= newRow < app.rows and 0 <= newCol < app.cols:
                if app.board[newRow][newCol] == 0:
                    app.playerRow = newRow
                    app.playerCol = newCol
                    processTurn(app)

def processTurn(app):
    app.turns += 1
    for i in range(len(app.cores)-1, -1, -1):
        c = app.cores[i]
        if c['row'] == app.playerRow and c['col'] == app.playerCol:
            app.score += 1
            app.cores.pop(i)
    if app.score >= app.targetScore:
        app.won = True
        return
    exploded = []
    for i in range(len(app.cores)-1, -1, -1):
        app.cores[i]['timer'] -= 1
        if app.cores[i]['timer'] <= 0:
            exploded.append(app.cores.pop(i))
    for ex in exploded:
        er, ec = ex['row'], ex['col']
        # Destroy the center and adjacent tiles (+)
        for dr, dc in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = er + dr, ec + dc
            if 0 <= nr < app.rows and 0 <= nc < app.cols:
                app.board[nr][nc] = -1    
    for i in range(len(app.cores)-1, -1, -1):
        cr, cc = app.cores[i]['row'], app.cores[i]['col']
        if app.board[cr][cc] == -1:
            app.cores.pop(i)
    if app.board[app.playerRow][app.playerCol] == -1:
        app.gameOver = True
        app.deathReason = "Caught in a Meltdown!"
        return
    trapped = True
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = app.playerRow + dr, app.playerCol + dc
        if 0 <= nr < app.rows and 0 <= nc < app.cols:
            if app.board[nr][nc] == 0:
                trapped = False
    if trapped:
        app.gameOver = True
        app.deathReason = "Trapped in the Void!"
        return
    spawnRate = max(2, 5 - (app.score // 6))
    if app.turns % spawnRate == 0:
        spawnCore(app)
    elif random.random() < 0.15:
        spawnCore(app)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(30, 30, 35))
    if app.screen == 'home':
        drawHome(app)
    elif app.screen == 'tutorial':
        drawTutorial(app)
    elif app.screen == 'game':
        drawGame(app)

def drawHome(app):
    drawLabel('QUANTUM', app.width/2, (100/500) * app.height, size=40, fill='cyan', bold=True, font='monospace')
    drawLabel('MELTDOWN', app.width/2, (145/500) * app.height, size=40, fill='orange', bold=True, font='monospace')
    drawLabel('A Turn-Based Grid Survival Game', app.width/2, (185/400) * app.height, size=14, fill='lightgray')
    playFill = 'darkgreen' if app.homeSelection == 0 else 'gray'
    drawRect(app.width/2, (280/500) * app.height, (160/400) * app.width, (50/500) * app.height, align='center', fill=playFill, border='white')
    drawLabel('PLAY', app.width/2, (280/500) * app.height, size=20, fill='white', bold=True)
    adj = (60/400) * app.width
    if app.homeSelection == 0:
        drawLabel('>', app.width/2 - adj, (280/500) * app.height, size=20, fill='white', bold=True)
    if app.homeSelection == 1:
        tutFill = 'darkblue'
    else:
        tutFill = 'gray'
    drawRect(app.width/2, (350/500) * app.height, (160/400) * app.width, (50/500) * app.height, align='center', fill=tutFill, border='white')
    drawLabel('TUTORIAL', app.width/2, (350/500) * app.height, size=20, fill='white', bold=True)
    if app.homeSelection == 1:
        drawLabel('>', app.width/2 - adj, (350/500) * app.height, size=20, fill='white', bold=True)
    drawLabel('Use ARROW KEYS to select, ENTER to confirm', app.width/2, (450/500) * app.height, size=12, fill='gray')

def drawTutorial(app):
    drawLabel('HOW TO PLAY', app.width/2, (50/500) * app.height, size=24, fill='white', bold=True)
    instructions = [
        "1. You are the cyan circle. Move with ARROW KEYS.",
        "2. Red Cores will spawn on the grid with a timer.",
        "3. Every step you take counts as ONE turn.",
        "4. Timers drop by 1 every turn you take.",
        "5. Step on a Core to collect it and score a point.",
        "6. WARNING: If a Core timer hits 0, it EXPLODES!",
        "7. Explosions destroy the tile and adjacent tiles (+).",
        "8. You cannot step on destroyed (black) tiles.",
        "9. If you are caught in a blast or trapped, you lose.",
        f"10. Collect {app.targetScore} Cores to stabilize the reactor."
    ]
    startY = (100/500) * app.height
    increment = (30/500) * app.height
    for i, line in enumerate(instructions):
        color = 'salmon' if 'WARNING' in line or 'EXPLODES' in line else 'lightgray'
        drawLabel(line, app.width/2, startY + (i * increment), size=13, fill=color)
    drawRect(app.width/2, (430/500) * app.height, (200/400) * app.width, (40/500) * app.height, align='center', fill='darkblue', border='white')
    drawLabel('Press ENTER to return', app.width/2, 430, size=14, fill='white', bold=True)

def drawGame(app):
    drawHeader(app)
    drawGrid(app)
    drawCores(app)
    drawPlayer(app)
    heightAdj = (50/500) * app.height
    if app.paused:
        drawOverlay(app, 'PAUSED', 'P: Resume | ENTER: Home Screen', rgb(0,0,150))
    elif app.won:
        drawOverlay(app, 'SYSTEM STABILIZED!', 'You collected enough cores.', rgb(100,0,180))
        drawLabel('Press R to Restart or ENTER for Home', app.width/2, app.height/2 + heightAdj, size=14, fill='white')
    elif app.gameOver:
        drawOverlay(app, 'MELTDOWN', app.deathReason, rgb(150,0,180))
        drawLabel('Press R to Restart or ENTER for Home', app.width/2, app.height/2 + heightAdj, size=14, fill='white')

def drawHeader(app):
    drawLabel(f'Score: {app.score} / {app.targetScore}', (20/400) * app.width, (40/500) * app.height, size=18, fill='white', align='left', bold=True)
    adj = (20/400) * app.width
    drawLabel(f'Turns: {app.turns}', app.width - adj, (40/500) * app.height, size=16, fill='gray', align='right')
    drawLabel('P: Pause | R: Restart', app.width/2, (15/500) * app.height, size=12, fill='gray')

def getCellBounds(app, row, col):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    x = app.boardLeft + col * cellWidth
    y = app.boardTop + row * cellHeight
    return x, y, cellWidth, cellHeight

def drawGrid(app):
    for r in range(app.rows):
        for c in range(app.cols):
            x, y, cw, ch = getCellBounds(app, r, c)
            if app.board[r][c] == 0:
                drawRect(x, y, cw, ch, fill=rgb(60, 60, 75), border=rgb(40, 40, 50))
            else:
                drawRect(x, y, cw, ch, fill='black', border=rgb(20, 20, 25))

def drawCores(app):
    for core in app.cores:
        r, c = core['row'], core['col']
        x, y, cw, ch = getCellBounds(app, r, c)
        t = core['timer']
        if t > 5:
            color = 'orange'
        elif t > 2:
            color = 'red'
        else:
            color = 'magenta'
        adjX1, adjY1 = (5/400) * app.width, (5/500) * app.height
        adjX2, adjY2 = (10/400) * app.width, (10/500) * app.height
        drawRect(x + adjX1, y + adjY1, cw - adjX2, ch - adjY2, fill=color, border='white', borderWidth=2)
        drawLabel(str(t), x + cw/2, y + ch/2, size=16, fill='white', bold=True)

def drawPlayer(app):
    if not app.gameOver:
        x, y, cw, ch = getCellBounds(app, app.playerRow, app.playerCol)
        drawCircle(x + cw/2, y + ch/2, cw/3, fill='cyan', border='white', borderWidth=2)

def drawOverlay(app, title, subtext, overlayColor):
    adj = (20 / 500) * app.height
    drawRect(0, 0, app.width, app.height, fill=overlayColor)
    drawLabel(title, app.width/2, app.height/2 - adj, size=30, fill='white', bold=True)
    drawLabel(subtext, app.width/2, app.height/2 + adj, size=16, fill='lightgray')

def main():
    runApp(width=400,height=500)

main()