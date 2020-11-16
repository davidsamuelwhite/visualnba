# this file relates to all of the 'buttons' at the bottom of the main plotting
# screen.

from tkinter import filedialog, simpledialog

from JSONGameData import *
from imagesSoundsColors import *
from NBADotComGameData import *

# skips the current event to a given time based on user input
def skip(data):
    # initialize the variables we ask the user for
    data.quarter = -1
    data.minutes = -1
    data.seconds = -1
    # require valid input
    while data.quarter < 1 or data.quarter > 4:
        data.quarter = simpledialog.askinteger("Skip","Enter Quarter:")
    while data.minutes < 0 or data.minutes > 12:
        data.minutes = simpledialog.askinteger("Skip","Enter Minutes:")
    while data.seconds < 0 or data.seconds > 59:
        data.seconds = simpledialog.askinteger("Skip","Enter Seconds:")
        while data.minutes == 0 or data.minutes == 12 and data.seconds != 0:
            data.seconds = simpledialog.askinteger("Skip","Enter Seconds:")
    # given valid input (hitting cancel returns None), recreate the scene
    if None not in [data.quarter, data.minutes, data.seconds]:
        data.players = []
        data.court = []
        data.eventNum = getEventNum(data.rawMovementData, data.quarter,
                                    data.minutes, data.seconds)
        data.coordinates = subsetMovements(data.rawMovementData, data.eventNum)
        # this triggers object creation
        data.timerCount = 0
        data.stats = createBoxScoreDictionary(data.rawJSON, data.eventNum)

# given a time input, find the correct event number so we know where to go
def getEventNum(df, quarter, minutes, seconds):
    time = minutes*60+seconds
    newDF = df[(df.period == quarter) & (df.gameClock > time-0.1) & \
               (df.gameClock < time+0.1)]
    newDF = newDF.reset_index(drop = True)
    return int(newDF.at[0, 'eventID'])

# increase the event number until we find one that has coordinate data
def increaseEventNum(data):
    # make sure we don't try to plot event that doesn't exist
    if data.eventNum + 1 <= data.gameData.at[len(data.gameData)-1, 'EVENTNUM']:
        # clear the court and players
        data.players = []
        data.court = []
        counter = 0
        # some plays have multiple events associated with them. this while loop
        # makes sure that we only see one event from a given play by checking
        # the equality of two adjacent events. it also
        # ensures that we don't choose an event with no movement data.
        while counter == 0 or len(subsetMovements(data.rawMovementData,
        data.eventNum)) == 0 or len(subsetMovements(data.rawMovementData,
        data.eventNum)) == len(subsetMovements(data.rawMovementData,
        data.eventNum-1)):
            counter += 1
            data.eventNum += 1
        data.coordinates = subsetMovements(data.rawMovementData, data.eventNum)
        # set the timer to 0 in order to be able to redraw objects in tFired
        data.timerCount = 0
        data.stats = createBoxScoreDictionary(data.rawJSON, data.eventNum)

# increase the event number until we find one that has coordinate data
def decreaseEventNum(data):
    # make sure we don't try to plot event that doesn't exist
    if data.eventNum - 1 >= 1:
        # clear the court and players
        data.players = []
        data.court = []
        counter = 0
        # some plays have multiple events associated with them. this while loop
        # makes sure that we only see one event from a given play by checking
        # the equality of two adjacent events. it also
        # ensures that we don't choose an event with no movement data. 
        while counter == 0 or len(subsetMovements(data.rawMovementData,
        data.eventNum)) == 0 or len(subsetMovements(data.rawMovementData,
        data.eventNum)) == len(subsetMovements(data.rawMovementData,
        data.eventNum-1)):
            counter += 1
            data.eventNum -= 1
        data.coordinates = subsetMovements(data.rawMovementData, data.eventNum)
        # set the timer to 0 in order to be able to redraw objects in tFired
        data.timerCount = 0
        data.stats = createBoxScoreDictionary(data.rawJSON, data.eventNum)

# load a new game from a JSON file. big reset!
def loadNewGame(data):
    # ask user for file
    newJSON = filedialog.askopenfilename(initialdir = "/",title = "Select file",
                                  filetypes = (("JSON files","*.json"),
                                  ("all files","*.*")))
    # reinitialize values for new game
    # some values are set to None before they are re-initialized in order
    # to conserve memory
    data.rawJSON = None
    data.rawJSON = loadData(newJSON)
    data.eventNum = 1 # start at the beginning
    data.rawMovementData = None
    data.rawMovementData = createDF(data.rawJSON)
    data.coordinates = None
    data.coordinates = subsetMovements(data.rawMovementData, data.eventNum)
    data.timerCount = 0
    data.players = []
    # setting these to None raised an error
    data.gameClock = 0
    data.shotClock = 0
    data.courts = []
    data.gameData = None
    data.gameData = getGameData(data.rawJSON)
    data.awayName = data.rawJSON["events"][0]['visitor']['name']
    data.homeName = data.rawJSON["events"][0]['home']['name']
    data.playerData = None
    data.playerData = getPlayerInfo(data.rawJSON)
    # initializing this function downloads all the headshot pngs we need to
    # the current working directory
    data.playerFaces = getAllPlayerFaces(data.playerData)
    data.homeColor = getTeamInfo(data.homeName, 'rgb')
    data.awayColor = getTeamInfo(data.awayName, 'rgb')
    data.homeLogo = getTeamLogo(data.homeName, 50)
    data.awayLogo = getTeamLogo(data.awayName, 50)
    data.stats = createBoxScoreDictionary(data.rawJSON, data.eventNum)
    data.homeOutline = getTeamInfo(data.homeName, 'num')
    data.awayOutline = getTeamInfo(data.awayName, 'num')