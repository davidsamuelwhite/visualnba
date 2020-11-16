# this file grabs information from NBA.com about a specific game. This is done
# in order to grab more information about the game (description, box score).
# it also cleans and organizes this information.

import requests
import pandas as pd

from JSONGameData import *

# ***the code for this function is from the internet***
# https://bit.ly/2H3roeM
# gets raw data from nba.com for a given JSON file. This gives more contextual
# data and helps clear up and clean inconsistencies in the movement data.
def rawGameData(data):
    headers = { #I pulled this header from the py goldsberry library
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'\
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '\
        'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'\
        ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    url = 'http://stats.nba.com/stats/playbyplayv2?' + \
    'EndPeriod=0&EndRange=0&GameID=' + data['gameid'] + \
    '&RangeType=0&StartPeriod=0&StartRange=0'
    response = requests.get(url, headers = headers)
    #get headers of data
    headers = response.json()['resultSets'][0]['headers']
    #get actual data from json object
    gameData = response.json()['resultSets'][0]['rowSet']
    #turn the data into a pandas dataframe
    df = pd.DataFrame(gameData, columns=headers)
    return df

# clean the GameData from nba.com
def cleanGameData(df):
    # only need a few columns
    df = df[[df.columns[1], df.columns[4], df.columns[7], df.columns[9],
             df.columns[10], df.columns[14], df.columns[21], df.columns[28]]]
    # split score column and fill in blank values
    # change the initial score to 0-0
    df.at[0, 'SCORE'] = "0 - 0"
    df[['visitorScore','homeScore']] = df['SCORE'].str.split(' - ',expand=True)
    df['visitorScore'] = df['visitorScore'].fillna(method='ffill')
    df['homeScore'] = df['homeScore'].fillna(method='ffill')
    # merge play descriptions
    df = df.replace([None], [''], regex=True)
    df['description'] = df['HOMEDESCRIPTION'] + df['VISITORDESCRIPTION']
    return df

# wrapper function for data collection
def getGameData(JSON):
    rawData = rawGameData(JSON)
    return cleanGameData(rawData)

# fixes the de-sync between the event number we get from the coordinates and
# the event number in the NBA.com data
def getRowGameData(data, column):
    df = data.gameData[(data.gameData.EVENTNUM == data.eventNum)]
    df = df.reset_index(drop = True)
    return df.at[0, column]

# allocates a dictionary mapping players to their accumulated statistics
def allocateDict(JSON, d, gameData):
    labels = ["PTS", "REB", "AST", "STL", "BLK", "FGM", "FGA",
              "3PM", "3PA", "FTM", "FTA", "PF", "TO"]
    players = getPlayerInfo(JSON)
    for i in range(len(players)):
        name = players.at[i, 'firstname'] + " " + players.at[i, 'lastname']
        d[name] = {}
        d[name]['team'] = players.at[i, 'team']
        for j in range(len(labels)):
            d[name][labels[j]] = 0
    return d

# for every play in the game, assign statistics to the appropriate players
# based on what happened in the play
def assignPlaysToDictionary(JSON, d, stoppingEvent, gameData):
    # we want to accumulate the statistics from the rows up until the current
    # event number
    currentRow = gameData.index[gameData['EVENTNUM']==stoppingEvent].tolist()[0]
    for event in range(1, currentRow+1):
        desc = gameData.at[event, 'description']
        p1Name = gameData.at[event, 'PLAYER1_NAME']
        p2Name = gameData.at[event, 'PLAYER2_NAME']
        p3Name = gameData.at[event, 'PLAYER3_NAME']
        # made layup or dunk
        if ('Layup' in desc or 'Dunk' in desc) and 'MISS' not in desc:
            d[p1Name]['FGA'] += 1
            d[p1Name]['FGM'] += 1
            d[p1Name]['PTS'] += 2
        # assist
        if 'AST' in desc:
            d[p2Name]['AST'] += 1
        # made free throw
        if 'Free Throw' in desc:
            d[p1Name]['FTA'] += 1
            if 'MISS' not in desc:
                d[p1Name]['FTM'] += 1
                d[p1Name]['PTS'] += 1
        # missed shot
        if 'MISS' in desc and 'Free Throw' not in desc:
            d[p1Name]['FGA'] += 1
            # missed three
            if '3PT' in desc:
               d[p1Name]['3PA'] += 1
        # foul
        if 'FOUL' in desc or 'Foul' in desc:
            d[p1Name]['PF'] += 1
        # block
        if 'BLOCK' in desc:
            d[p3Name]['BLK'] += 1
        # made jump shot
        if 'Shot' in desc and 'MISS' not in desc:
            d[p1Name]['FGA'] += 1
            d[p1Name]['FGM'] += 1
            d[p1Name]['PTS'] += 2
            # made 3pt jump shot
            if '3PT' in desc:
                d[p1Name]['3PA'] += 1
                d[p1Name]['3PM'] += 1
                d[p1Name]['PTS'] += 1
        # rebound
        if 'REBOUND' in desc:
            d[p1Name]['REB'] += 1
        # steal
        if 'STEAL' in desc:
            d[p2Name]['STL'] += 1
        # turnover
        if 'Turnover' in desc:
            d[p1Name]['TO'] += 1
    return d

# wrapper function for dictionary statistics
def createBoxScoreDictionary(JSON, stoppingEvent):
    d = {}
    gameData = getGameData(JSON)
    allocateDict(JSON, d, gameData)
    return assignPlaysToDictionary(JSON, d, stoppingEvent, gameData)