# this file holds all the drawing functions in tkinter.

from tkinter import *
from PIL import ImageTk,Image

from NBADotComGameData import *
from miscHelperFunctions import *

# draw the opening splash screen
def drawSplash(canvas, data):
    margin = data.height/10
    canvas.create_image(0, 0, image = data.background, anchor = NW)
    canvas.create_text(data.width/1.3, margin, text = "Visual NBA",
                       fill = 'white', font = "Verdana 30 bold")
    if data.timerCount % 5 != 0:
        canvas.create_text(data.width/2, margin*8, fill = "white",
                        text = "Press Space To View",
                        font = "Verdana 30 bold")
    
# draw the graphics for the top of the application
def drawTopRowGraphics(canvas, data):
    # home team
    canvas.create_text(data.margin, data.margin/8, text = "Home Team",
                       fill = 'black', font = "Arial 16 bold underline",
                       anchor = W)
    canvas.create_text(data.margin/2,data.margin/2, text = data.homeName,
                       fill = data.homeColor, font = "Arial 24 bold",
                       anchor = W)
    # home score
    canvas.create_text(data.width/3.25, data.margin/2, fill = "red",
                       text = getRowGameData(data, 'homeScore'),
                       font = "Arial 24 bold")
    canvas.create_text(data.width/3.25, data.margin/8, fill = "black",
                       text = "Score", font = "Arial 16 bold underline")
    # game clock
    canvas.create_text(data.width/2.5, data.margin/2,
                       text = str(floatToTimer(data.gameClock)),
                       fill = 'black', font = "Arial 24 bold")
    canvas.create_text(data.width/2.5, data.margin/8, text = "Game Clock",
                       fill = 'black', font = "Arial 16 bold underline")
    # shot clock
    canvas.create_text(data.width/1.9, data.margin/2,
                       text = str(data.shotClock),
                       fill = 'black', font = "Arial 24 bold")
    canvas.create_text(data.width/1.9, data.margin/8, text = "Shot Clock",
                       fill = 'black', font = "Arial 16 bold underline")
    # period
    canvas.create_text(data.width/2+(1.75*data.margin), data.margin/2,
                       text = getRowGameData(data, 'PERIOD'),
                       fill = 'black', font = "Arial 24 bold")
    canvas.create_text(data.width/2+(1.75*data.margin), data.margin/8,
                       text = "Period", fill = 'black',
                       font = "Arial 16 bold underline")
    # away team
    canvas.create_text(data.width-data.margin, data.margin/2,
                       text = data.awayName, fill = data.awayColor,
                       font = "Arial 24 bold", anchor = E)
    canvas.create_text(data.width-(1.5*data.margin), data.margin/8, 
                       text = "Visiting Team", fill = 'black',
                       font = "Arial 16 bold underline", anchor = E)
    # away score
    canvas.create_text(data.width-(data.margin/2), data.margin/2, fill = "red",
                       text = getRowGameData(data, 'visitorScore'),
                       font = "Arial 24 bold")
    canvas.create_text(data.width-(data.margin/2),data.margin/8, fill = "black",
                       text = "Score", font = "Arial 16 bold underline")
    # description
    canvas.create_text(0, data.margin/1.25, fill = "black", anchor = W,
                       font = "Arial 12 bold italic", text = "Description: " + \
                       str(getRowGameData(data, 'description')))

# draw the sidebar on the right
def drawSideBar(canvas, data):
    # labels
    canvas.create_text(data.courtLength + data.margin, data.margin/1.2,
                       fill = 'blue', anchor = W, font = "Arial 12 bold",
                       text = "On Court")
    canvas.create_text(data.courtLength + .5*data.margin,data.margin/1.1+data.e,
                       fill = data.homeColor, font = "Arial 12 bold underline",
                       text = data.homeName, anchor = W)
    canvas.create_text(data.courtLength + .5*data.margin,
                       data.margin/1.1+(data.courtHeight/2)+data.e,
                       font = "Arial 12 bold underline",text = data.awayName,
                       fill = data.awayColor, anchor = W)
    # player names, images, number
    drawPlayersSideBar(canvas, data)

# draw the player names, images, number on the sidebar
def drawPlayersSideBar(canvas, data):
    # home team
    # raising a weird error that doesn't crash the program
    try:
        for i in range(1, 6):
            canvas.create_image(data.courtLength+(data.e*1.25),
                                data.margin+(.5*data.e)+(2*data.e*i),
                                image = data.players[i].image)
            canvas.create_text(data.courtLength+(data.e*2.75),
                            data.margin+(.5*data.e)+(2*data.e*i),
                            fill = data.homeColor, font = "Arial 14 bold",
                            text = data.players[i].jersey)
            canvas.create_text(data.courtLength+(.7*data.margin),
                            data.margin+(.5*data.e)+(2*data.e*i),
                            fill = data.homeColor, font = "Arial 14 bold",
                            text = data.players[i].first + " " + \
                            data.players[i].last, anchor = W)
        # away team
        for i in range(6, 11):
            canvas.create_image(data.courtLength+(1.25*data.e),
                                data.margin+(2.75*data.e)+(2*data.e*i),
                                image = data.players[i].image)
            canvas.create_text(data.courtLength+(2.75*data.e),
                            data.margin+(2.75*data.e)+(2*data.e*i),
                            fill = data.awayColor, font = "Arial 14 bold",
                            text = data.players[i].jersey)
            canvas.create_text(data.courtLength+(.7*data.margin),
                            data.margin+(2.75*data.e)+(2*data.e*i),
                            fill = data.awayColor, font = "Arial 14 bold",
                            text = data.players[i].first + " " + \
                            data.players[i].last, anchor = W)
    except:
        pass

# draw the buttons on the bottom of the application
def drawButtons(canvas, data):
    c = canvas
    labels = ["Previous Event", "Play/Pause", "Next Event", "Skip Ahead",
              "Load New Game", "Box Score", "Toggle Music", "Return"]
    for i in range(8):
        c.create_rectangle(i*(data.width/8)+(data.e/2),
                           data.margin+data.courtHeight+(data.e/2),
                           (i+1)*data.width/8-(data.e/2), data.height,
                           width = 3, fill = 'gray77')
        c.create_text(((i*(data.width/8)+(data.e/2))+ \
                        ((i+1)*data.width/8-(data.e/2)))/2,
                        (data.margin+data.courtHeight+(data.e/2)+data.height)/2,
                        fill = "black", text = labels[i],font = "Arial 12 bold")

# draw the box score
def drawBoxScore(canvas, data):
    labels = ["FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "REB", "AST", "PF",
              "STL", "BLK", "TO", "PTS"]
    colors = ['white', 'gray95']
    c = canvas
    # top colored bars
    c.create_rectangle(0, 0, data.width, data.height/30, fill = data.awayColor)
    c.create_rectangle(0, data.height/2, data.width,
                       (data.height/2)+(data.height/30), fill = data.homeColor)
    for i in range(30):
        for j in range(1,14):
            # draw the names on the colored bars, row 0 and 15
            if i == 0:
                c.create_text(data.width/15, (i+.5)*data.height/30,
                              fill = data.awayOutline, text = data.awayName,
                              font = "Arial 12 bold")
                c.create_text(data.width/2, (i+.5)*data.height/30,
                              fill = data.awayOutline, font = "Arial 12 bold",
                              text = "Press b to return!")
                continue
            if i == 15:
                c.create_text(data.width/15, (i+.5)*data.height/30,
                              fill = data.homeOutline, text = data.homeName,
                              font = "Arial 12 bold")
                continue
            # draw name column custom because it has a different size
            c.create_rectangle(0, (i)*(data.height/30), 2*data.width/15,
                               (i+1)*(data.height/30), outline = 'gray77',
                               fill = colors[i%2])
            # draw rest of cells
            c.create_rectangle(data.width/15*(1+j), (i)*(data.height/30),
                               data.width/15*(2+j), (i+1)*(data.height/30),
                               outline = 'gray77', fill = colors[i%2])
            # draw labels for statistical columns
            if i == 1 or i == 16:
                c.create_text(data.width/15, (2*i+1)*(data.height/30)/2,
                              text = "Player Name", font = "Arial 10 bold")
                c.create_text(data.width/15*(1.5+j), (2*i+1)*(data.height/30)/2,
                              text = labels[j-1], font = "Arial 10 bold")
                continue
            # populate cells of box score with statistics from stats dict
            # ***away team***
            if i < 16:
                playerName = list(data.stats.keys())[i-2]
                # start with away team, if we reach a home player, just iterate
                # until we get to i = 16
                if data.stats[playerName]['team'] != data.awayName:
                    continue
                c.create_text(data.width/15, (2*i+1)*(data.height/30)/2,
                              font = "Arial 10", text = playerName)
                c.create_text((j+1)*(data.width/15)+(data.width/30),
                                (2*i+1)*(data.height/30)/2, font = "Arial 10",
                                text = data.stats[playerName][labels[j-1]],
                                anchor = W)
            # ***home team***
            if i > 16:
                # sometimes we run out of players in the dict
                try:
                    playerName = list(data.stats.keys())[i-4]
                except:
                    continue
                c.create_text(data.width/15, (2*i+1)*(data.height/30)/2,
                              font = "Arial 10", text = playerName)
                c.create_text((j+1)*(data.width/15)+(data.width/30),
                                (2*i+1)*(data.height/30)/2, font = "Arial 10",
                                text = data.stats[playerName][labels[j-1]],
                                anchor = W)