#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# frdepartment : mainfile
#!/usr/bin/python

import random
import sys
from optparse import OptionParser
import pygame
from pygame.locals import *

version = "0.1"
usage = "usage: %prog [ --lvl [0-5] | ]"
parser = OptionParser(usage=usage, version="%prog 0.1")

parser.add_option("-m",              help="Number of match",              default=0, action="store", dest="numberOfMatch")
(options, args) = parser.parse_args()

if not options.numberOfMatch:
    # If no lelvel was explicitly choosen by the user, it is automatically set to 0.
    options.numberOfMatch = 16

innitialNumberOfMatch = int(options.numberOfMatch)
currentNumberOfMatch = int(innitialNumberOfMatch)

class borderSize:
    def __init__(self):
        self.top    = 0
        self.bototm = 0
        self.right  = 0
        self.left   = 0

class surfaceInformations:
    def __init__(self):
        self.width  = 0
        self.height = 0
        self.y      = 0
        self.x      = 0
        self.top    = 0
        self.bototm = 0
        self.right  = 0
        self.left   = 0


print("This is Nim " + version +"\n")

def newClassicalGame(remainingMatch):
    numberOfTry=0
    userInput = ""
    while (remainingMatch > 0) or (userInput.lower() == "q"):
        userIsWiner = True
        while (userInput not in [1, 2, 3]) or (userInput > remainingMatch) :
            print("Imput[" + str(remainingMatch) + "/" + str(innitialNumberOfMatch) + "] ", end="")
            userInput = input()
            if userInput == "q":
                print("Quiting the game")
                sys.exit(0)
            try:
                userInput = int(userInput)
            except ValueError:
                print("\"userInput\"" + " is not a valid input.")

            if userInput not in [1, 2, 3]:
                print("Please select a number betwen 1, 2, or 3.")
            elif userInput > remainingMatch:
                print("The remaining match is not enough.", end="")
                if remainingMatch == 3:
                    print(" Please chose a number betwen 1, 2, and 3.")
                if remainingMatch == 2:
                    print(" Please chose a number betwen 1 and 2.")
                if remainingMatch == 1:
                    print(" Your only choice is 1.")

        remainingMatch=remainingMatch-int(userInput)
        userInput = ""

        print("--- " + str(remainingMatch))
        if remainingMatch != 0:
            if remainingMatch%4 != 0:
                computerImput = remainingMatch%4
            else:
                computerImput = random.sample([1, 2, 3],  1)
                computerImput = computerImput[0]

            print("I chose: " + str(computerImput))
            remainingMatch = remainingMatch - computerImput
            print("--- " + str(remainingMatch))
            userIsWiner = False

        numberOfTry+=1

    if userInput.lower == "q":
        quiting = True

    else:
        if userIsWiner:
            winerName="user"
        else:
            winerName="computer"

        print("The " + winerName + " win after " + str(numberOfTry) + " try.")

# Colour deffinitions
background_colour   = (144,124,106)
text_zone_colour    = (81,69,58)
history_area_colour = (69, 59, 49)
indicator_colour    = (70, 60, 50)
red                 = (0, 0, 225)

# Sizes deffinitions
xSize = 640
ySize = 480
textZoneHeigh = 14
matchPicRatio = 11.813186
numberOfInitialMatch = innitialNumberOfMatch
historyAreaWidth = 67
circleRadius = 10
gameAreaDim  = [0,0]
matchAreaDim = [0,0]
matchAreaPos = [0,0]
indicatorDim = [127,55]
matchAreaBorder = borderSize()
matchAreaBorder.top = 40
matchAreaBorder.bottom = 80
matchAreaBorder.left = 40
matchAreaBorder.right = 40

pygame.init()
mainWindow = pygame.display.set_mode((xSize, ySize), RESIZABLE)

programHaveToContinue = True
while programHaveToContinue:
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, RESIZABLE)
        if event.type == QUIT:
            programHaveToContinue = False

    # Redifining variables
    xSize, ySize = mainWindow.get_size()
    gameAreaDim[0] = xSize-historyAreaWidth

    #indicator area variables
    indicatorPosition = ((historyAreaWidth+((xSize-historyAreaWidth)-indicatorDim[0])/2) , ySize-textZoneHeigh-indicatorDim[1])
    indicatorArea = pygame.Surface((indicatorDim[0],indicatorDim[1]))

    # Match area variables
 #  gameAreaDim[1] = ySize-textZoneHeigh-indicatorDim[1]-circleRadius
 #  gameAreaDim[1] = ySize-textZoneHeigh-indicatorDim[1]-circleRadius
 #  maxMatchAreaHeight = gameAreaDim[1]-40
 #  matchAreaDim[0] = gameAreaDim[0]-(gameAreaDim[0]/40)
 #  matchAreaPos[1] = historyAreaWidth+((gameAreaDim[0] - matchAreaDim[0])/2)
 #  matchAreaDim[1] = (matchAreaDim[0]/numberOfInitialMatch)*matchPicRatio
 #  matchAreaPos[0] = ((ySize-textZoneHeigh)/2)-(matchAreaDim[1]/2)
 #  matchAreaPos[0] = ySize-textZoneHeigh-indicatorDim[1]-gameAreaDim[1]+10
 #  matchAreaDim[1] = maxMatchAreaHeight
 #  matchArea = pygame.Surface((matchAreaDim[0], matchAreaDim[1]))


    # Appling variables

    mainWindow.fill(background_colour)

    # Historyzone deffinition
    historyZone = pygame.Surface((historyAreaWidth, ySize))
    historyZone.fill(history_area_colour)
    mainWindow.blit(historyZone, (0, 0))

    # Textzone deffinition
    textZone = pygame.Surface((xSize, textZoneHeigh))
    textZone.fill(text_zone_colour)
    heighTextZonePosition=ySize-textZoneHeigh
    mainWindow.blit(textZone, (0, heighTextZonePosition))

    # Match area deffinition
    #matchArea.fill(red)
    #mainWindow.blit(matchArea, (matchAreaPos[1], matchAreaPos[0]))

    # Indicator area deffinition
    indicatorArea.fill(indicator_colour)
    mainWindow.blit(indicatorArea, (indicatorPosition[0], indicatorPosition[1]))


    indicatorBorderPositionLeft = (int(indicatorPosition[0]+circleRadius),int(indicatorPosition[1]))
    pygame.draw.circle(mainWindow, indicator_colour, (indicatorBorderPositionLeft[0],indicatorBorderPositionLeft[1]), circleRadius)

    indicatorBorderPositionRight = (int(indicatorPosition[0]+indicatorDim[0]-circleRadius),int(indicatorPosition[1]))
    pygame.draw.circle(mainWindow, indicator_colour, (indicatorBorderPositionRight[0],indicatorBorderPositionRight[1]), circleRadius)

    indicatorRadiusCompleterPosition = (indicatorPosition[0]+circleRadius , indicatorPosition[1]-circleRadius)
    indicatorRadiusCompleterDim = (indicatorDim[0]-2*circleRadius,circleRadius)
    indicatorRadiusCompleterArea = pygame.Surface((indicatorRadiusCompleterDim[0],indicatorRadiusCompleterDim[1]))
    indicatorRadiusCompleterArea.fill(indicator_colour)
    mainWindow.blit(indicatorRadiusCompleterArea, (indicatorRadiusCompleterPosition[0], indicatorRadiusCompleterPosition[1]))


    # Matchs deffinition
    maxMatchAreaDim = [xSize-historyAreaWidth-(2*matchAreaBorder.right),ySize-textZoneHeigh-indicatorDim[1]-matchAreaBorder.top-matchAreaBorder.bottom]

    ###################################
    # Test
    matchAreaPos = [historyAreaWidth+matchAreaBorder.left,matchAreaBorder.top]
    testRectangle = pygame.Surface((maxMatchAreaDim[0], maxMatchAreaDim[1]))
    testRectangle.fill(red)
    mainWindow.blit(testRectangle, (matchAreaPos[0], matchAreaPos[1]))
    ###################################


    maxMatchDim = [0,0]
    maxMatchDim[0] = maxMatchAreaDim[0]/numberOfInitialMatch
    maxMatchDim[1] = maxMatchDim[0]*matchPicRatio

    if maxMatchDim[1] > maxMatchAreaDim[1]:
        matchDim = [int(maxMatchAreaDim[1]/matchPicRatio),int(maxMatchAreaDim[1])]
    else:
        matchDim = [int(maxMatchDim[0]),int(maxMatchDim[0]*matchPicRatio)]



    matchAreaDim = [matchDim[0]*numberOfInitialMatch, matchDim[1]]

    matchAreaPos = [historyAreaWidth+matchAreaBorder.left+((maxMatchAreaDim[0]-(matchDim[0]*numberOfInitialMatch))/2),matchAreaBorder.top]
    matchAreaPos = [historyAreaWidth+matchAreaBorder.left+((maxMatchAreaDim[0]-matchAreaDim[0])/2),matchAreaBorder.top]
    maxMatchAreaPos = [historyAreaWidth+matchAreaBorder.left,matchAreaBorder.top]

    i = 0
    matchS = []
    while i < numberOfInitialMatch:
        currentMatchPos=[matchAreaPos[0]+i*matchDim[0],matchAreaPos[1]]
        matchS.append(pygame.image.load("match.png").convert_alpha())
        matchS[i] = pygame.transform.scale(matchS[i], (matchDim[0], matchDim[1]))
        mainWindow.blit(matchS[i], (currentMatchPos[0], currentMatchPos[1]))
        i=i+1

    #####################
    pygame.display.flip()
    #####################

#newClassicalGame(currentNumberOfMatch)

