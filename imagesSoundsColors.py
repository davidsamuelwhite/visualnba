# this file contains functions that create and manage all images, sounds and
# colors in the program. Some functions utilize APIs to grab images, other
# do native image manipulation. the 'team' functions give more information
# about each team in order to add some color to the project.

from PIL import ImageTk,Image
from winsound import *
import csv, shutil, requests, winsound

# ***some of the code for this function is adapted from the internet***
# https://bit.ly/2qONMi3
# utilizes api to get headshots of a player
def getPlayerFace(first, last, xsize):
    url = 'https://nba-players.herokuapp.com/players/' + last + '/' + first
    response = requests.get(url, stream=True)
    # saves player face png to working directory
    with open(first + last +'.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    # need image resized
    resizeImage(first+last+".png", xsize)
    del response

# resize headshots for the sidebar into a smaller size (and for the logos!)
def resizeImage(file, xsize):
    size = xsize, xsize
    # some players aren't in the NBA anymore and won't have headshots
    try:
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save("resized"+str(xsize)+file)
    except:
        pass

# download all the player faces who will appear in a game
def getAllPlayerFaces(df, xsize):
    for i in range(len(df)):
        getPlayerFace(df.at[i, 'firstname'], df.at[i, 'lastname'], xsize)
    return None

# creates a dictionary of team information from a csv
def getTeamDict(csvfile):
    with open(csvfile,'rU') as f: 
        reader = csv.reader(f)
        d = {}
        for row in reader:
            d[row[0]] = (row[1], row[2], row[3])
    return d

# grabs info from the created dictionary, where rgb grabs color, abb grabs the
# team abbreviation, and num grabs a color for the number of each circle
# when plotting
def getTeamInfo(teamName, type):
    colorDict = getTeamDict(r'teamcolors.csv')
    if type == "rgb":
        return colorDict[teamName][0]
    if type == "abb":
        return colorDict[teamName][1]
    if type == "num":
        return colorDict[teamName][2]

# creates a set of an aggregate of every team's type of information
def getAllTeamInfo(type):
    info = set()
    dict = getTeamDict(r'teamcolors.csv')
    for key in dict:
        if type == "abb":
            info.add(dict[key][1])
        if type == "name":
            info.add(key)
    return info

# grabs nba team logos from the internet for the top bar
def getTeamLogo(teamName, xsize):
    abb = getTeamInfo(teamName, 'abb')
    url = 'http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/' + \
    'logos/teamlogos_500x500/' + abb + '.png'
    response = requests.get(url, stream=True)
    # saves player face png to working directory
    with open(abb + '.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    # need image resized
    resizeImage(abb+".png", xsize)
    del response

# play the opening music
def playMusic(data):
    data.musicState = True
    PlaySound('basketball.wav', SND_FILENAME|SND_LOOP|SND_ASYNC)

# turn the music on and off, though after intro stops we switch songs
def toggleMusic(data):
    if data.musicState == True:
        PlaySound(None, SND_PURGE)
        data.musicState = False
    else:
        playMusic(data)