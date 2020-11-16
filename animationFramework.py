# this is the animation framework, or the 'main file' of the project.

from tkinter import *

from JSONGameData import *
from objects import *
from drawingFunctions import *
from NBADotComGameData import *
from imagesSoundsColors import *
from miscHelperFunctions import *
from buttonFunctions import *

####################################
# Animations
####################################

def init(data):
    data.rawJSON = loadData(r'0021500495.json')
    data.eventNum = 1 # start at the beginning
    data.rawMovementData = createDF(data.rawJSON)
    data.coordinates = subsetMovements(data.rawMovementData, data.eventNum)
    data.timerCount = 0
    data.players = []
    data.xScale = data.width / (data.width//10)
    data.yScale = 10
    data.yScalar = 100
    data.gameClock = 0
    data.shotClock = 0
    data.courts = []
    data.gameData = getGameData(data.rawJSON)
    data.splash = True
    data.margin = 100
    data.awayName = data.rawJSON["events"][0]['visitor']['name']
    data.homeName = data.rawJSON["events"][0]['home']['name']
    data.playerData = getPlayerInfo(data.rawJSON)
    # initializing this function downloads all the headshot pngs we need to
    # the current working directory
    data.playerFaces = getAllPlayerFaces(data.playerData, 50)
    data.courtLength = 940
    # epsilon
    data.e = 20
    data.courtHeight = 500
    data.homeColor = getTeamInfo(data.homeName, 'rgb')
    data.awayColor = getTeamInfo(data.awayName, 'rgb')
    data.homeOutline = getTeamInfo(data.homeName, 'num')
    data.awayOutline = getTeamInfo(data.awayName, 'num')
    data.playing = True
    data.boxScore = False
    data.music = playMusic(data)
    data.stats = createBoxScoreDictionary(data.rawJSON, data.eventNum)
    data.homeLogo = getTeamLogo(data.homeName, 50)
    data.awayLogo = getTeamLogo(data.awayName, 50)
    data.logos = []
    data.background = PhotoImage(file=r'harden.png')

def mousePressed(event, data):
    s = data.splash
    x = event.x
    y = event.y
    w = data.width
    h = data.height
    m = data.margin
    e = data.e
    c = data.courtHeight
    if not s:
        # buttons all have the same y
        if y >= m+c+e and y <= h:
            # decrease event num
            if x >= e and x <= w/8+e:
                decreaseEventNum(data)
            # play/pause
            if x >= w/8+e and x <= 2*w/8+e:
                data.playing = not data.playing
            # increase event num
            if x >= 2*w/8+e and x <= 3*w/8+e:
                increaseEventNum(data)
            # skip to specific event
            if x >= 3*w/8+e and x <= 4*w/8+e:
                skip(data)
            # load new game
            if x >= 4*w/8+e and x <= 5*w/8+e:
                loadNewGame(data)
            # stats
            if x >= 5*w/8+e and x <= 6*w/8+e:
                data.boxScore = True
            # speed
            if x >= 6*w/8+e and x <= 7*w/8+e:
                toggleMusic(data)
            # return
            if x >= 7*w/8+e and x <= 8*w/8+e:
                data.splash = not data.splash
            
def redrawAll(canvas, data):
    # splash screen
    if data.splash:
        drawSplash(canvas, data)
    # box score
    elif data.boxScore:
        drawBoxScore(canvas, data)
    else:
        # draw the court
        for court in data.courts:
            court.draw(canvas)
        # draw the players and the ball
        for player in data.players:
            player.draw(canvas)
        # draw supporting graphics
        drawTopRowGraphics(canvas, data)
        drawSideBar(canvas, data)
        drawButtons(canvas, data)

def keyPressed(event, data):
    # return
    if event.keysym == "space":
        data.splash = not data.splash
    # music
    if event.keysym == "m":
        toggleMusic(data)
    # boxscore
    if not data.splash:
        if event.keysym == "b":
            data.boxScore = not data.boxScore
    if not data.splash and not data.boxScore:
        # play/pause
        if event.keysym == "p":
            data.playing = not data.playing
        # next event
        if event.keysym == "Right":
            increaseEventNum(data)
        # previous event
        if event.keysym == "Left":
            decreaseEventNum(data)
        # skip
        if event.keysym == "s":
            skip(data)
        # load new game
        if event.keysym == "l":
            loadNewGame(data)

def timerFired(data):
    # at the beginning
    if data.timerCount == 0:
        # initialize the court
        data.courts.append(Court(data.homeName, data.awayName))
        # initalize the ball and players
        for index in range(11):
            if index == 0:
                assignObject(data, index, "Ball")
            elif index >= 1 and index <= 5:
                assignObject(data, index, data.homeName)
            else:
                assignObject(data, index, data.awayName)
    data.timerCount += 1
    # move the players if unpaused
    if data.playing:
        for player in data.players:
            player.move(data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200, 700)