# this file defines the player and court objects, as well as providing a way
# for the objects to be assigned.

from tkinter import *
from PIL import ImageTk,Image

from imagesSoundsColors import *

# object for the players and ball.
class Player(object):
    
    # initial values
    def __init__(self, x, y, index, jersey, team, first, last):
        self.x = x
        self.y = y
        self.r = 15
        self.index = index
        self.jersey = jersey
        self.team = team
        self.first = first
        self.last = last
        try:
            self.bColor = getTeamInfo(team, 'rgb')
            self.nColor = getTeamInfo(team, 'num')
        except:
            self.bColor = 'black'
            self.nColor = 'white'
        # to make things simple, if a player doesn't have an image in the
        # NBA API, we will plot a 1x1 white pixel.
        try:
            self.image = PhotoImage(file = "resized50"+first+last+".png")
        except:
            self.image = PhotoImage(file = "blank.png")
    
    # movement for the players
    def move(self, data):
        result = []
        for player in data.players:
            # in order to avoid index errors...
            if player.index + 11 < len(data.coordinates):
                # the data is in 11 row chunks (10 players plus the ball).
                # structure allows us to just look 11 rows forward for the
                # next position.
                player.index += 11
            player.x = data.coordinates.at[player.index, 'x']*data.xScale
            player.y = data.coordinates.at[player.index, 'y']*data.yScale + \
            data.yScalar
            player.jersey = data.coordinates.at[player.index, 'jersey']
            result.append(player)
            # update the game and shot clock
            data.gameClock = data.coordinates.at[player.index, 'gameClock']
            data.shotClock = data.coordinates.at[player.index, 'shotClock']
        data.players = result
    
    # draw the players as circles with their jersey number in the middle
    def draw(self, canvas):
        r = self.r
        x = self.x
        y = self.y
        if self.team == "Ball":
            canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'orange')
        else:
            canvas.create_oval(x-r, y-r, x+r, y+r, fill = self.bColor)
            canvas.create_text(x, y, text = str(self.jersey), fill = self.nColor,
                               font = "Arial 12 bold")

# object for the background of the court
class Court(object):
    
    # use a clear image of the court
    def __init__(self, homeName, awayName):
        self.img = ImageTk.PhotoImage(Image.open(r"nba_court_T.png"))
        self.homeLogo = PhotoImage(file = 'resized50'+ \
                                   getTeamInfo(homeName, 'abb')+'.png')
        self.awayLogo = PhotoImage(file = 'resized50'+ \
                                   getTeamInfo(awayName, 'abb')+'.png')
    
    def draw(self, canvas):
        # draw court
        canvas.create_image(0, 100, anchor = NW, image = self.img)
        # draw logos
        canvas.create_image(25, 50, image = self.homeLogo)
        canvas.create_image(850, 50, image = self.awayLogo)

# assigns objects for plotting
def assignObject(data, index, team):
    if team != "Ball":
        data.players.append(Player(data.coordinates.at[index, 'x']*data.xScale,
                                   data.coordinates.at[index, 'y']*data.yScale,
                                   index,
                                   data.coordinates.at[index, 'jersey'],
                                   team,
                                   data.coordinates.at[index, 'firstname'],
                                   data.coordinates.at[index, 'lastname']))
    else:
        data.players.append(Player(data.coordinates.at[index, 'x']*data.xScale,
                                   data.coordinates.at[index, 'y']*data.yScale,
                                   index,
                                   data.coordinates.at[index, 'jersey'],
                                   team, None, None))