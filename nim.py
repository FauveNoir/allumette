#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# frdepartment : mainfile
#!/usr/bin/python

import random
import sys
import time
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
        if self.y != 0:
            self.ratio  = self.x/self.y


print("This is Nim " + version +"\n")

# Colour deffinitions
background_colour   = (144,124,106)
text_zone_colour    = (81,69,58)
history_area_colour = (69, 59, 49)
indicator_colour    = (70, 60, 50)
prompt_colour       = (25, 21, 18)
creme_colour        = (236,228,217)
red                 = (225, 0, 0)

# Sizes deffinitions
xSize = 640
ySize = 480
textZoneHeigh = 16
maxPaddingBetwenMatch = 3
matchPicRatio = 11.813186
matchPicRatio = 13.818182
numberOfInitialMatch = innitialNumberOfMatch
if (numberOfInitialMatch  % 2 == 0): #even
    numberOfVoids =0
else: #odd
    numberOfVoids
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
trianglePromptWidth = 7
textUserInput = []
normaUserInput = []

textUserInput = []
normalUserInput = ""
exMode = False
normalMode = True
textToAnalyse = ""
normalTextToAnalyse = ""

allowedMatchDel = ["1", "2", "3"]

pygame.init()
screen = pygame.display.set_mode((xSize, ySize), RESIZABLE)

charInputed = [K_TAB, K_SPACE, K_EXCLAIM, K_QUOTEDBL, K_HASH, K_DOLLAR, K_AMPERSAND, K_QUOTE, K_LEFTPAREN, K_RIGHTPAREN, K_ASTERISK, K_PLUS, K_COMMA, K_MINUS, K_PERIOD, K_SLASH, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_COLON, K_SEMICOLON, K_LESS, K_EQUALS, K_GREATER, K_QUESTION, K_AT, K_LEFTBRACKET, K_BACKSLASH, K_RIGHTBRACKET, K_CARET, K_UNDERSCORE, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS, K_KP_EQUALS]

def makeTextZone():
    # Redifining variables
    xSize, ySize = screen.get_size()

    # Textzone deffinition
    textZone = pygame.Surface((xSize, textZoneHeigh))
    textZone.fill(text_zone_colour)
    heighTextZonePosition=ySize-textZoneHeigh
    screen.blit(textZone, (0, heighTextZonePosition))

    # promptzone deffinition
    promptZoneInfo = surfaceInformations()
    promptZoneInfo.width = historyAreaWidth
    promptZoneInfo.heigh = textZoneHeigh
    promptZone = pygame.Surface((promptZoneInfo.width, promptZoneInfo.heigh))
    promptZone.fill(prompt_colour)
    screen.blit(promptZone, (0, heighTextZonePosition))

    promptTriangle = pygame.draw.polygon(screen, prompt_colour, [[historyAreaWidth,ySize-textZoneHeigh], [historyAreaWidth, ySize], [historyAreaWidth+trianglePromptWidth, ySize-(textZoneHeigh/2)]], 0)

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("monospace", 14)

    # render text
    label = myfont.render("".join(textUserInput), 1, (255,255,255))
    screen.blit(label, (promptZoneInfo.width+trianglePromptWidth+4,heighTextZonePosition))

def analyseTyping():
    global programHaveToContinue
    global textUserInput
    global normalUserInput
    global exMode
    global normalMode
    global textToAnalyse
    global normalTextToAnalyse
    global screen

    keyboardInput = dict()
    keyboardInput["mode"] =  "normal"
    keyboardInput["content"] = ""
    finalNormalUserInput = ""

    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, RESIZABLE)
        if event.type == QUIT:
            programHaveToContinue = False

        if event.type == KEYDOWN:
            if event.unicode == ":":
                exMode = True
            if exMode == True:
                if event.key is K_ESCAPE:
                    exMode = False
                    normalMode = True
                    textUserInput = []
                if event.key in charInputed:
                    textUserInput.append(event.unicode)
                if event.key == K_BACKSPACE and textUserInput != []:
                    del textUserInput[-1]
                    if len(textUserInput) == 1:
                        exMode = False
                        normalMode = True
                        del textUserInput[-1]
                if event.key in [K_RETURN, K_KP_ENTER]:
                    textToAnalyse = "".join(textUserInput[1:])
                    textUserInput = []
                    exMode = False

            if normalMode == True:
            #   if (event.unicode in allowedMatchDel) and (normalUserInput == ""):
            #       normalUserInput = event.unicode
            #   if (event.key in [K_RETURN, K_KP_ENTER]) and (normalUserInput in allowedMatchDel) :
            #       normalTextToAnalyse = normalUserInput
            #       normalUserInput = ""
            #   else:
            #       normalUserInput = event
                if (event.key is K_ESCAPE) and (normalUserInput != []):
                    normalUserInput = []
                elif (event.key is K_ESCAPE) and (normalUserInput == []):
                    finalNormalUserInput = event
                    normalUserInput = []
                elif (event.key not in [K_RETURN, K_KP_ENTER]):
                   #normalUserInput = normalUserInput + event.unicode
                    normalUserInput.append(event.unicode)
                elif (event.key in [K_RETURN, K_KP_ENTER]):
                    finalNormalUserInput = normalUserInput
                    normalUserInput = []


    if textToAnalyse == "about":
        textToAnalyse = ""
        aboutScreen(screen)
    elif textToAnalyse == "quit":
        textToAnalyse = ""
        programHaveToContinue = False
    else:
        keyboardInput["mode"] = "ex"
        keyboardInput["content"] = textToAnalyse

    if finalNormalUserInput != "":
        keyboardInput["mode"] = "normal"
        keyboardInput["content"] = finalNormalUserInput
        finalNormalUserInput = ""
#   elif normalUserInput != []:
#       keyboardInput["mode"] = "normal"
#       keyboardInput["content"] = normalUserInput



    return keyboardInput

def makeTimetZone(beginingOfGame):
    timeZoneInformation = surfaceInformations()
    timeZoneBackground = surfaceInformations()
    xSize, ySize = screen.get_size()

    myfont = pygame.font.SysFont("monospace", 14)

    secondSinceBegining = int(time.time()) - beginingOfGame
    m, s = divmod(secondSinceBegining, 60)
    h, m = divmod(m, 60)
    timePassed = "%02d:%02d" % (m, s)
    print(timePassed)

    heighTextZonePosition=ySize-textZoneHeigh
    timeZoneText = myfont.render(timePassed, 1, (0,0,0))
    timeZoneInformation.width, timeZoneInformation.height = myfont.size(timePassed)
    timeZoneInformation.x = xSize - timeZoneInformation.width
    timeZoneInformation.y = ySize-textZoneHeigh

    timeZoneBackground.width = timeZoneInformation.width+2
    timeZoneBackground.height = textZoneHeigh
    timeZoneBackground.y = heighTextZonePosition
    timeZoneBackground.x = timeZoneInformation.x-2
    timeZoneBackgroundSurface = pygame.Surface((timeZoneBackground.width, timeZoneBackground.height))
    timeZoneBackgroundSurface.fill(creme_colour)


    screen.blit(timeZoneBackgroundSurface, (timeZoneBackground.x, timeZoneBackground.y))
    screen.blit(timeZoneText, (timeZoneInformation.x,timeZoneInformation.y))


normalUserInput = []
def aboutScreen(screen):
    global programHaveToContinue
    global textUserInput
    global normalUserInput
    global exMode
    global normalMode
    global textToAnalyse
    global normalTextToAnalyse

    functionHaveToContinue = True

    keyboardInput = dict()
    keyboardInput["mode"] =  "normal"
    keyboardInput["content"] = ""
    while functionHaveToContinue and programHaveToContinue:
        textToanalyse=analyseTyping()

        if textToanalyse["mode"] == "normal":
            print(textToanalyse["content"])
            if textToanalyse["content"][0] is K_ESCAPE:
                functionHaveToContinue = False

        # Appling variables
        screen.fill(background_colour)
        xSize, ySize = screen.get_size()

        # Illustartion deffinition
        illustrationInformation = surfaceInformations()
        illustration = pygame.image.load("about-illustration.png").convert_alpha()
        illustrationInformation.width,illustrationInformation.height = illustration.get_size()

        illustrationInformationRatio = illustrationInformation.width/illustrationInformation.height

        if illustrationInformation.width > xSize:
            illustrationInformation.width = xSize*(3/4)
            illustrationInformation.height = illustrationInformation.width/illustrationInformationRatio

        if illustrationInformation.height > ySize:
            illustrationInformation.height = ySize*(3/4)
            illustrationInformation.width = illustrationInformation.height*illustrationInformationRatio

        illustrationInformation.y = (ySize-illustrationInformation.height)/2
        illustrationInformation.x = (xSize-illustrationInformation.width)/2

        illustration = pygame.transform.scale(illustration, (int(illustrationInformation.width),int(illustrationInformation.height)))
        screen.blit(illustration, (illustrationInformation.x, illustrationInformation.y))


        makeTextZone()
        #####################
        pygame.display.flip()
        #####################


def trivial(numberOfInitialMatch,screen):
    global programHaveToContinue
    global textUserInput
    global normalUserInput
    global exMode
    global normalMode
    global textToAnalyse
    global normalTextToAnalyse

    allowedEntry=["1","2","3"]

    beginingOfGame = int(time.time())



    functionHaveToContinue = True
    while functionHaveToContinue and programHaveToContinue:
        textToanalyse=analyseTyping()



        # Redifining variables
        xSize, ySize = screen.get_size()
        gameAreaDim[0] = xSize-historyAreaWidth

        #indicator area variables
        indicatorPosition = ((historyAreaWidth+((xSize-historyAreaWidth)-indicatorDim[0])/2) , ySize-textZoneHeigh-indicatorDim[1])
        indicatorArea = pygame.Surface((indicatorDim[0],indicatorDim[1]))


        # Appling variables
        screen.fill(background_colour)

        # Historyzone deffinition
        historyZone = pygame.Surface((historyAreaWidth, ySize))
        historyZone.fill(history_area_colour)
        screen.blit(historyZone, (0, 0))

        # Indicator area deffinition
        indicatorArea.fill(indicator_colour)
        screen.blit(indicatorArea, (indicatorPosition[0], indicatorPosition[1]))


        indicatorBorderPositionLeft = (int(indicatorPosition[0]+circleRadius),int(indicatorPosition[1]))
        pygame.draw.circle(screen, indicator_colour, (indicatorBorderPositionLeft[0],indicatorBorderPositionLeft[1]), circleRadius)

        indicatorBorderPositionRight = (int(indicatorPosition[0]+indicatorDim[0]-circleRadius),int(indicatorPosition[1]))
        pygame.draw.circle(screen, indicator_colour, (indicatorBorderPositionRight[0],indicatorBorderPositionRight[1]), circleRadius)

        indicatorRadiusCompleterPosition = (indicatorPosition[0]+circleRadius , indicatorPosition[1]-circleRadius)
        indicatorRadiusCompleterDim = (indicatorDim[0]-2*circleRadius,circleRadius)
        indicatorRadiusCompleterArea = pygame.Surface((indicatorRadiusCompleterDim[0],indicatorRadiusCompleterDim[1]))
        indicatorRadiusCompleterArea.fill(indicator_colour)
        screen.blit(indicatorRadiusCompleterArea, (indicatorRadiusCompleterPosition[0], indicatorRadiusCompleterPosition[1]))


        # Matchs deffinition
        maxMatchAreaDim = [xSize-historyAreaWidth-(2*matchAreaBorder.right),ySize-textZoneHeigh-indicatorDim[1]-matchAreaBorder.top-matchAreaBorder.bottom]


        maxMatchDim = [0,0]
        maxMatchDim[0] = maxMatchAreaDim[0]/(numberOfInitialMatch*1.5)
        maxMatchDim[1] = maxMatchDim[0]*matchPicRatio

        if maxMatchDim[1] > maxMatchAreaDim[1]:
            matchDim = [int(maxMatchAreaDim[1]/matchPicRatio),int(maxMatchAreaDim[1])]
        else:
            matchDim = [int(maxMatchDim[0]),int(maxMatchDim[0]*matchPicRatio)]



        matchAreaDim = [matchDim[0]*numberOfInitialMatch, matchDim[1]]

        matchAreaPos = [historyAreaWidth+matchAreaBorder.left+((maxMatchAreaDim[0]-matchAreaDim[0])/2),matchAreaBorder.top]
        secondMatchAreaPos = [matchAreaPos[0]+(matchAreaDim[0]-(numberOfInitialMatch*1.5)*matchDim[0])/2,matchAreaPos[1]]

        i = 0
        matchS = []
        while i < numberOfInitialMatch:
            matchLeftVoid = 0
            if i != 0:
                matchLeftVoid = matchDim[0]/2
            currentMatchPos=[secondMatchAreaPos[0]+i*(matchLeftVoid+matchDim[0]),secondMatchAreaPos[1]]
            matchS.append(pygame.image.load("match.png").convert_alpha())
            matchS[i] = pygame.transform.scale(matchS[i], (matchDim[0], matchDim[1]))
            screen.blit(matchS[i], (currentMatchPos[0], currentMatchPos[1]))
            i=i+1

        if textToanalyse in allowedEntry:
            normalTextZone = myfont.render("".join(textToanalyse), 1, (255,255,255))
            screen.blit(normalTextZone, (100,100))


        myfont = pygame.font.SysFont("monospace", 14)
        if textToanalyse["mode"] == "normal":
            print(textToanalyse["content"])
            normalText = myfont.render("".join(textToanalyse["content"]), 1, (255,255,255))
            screen.blit(normalText, (100,100))


        makeTextZone()
        makeTimetZone(beginingOfGame)

        #####################
        pygame.display.flip()
        #####################

    return False

programHaveToContinue = True
def main(variant="trivial", number=numberOfInitialMatch):
    global programHaveToContinue
    while programHaveToContinue:
        if variant == "trivial":
            trivial(number,screen)

main("trivial",numberOfInitialMatch)
