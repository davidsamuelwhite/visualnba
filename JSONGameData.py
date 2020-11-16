# this file contains functions that manipulate the data from the JSON file which
# holds all the data that is plotted by the program. it creates objects called
# dataframes from the pandas packages, which are essentially 2d lists that are
# easier to data manipulation with.

import json
import pandas as pd

# disables warnings from pandas package. cleans the console
pd.options.mode.chained_assignment = None 

# load data from a JSON file
def loadData(file):
    JSON = open(file)
    return json.load(JSON)

# get the info about the players in a game, and create a dataframe
def getPlayerInfo(JSON):
    # row headers
    playerColumns = JSON["events"][0]["home"]["players"][0].keys()
    # home, then away team info
    homePlayers = pd.DataFrame(data = [home for home in \
    JSON["events"][0]["home"]["players"]], columns = playerColumns)
    visitingPlayers = pd.DataFrame(data = [visitor for visitor in \
    JSON["events"][0]["visitor"]["players"]], columns = playerColumns)
    # rename and add some columns
    homePlayers.rename(columns = {'playerid':'playerID'}, inplace = True)
    visitingPlayers.rename(columns = {'playerid':'playerID'}, inplace = True)
    homePlayers['team'] = JSON["events"][0]['home']['name']
    visitingPlayers['team'] = JSON["events"][0]['visitor']['name']
    # merge together
    df = pd.merge(visitingPlayers, homePlayers, how='outer')
    # delete for memory conservation
    del homePlayers
    del visitingPlayers
    df = df.drop(columns = ['position'])
    return df

# create a dataframe of the movement data of a whole game
# output will be roughly 2,000,000 rows
def getMovementInfo(JSON):
    final = []
    # hierarchy of info: JSON --> events --> moments
    for event in JSON['events']:
        eventID = event['eventId']
        for moment in event['moments']:
            # moment[5] is a 11x5 matrix of movement info for all 10 players
            # on the court along with the ball
            for entity in moment[5]:
                entity.extend((eventID, moment[0], moment[2], moment[3]))
                final.append(entity)
    columns = ["teamID", "playerID", "x", "y", "radius", "eventID", "period", \
    "gameClock", "shotClock"]
    df = pd.DataFrame(final, columns = columns)
    # delete the list and some columns to save memoery
    del final
    df = df.drop(columns = ['teamID', 'radius'])
    return df

# merge the player data to each row of movement so we know who exactly is moving
def mergePlayerAndMovement(df, players):
    # we create an index to sort by because the original order of the movement
    # data is important and needs to be preserved. merging by default loses
    # the order
    df['index'] = range(len(df))
    df = pd.merge(df, players, how = 'outer')
    df = df.sort_values('index')
    df = df.reset_index(drop=True)
    return df

# takes the raw JSON data and creates a tidy dataframe for plotting
def createDF(JSON):
    players = getPlayerInfo(JSON)
    movement = getMovementInfo(JSON)
    df = mergePlayerAndMovement(movement, players)
    df.shotClock = df.shotClock.fillna('')
    del players
    del movement
    return df

# subset the tidy movement dataframe by a specific event we wish to plot
def subsetMovements(df, eventNum):
    newDF = df[df.eventID == str(eventNum)]
    newDF = newDF.reset_index(drop=True)
    return newDF