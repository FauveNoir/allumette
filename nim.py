#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
import time
import re
from optparse import OptionParser
import pygame
from pygame.locals import *

version = "0.1"
usage = "usage: %prog [ --lvl [0-5] | ]"
parser = OptionParser(usage=usage, version="%prog 0.1")

parser.add_option("-m",              help="Number of match",
                  default=0, action="store", dest="numberOfMatch")
(options, args) = parser.parse_args()

if not options.numberOfMatch:
    # If no lelvel was explicitly choosen by the user, it is automatically set
    # to 0.
    options.numberOfMatch = 16

innitialNumberOfMatch = int(options.numberOfMatch)
currentNumberOfMatch = int(innitialNumberOfMatch)


class borderSize:

    def __init__(self):
        self.top = 0
        self.bototm = 0
        self.right = 0
        self.left = 0


class surfaceInformations:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.y = 0
        self.x = 0
        self.top = 0
        self.bototm = 0
        self.right = 0
        self.left = 0
        if self.y != 0:
            self.ratio = self.x / self.y


class whatToDo:

    def __init__(self):
        self.programHaveToContinue = True
        self.variant = "trivial"
        self.number = numberOfInitialMatch
        self.wtw = "ttl"


print("This is Nim " + version + "\n")

# Colour deffinitions
background_colour = (144, 124, 106)
text_zone_colour = (81, 69, 58)
history_area_colour = (69, 59, 49)
indicator_colour = (70, 60, 50)
prompt_colour = (25, 21, 18)
creme_colour = (236, 228, 217)
yellow_colour = (205, 153, 29)
winingMainText_colour = (236, 232, 228)
red = (225, 0, 0)



class variants:
    def __init__(self):
        self.name = ""
        self.number = 15
        self.wtw = "ttl"

trivial = variants()
trivial.name = "Trivial"
trivial.number = 16
trivial.wtw = "ttl"

marienbad = variants()
marienbad.name = "Marienbad"
marienbad.number = 5
marienbad.wtw = "ttl"

knowenVarients = [trivial, marienbad]
viarentNames = []
for varientRow in knowenVarients:
    viarentNames.append(varientRow.name)



# Sizes deffinitions
xSize = 640
ySize = 480
textZoneHeigh = 16
maxPaddingBetwenMatch = 3
matchPicRatio = 6.925
numberOfInitialMatch = innitialNumberOfMatch
historyAreaWidth = 67
circleRadius = 10
gameAreaDim = [0, 0]
matchAreaDim = [0, 0]
matchAreaPos = [0, 0]
indicatorDim = [127, 55]
matchAreaBorder = borderSize()
matchAreaBorder.top = 40
matchAreaBorder.bottom = 80
matchAreaBorder.left = 40
matchAreaBorder.right = 40
trianglePromptWidth = 7
textUserInput = []
normaUserInput = []

textUserInput = []
normalUserInput = []
exMode = False
normalMode = True
textToAnalyse = ""
normalTextToAnalyse = ""

allowedMatchDel = ["1", "2", "3"]

pygame.init()
screen = pygame.display.set_mode((xSize, ySize), RESIZABLE)

charInputed = [K_TAB, K_SPACE, K_EXCLAIM, K_QUOTEDBL, K_HASH, K_DOLLAR, K_AMPERSAND, K_QUOTE, K_LEFTPAREN, K_RIGHTPAREN, K_ASTERISK, K_PLUS, K_COMMA, K_MINUS, K_PERIOD, K_SLASH, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_COLON, K_SEMICOLON, K_LESS, K_EQUALS, K_GREATER, K_QUESTION,
               K_AT, K_LEFTBRACKET, K_BACKSLASH, K_RIGHTBRACKET, K_CARET, K_UNDERSCORE, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS, K_KP_EQUALS]


def makeTextZone(nameToDisplay):
    # Redifining variables
    xSize, ySize = screen.get_size()

    # Textzone deffinition
    textZone = pygame.Surface((xSize, textZoneHeigh))
    textZone.fill(text_zone_colour)
    heighTextZonePosition = ySize - textZoneHeigh
    screen.blit(textZone, (0, heighTextZonePosition))

    # promptzone deffinition
    promptFont = pygame.font.SysFont("monospace", 14, bold=True)
    textSizeWidth, textSizeHeight = promptFont.size(nameToDisplay)
    promptZoneInfo = surfaceInformations()
    promptZoneInfo.width = textSizeWidth + 8
    promptZoneInfo.heigh = textZoneHeigh
    promptZone = pygame.Surface((promptZoneInfo.width, promptZoneInfo.heigh))
    promptZone.fill(prompt_colour)
    promptText = promptFont.render(nameToDisplay, 1, (205, 153, 29))
    textSizeWidth, textSizeHeight = promptFont.size(nameToDisplay)
    screen.blit(promptZone, (0, heighTextZonePosition))
    screen.blit(promptText, (4, heighTextZonePosition + 1))

    promptTriangle = pygame.draw.polygon(screen, prompt_colour, [[promptZoneInfo.width, ySize - textZoneHeigh], [
                                         promptZoneInfo.width, ySize], [promptZoneInfo.width + trianglePromptWidth, ySize - (textZoneHeigh / 2)]], 0)

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not
    # Initialized' error
    myfont = pygame.font.SysFont("monospace", 14)

    # render text
    label = myfont.render("".join(textUserInput), 1, (255, 255, 255))
    screen.blit(label, (promptZoneInfo.width +
                        trianglePromptWidth + 4, heighTextZonePosition))

finalNormalUserInput = ""


def analyseTyping(variant, numberOfInitialMatch, wtw):
    global programHaveToContinue
    global textUserInput
    global normalUserInput
    global exMode
    global normalMode
    global textToAnalyse
    global normalTextToAnalyse
    global screen
    global finalNormalUserInput
    global generalState

    keyboardInput = dict()
    keyboardInput["mode"] = "normal"
    keyboardInput["content"] = ""

    functionHaveToContinue = True
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, RESIZABLE)
        if event.type == QUIT:
            programHaveToContinue = False

        if event.type == KEYDOWN:
            if (event.unicode == ":") and ("".join(normalUserInput) == ""):
                exMode = True
                normalMode = False
            if exMode == True:
                if event.key is K_ESCAPE:
                    exMode = False
                    normalMode = True
                    textUserInput = []
                elif event.key in charInputed:
                    textUserInput.append(event.unicode)
                elif event.key == K_BACKSPACE and textUserInput != []:
                    del textUserInput[-1]
                    if len(textUserInput) == 1:
                        exMode = False
                        normalMode = True
                        del textUserInput[-1]
                elif event.key in [K_RETURN, K_KP_ENTER]:
                    textToAnalyse = "".join(textUserInput[1:])
                    textUserInput = []
                    exMode = False
                if textUserInput == []:
                    exMode = False
                    normalMode = True

            elif normalMode == True:
                if (event.key is K_ESCAPE) and (normalUserInput != []):
                    normalUserInput = []
                elif (event.key is K_ESCAPE) and (normalUserInput == []):
                    normalUserInput = []
                    keyboardInput["mode"] = "escape"
                elif (event.key not in [K_RETURN, K_KP_ENTER, K_ESCAPE]):
                    normalUserInput.append(event.unicode)
                elif (event.key in [K_RETURN, K_KP_ENTER]):
                    finalNormalUserInput = "".join(normalUserInput)
                    normalUserInput = []

    if textToAnalyse == "about":
        textToAnalyse = ""
        aboutScreen(screen)
    elif textToAnalyse in ["quit", "q"]:
        textToAnalyse = ""
        programHaveToContinue = False
#    elif textToAnalyse in ["new", "n"]:
    #elif re.match("n(ew| *)?$", textToAnalyse) is not None:
    elif re.match("n(ew)?( +((trivial)|(marienbad)))?( +[0-9]*)?( +(((ttl)|(take-the-last))|((ltl)|(let-the-last))))? *$", textToAnalyse) is not None:
        programHaveToContinue = True
        functionHaveToContinue = False

        syntaxToExtractOptions = "n(ew)?( +(?P<variente>(trivial|marienbad)))?( +(?P<number>[0-9]*))?( +(?P<wtw>((ttl)|(ltl))))?"
        newGameOptions = re.match(syntaxToExtractOptions,textToAnalyse)
        textToAnalyse = ""

        print("machin")
        type(newGameOptions.group("variente"))
        if (newGameOptions.group("variente") == None) :
            generalState.variant = variant
        else:
            generalState.variant = newGameOptions.group("variente")

        if ( newGameOptions.group("number") == None) :
            generalState.number = numberOfInitialMatch
        else:
            generalState.number = int(newGameOptions.group("number"))

        generalState.wtw = wtw
    elif keyboardInput["mode"] == "escape":
        keyboardInput["mode"] = "escape"
    else:
        keyboardInput["mode"] = "ex"
        keyboardInput["content"] = textToAnalyse

    if normalUserInput != []:
        keyboardInput["mode"] = "normal"
        keyboardInput["content"] = normalUserInput

    return functionHaveToContinue, keyboardInput


def makeTimetZone(beginingOfGame):
    timeZoneInformation = surfaceInformations()
    timeZoneBackground = surfaceInformations()
    timeZoneInformation.left = 2
    timeZoneInformation.right = 2

    xSize, ySize = screen.get_size()

    myfont = pygame.font.SysFont("monospace", 14)

    secondSinceBegining = int(time.time()) - beginingOfGame
    m, s = divmod(secondSinceBegining, 60)
    h, m = divmod(m, 60)
    timePassed = "%02d:%02d" % (m, s)

    heighTextZonePosition = ySize - textZoneHeigh
    timeZoneText = myfont.render(timePassed, 1, (0, 0, 0))
    timeZoneInformation.width, timeZoneInformation.height = myfont.size(
        timePassed)
    timeZoneInformation.x = xSize - timeZoneInformation.width - timeZoneInformation.left
    timeZoneInformation.y = ySize - textZoneHeigh

    timeZoneBackground.width = timeZoneInformation.width + \
        (timeZoneInformation.left + timeZoneInformation.right)
    timeZoneBackground.height = textZoneHeigh
    timeZoneBackground.y = heighTextZonePosition
    timeZoneBackground.x = timeZoneInformation.x - 2
    timeZoneBackgroundSurface = pygame.Surface(
        (timeZoneBackground.width, timeZoneBackground.height))
    timeZoneBackgroundSurface.fill(creme_colour)

    screen.blit(timeZoneBackgroundSurface,
                (timeZoneBackground.x, timeZoneBackground.y))
    screen.blit(timeZoneText, (timeZoneInformation.x, timeZoneInformation.y))
    timeZoneBorder = pygame.draw.polygon(screen, yellow_colour, [[timeZoneBackground.x, timeZoneBackground.y], [timeZoneBackground.x, timeZoneBackground.y + timeZoneBackground.height - 2], [
                                         timeZoneBackground.x + timeZoneBackground.width - 2, timeZoneBackground.y + timeZoneBackground.height - 2], [timeZoneBackground.x + timeZoneBackground.width - 2, timeZoneBackground.y]], 2)

    return timeZoneBackground.width


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
    keyboardInput["mode"] = "normal"
    keyboardInput["content"] = ""
    while functionHaveToContinue and programHaveToContinue:
        functionHaveToContinue, textToanalyse = analyseTyping(None, None, None)

        if textToanalyse["mode"] == "escape":
            functionHaveToContinue = False

        # Appling variables
        screen.fill(background_colour)
        xSize, ySize = screen.get_size()

        # Illustartion deffinition
        illustrationInformation = surfaceInformations()
        illustration = pygame.image.load(
            "about-illustration.png").convert_alpha()
        illustrationInformation.width, illustrationInformation.height = illustration.get_size()

        illustrationInformationRatio = illustrationInformation.width / \
            illustrationInformation.height

        if illustrationInformation.width > xSize:
            illustrationInformation.width = xSize * (3 / 4)
            illustrationInformation.height = illustrationInformation.width / \
                illustrationInformationRatio

        if illustrationInformation.height > ySize:
            illustrationInformation.height = ySize * (3 / 4)
            illustrationInformation.width = illustrationInformation.height * \
                illustrationInformationRatio

        illustrationInformation.y = (
            ySize - illustrationInformation.height) / 2
        illustrationInformation.x = (xSize - illustrationInformation.width) / 2

        illustration = pygame.transform.scale(illustration, (int(
            illustrationInformation.width), int(illustrationInformation.height)))
        screen.blit(illustration, (illustrationInformation.x,
                                   illustrationInformation.y))

        makeTextZone("About")
        #####################
        pygame.display.flip()
        #####################


def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def playTrivial(currentMatchNumber):
    if currentMatchNumber != 0:
        numberOfMatchToDel = 0
        if currentMatchNumber >= 3:
            authorisedNumbers = [3, 2, 1]
        elif currentMatchNumber == 2:
            authorisedNumbers = [2, 1]
        elif currentMatchNumber == 1:
            authorisedNumbers = [1]

        if ((currentMatchNumber - 1) % 4) == 0:
            numberComputerHaveToDel = 1
        elif ((currentMatchNumber - 2) % 4) == 0:
            numberComputerHaveToDel = 2
        elif ((currentMatchNumber - 3) % 4) == 0:
            numberComputerHaveToDel = 3
        else:
            numberComputerHaveToDel = random.randint(1, 3)

        answer = numberComputerHaveToDel
    else:
        answer = 0

    return answer


def trivialAnalysis(currentMatchNumber, initialMatchNumber, wtw, userInput):
    if currentMatchNumber != 0:
        numberOfMatchToDel = 0

        if currentMatchNumber >= 3:
            authorisedNumbers = [3, 2, 1]
        elif currentMatchNumber == 2:
            authorisedNumbers = [2, 1]
        elif currentMatchNumber == 1:
            authorisedNumbers = [1]

        if list(userInput)[0] == "=":
            action = "application"
            stringToEvaluate = userInput[1:]
        elif list(userInput)[0] == "-":
            action = "soustraction"
            stringToEvaluate = userInput[1:]
        else:
            action = "soustraction"
            stringToEvaluate = userInput

        if representsInt(stringToEvaluate):
            if action == "soustraction":
                numberOfMatchToDel = int(stringToEvaluate)
            elif action == "application":
                numberOfMatchToDel = currentMatchNumber - int(stringToEvaluate)
        else:
            answer = [False, "“" + userInput + "” is not a valid syntax."]

        if numberOfMatchToDel != 0:
            if numberOfMatchToDel in authorisedNumbers:
                numberLetByUser = initialMatchNumber - numberOfMatchToDel
                answer = [True, numberLetByUser, numberOfMatchToDel]
            else:
                answer = [False, "“" +
                          str(numberOfMatchToDel) + "” is too big."]
        elif (numberOfMatchToDel == 0):
            answer = [False, "“0” is not a valid answer."]

    else:
        answer = [True, 0, 0]
    return answer


def winingFallingScreenMatchExplosion(winer, variant, numberOfInitialMatch, time):
    xSize, ySize = screen.get_size()

    if winer == True:
        matchInformation = surfaceInformations()
        matchS = []
        match = 0
        while match < 1000:
            matchS.append(pygame.image.load(
                "match-animation.png").convert_alpha())
            matchInformation.heigh = random.randint(0, ySize)
            matchInformation.weight = random.randint(0, xSize)
            rotation = random.randint(0, 360)
            matchS[match] = pygame.transform.rotate(matchS[match], rotation)
            screen.blit(
                matchS[match], (matchInformation.weight, matchInformation.heigh))
            match = match + 1
    elif winer == False:
        print("machin")

def formateSecondToDotedTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h == 0:
        formatedTime = "%02d:%02d" % (m, s)
    else:
        formatedTime = "%02d:%02d:%02d" % (h, m, s)

    return formatedTime

def winingFallingScreen(winer, variant, numberOfInitialMatch, time):
    global indicator_colour
    global winingMainText_colour
    lineSeparationColor = (205, 153, 29)
    helpText_color = (163, 143, 125)
    xSize, ySize = screen.get_size()

    time = formateSecondToDotedTime(time)

    if winer == True:

        winingTextInfo = surfaceInformations()
        winingTimeTextInfo = surfaceInformations()
        winingHelpTextInfo = surfaceInformations()


        print("machin")
        screen.fill(indicator_colour)

        # Bliting the text "You win"
        winingFont = pygame.font.SysFont("CMU Typewriter Text", 44, bold=True)
        winingText = winingFont.render("You win!", 1, winingMainText_colour)
        winingTextInfo.width, winingTextInfo.height = winingFont.size("You win!")
        winingTextInfo.x = (xSize - winingTextInfo.width) / 2
        winingTextInfo.y = 40
        screen.blit(winingText, (winingTextInfo.x, winingTextInfo.y))

        # Bliting the time passed
        winingTimeFont = pygame.font.SysFont("CMU Typewriter Text", 137, bold=True)
        winingTimeText = winingTimeFont.render(time, 1, lineSeparationColor)
        winingTimeTextInfo.width, winingTimeTextInfo.height = winingTimeFont.size(time)
        winingTimeTextInfo.x = (xSize - winingTimeTextInfo.width) / 2
        winingTimeTextInfo.y = 90
        screen.blit(winingTimeText, (winingTimeTextInfo.x, winingTimeTextInfo.y))

        # Bliting help text
        helpText = "Type :new to begin new game or :help for more options."
        winingHelpFont = pygame.font.SysFont("CMU Typewriter Text", 23, bold=True)
        winingHelpText = winingHelpFont.render(helpText, 1, helpText_color)
        winingHelpTextInfo.width, winingHelpTextInfo.height = winingHelpFont.size(helpText)
        winingHelpTextInfo.x = (xSize - winingHelpTextInfo.width) / 2
        winingHelpTextInfo.y = ySize-90
        screen.blit(winingHelpText, (winingHelpTextInfo.x, winingHelpTextInfo.y))

    elif winer == False:
        print("machin")

def printListOfTry(screen, listOfTry):
    historyFont = pygame.font.SysFont("monospace", 14, bold=True)
    pageUpDownFont = pygame.font.SysFont("monospace", 18, bold=True)
    pageUpDownColor = (220, 36, 4)
    lineSeparationColor = (205, 153, 29)
    realLineSeparationPlayed = (54,46,38)
    xSize, ySize = screen.get_size()
    arrowBackground = []
    row = 0
    arrowPosX = 40
    delledNumberPosX = 53

    historyZone = pygame.Surface((historyAreaWidth, ySize))
    historyZone.fill(history_area_colour)
    screen.blit(historyZone, (0, 0))

    scroowlingHistory = 0

    while row < len(listOfTry):
        if (row % 2 == 0):  # even
            row_coulour = (234, 226, 215)
            arrowSign = "←"
        else:  # odd
            row_coulour = (207, 194, 184)
            arrowSign = "→"

        if listOfTry[row] == 1:
            numberToDelColor = (0, 126, 223)
        if listOfTry[row] == 2:
            numberToDelColor = (40, 149, 0)
        if listOfTry[row] == 3:
            numberToDelColor = (215, 0, 95)

        print("This row: " + str(row))
        arrowBackground.append(pygame.Surface(
            (historyAreaWidth, textZoneHeigh)))
        print(len(arrowBackground))
        arrowBackground[row].fill(row_coulour)

        rowPosY = ySize - textZoneHeigh - \
            (len(listOfTry) - row) * textZoneHeigh

        historyNumberText = historyFont.render(str(row), 1, (0, 0, 0))
        historyArrowText = historyFont.render(arrowSign, 1, (0, 0, 0))
        numberDelledText = historyFont.render(
            str(listOfTry[row]), 1, numberToDelColor)

        screen.blit(arrowBackground[row], (0, rowPosY))
        screen.blit(historyNumberText, (2, rowPosY + 2))
        screen.blit(historyArrowText, (arrowPosX, rowPosY + 2))
        screen.blit(numberDelledText, (delledNumberPosX, rowPosY + 2))
        row = row + 1
        print("It success")

    print(len(listOfTry))
    print("textZoneHeigh: " + str(textZoneHeigh))
    realHistoryHeigh = (len(listOfTry) + 1) * textZoneHeigh
    print(realHistoryHeigh, ySize)

    lineHistorySeparation = pygame.Surface((1, ySize))
    lineHistorySeparation.fill(lineSeparationColor)
    screen.blit(lineHistorySeparation, (35, 0))

    realLineHistorySeparation = pygame.Surface((1, realHistoryHeigh))
    realLineHistorySeparation.fill(realLineSeparationPlayed)
    screen.blit(realLineHistorySeparation, (35, ySize-realHistoryHeigh))


    if realHistoryHeigh > ySize:
        pageUpText = pageUpDownFont.render("⇈", 1, pageUpDownColor)
        screen.blit(pageUpText, (historyAreaWidth + 8, 4))
        shadowTop = pygame.image.load("history-top-shadow.png").convert_alpha()
        shadowTop = pygame.transform.scale(shadowTop, (historyAreaWidth, 8))
        screen.blit(shadowTop, (0, 0))


winMatchDisposition = []

def showVariant(screen, wtw, posX):
    yellow_colour = (205, 153, 29)
    xSize, ySize = screen.get_size()
    variantFont = pygame.font.SysFont("monospace", 14, bold=True)
    wtwText = variantFont.render(wtw, 1, (225, 225, 225))

    # Size deffinition
    variantBackgroundInformation = surfaceInformations()
    variantBackgroundInformation.left = 2
    variantBackgroundInformation.right = 2
    variantBackgroundInformation.height = textZoneHeigh
    variantBackgroundInformation.y = ySize - textZoneHeigh

    variantTextInformation       = surfaceInformations()
    variantTextInformation.width, variantTextInformation.height = variantFont.size(wtw)


    variantBackgroundInformation.width = variantTextInformation.width
    variantBackgroundInformation.width = variantBackgroundInformation.width + variantBackgroundInformation.left  + variantBackgroundInformation.right
    variantBackgroundInformation.x = xSize - variantBackgroundInformation.width - posX

    variantTextInformation.x = variantBackgroundInformation.x + 1 + variantBackgroundInformation.left
    variantTextInformation.y = variantBackgroundInformation.y + 1

    #creation
    variantBackground = pygame.Surface(
        (variantBackgroundInformation.width, variantBackgroundInformation.height))
    variantBackground.fill(yellow_colour)

    #Blitting

    screen.blit(variantBackground, (variantBackgroundInformation.x, variantBackgroundInformation.y))
    screen.blit(wtwText, (variantTextInformation.x, variantTextInformation.y))


    #Ending
    return variantBackgroundInformation.width + variantBackgroundInformation.left + variantBackgroundInformation.right

def trivial(numberOfInitialMatch, wtw, screen):
    global programHaveToContinue
    global textUserInput
    global normalUserInput
    global exMode
    global normalMode
    global textToAnalyse
    global normalTextToAnalyse
    global finalNormalUserInput

    allowedEntry = ["1", "2", "3"]

    beginingOfGame = int(time.time())

    currentNumberOfMatch = numberOfInitialMatch

    normalTextInformation = surfaceInformations()
    indicatorTextInformation = surfaceInformations()

    listOfTry = []
    functionHaveToContinue = True

    myfont = pygame.font.SysFont("monospace", 14)
    errorToDisplay = False
    weHaveAWiner = False
    winer = None

    winMatchDisposition = []
    while functionHaveToContinue and programHaveToContinue and (weHaveAWiner == False):
        userPlayed = 0
        computerPlayed = 0
        functionHaveToContinue, textToanalyse = analyseTyping(
            "trivial", numberOfInitialMatch, wtw)

        # Redifining variables
        xSize, ySize = screen.get_size()
        gameAreaDim[0] = xSize - historyAreaWidth

        # indicator area variables
        indicatorPosition = ((historyAreaWidth + ((xSize - historyAreaWidth) -
                                                  indicatorDim[0]) / 2), ySize - textZoneHeigh - indicatorDim[1])
        indicatorArea = pygame.Surface((indicatorDim[0], indicatorDim[1]))

        # Appling variables
        screen.fill(background_colour)

        if weHaveAWiner == False:
            printListOfTry(screen, listOfTry)

            # Indicator area deffinition
            indicatorArea.fill(indicator_colour)
            screen.blit(indicatorArea, (indicatorPosition[
                        0], indicatorPosition[1]))

            indicatorBorderPositionLeft = (
                int(indicatorPosition[0] + circleRadius), int(indicatorPosition[1]))
            pygame.draw.circle(screen, indicator_colour, (indicatorBorderPositionLeft[
                               0], indicatorBorderPositionLeft[1]), circleRadius)

            indicatorBorderPositionRight = (int(
                indicatorPosition[0] + indicatorDim[0] - circleRadius), int(indicatorPosition[1]))
            pygame.draw.circle(screen, indicator_colour, (indicatorBorderPositionRight[
                               0], indicatorBorderPositionRight[1]), circleRadius)

            indicatorRadiusCompleterPosition = (
                indicatorPosition[0] + circleRadius, indicatorPosition[1] - circleRadius)
            indicatorRadiusCompleterDim = (
                indicatorDim[0] - 2 * circleRadius, circleRadius)
            indicatorRadiusCompleterArea = pygame.Surface(
                (indicatorRadiusCompleterDim[0], indicatorRadiusCompleterDim[1]))
            indicatorRadiusCompleterArea.fill(indicator_colour)
            screen.blit(indicatorRadiusCompleterArea, (indicatorRadiusCompleterPosition[
                        0], indicatorRadiusCompleterPosition[1]))

            # Matchs deffinition
            maxMatchAreaDim = [xSize - historyAreaWidth - (2 * matchAreaBorder.right), ySize - textZoneHeigh - indicatorDim[
                1] - matchAreaBorder.top - matchAreaBorder.bottom]

            maxMatchDim = [0, 0]
            maxMatchDim[0] = maxMatchAreaDim[0] / (numberOfInitialMatch * 1.5)
            maxMatchDim[1] = maxMatchDim[0] * matchPicRatio

            if maxMatchDim[1] > maxMatchAreaDim[1]:
                matchDim = [int(maxMatchAreaDim[1] / matchPicRatio),
                            int(maxMatchAreaDim[1])]
            else:
                matchDim = [int(maxMatchDim[0]), int(
                    maxMatchDim[0] * matchPicRatio)]

            tempImageMatch = pygame.image.load("match.png").convert_alpha()
            matchMaxWidth, matchMaxHeight = tempImageMatch.get_rect().size

            if matchDim[0] > matchMaxWidth:
                matchDim[0] = matchMaxWidth
                matchDim[1] = matchMaxHeight

            matchAreaDim = [matchDim[0] * numberOfInitialMatch, matchDim[1]]

            matchAreaPos = [historyAreaWidth + matchAreaBorder.left + (
                (maxMatchAreaDim[0] - matchAreaDim[0]) / 2), (ySize - indicatorDim[1] - matchDim[1]) / 2]
            secondMatchAreaPos = [matchAreaPos[
                0] + (matchAreaDim[0] - (numberOfInitialMatch * 1.5) * matchDim[0]) / 2, matchAreaPos[1]]

            i = 0
            matchS = []
            while i < numberOfInitialMatch:
                if i < currentNumberOfMatch:
                    if currentNumberOfMatch in [1, 2, 3]:
                        matchS.append(pygame.image.load(
                            "match-burned.png").convert_alpha())
                    else:
                        if i >= (currentNumberOfMatch - 3):
                            matchS.append(pygame.image.load(
                                "match-allowed.png").convert_alpha())
                        else:
                            matchS.append(pygame.image.load(
                                "match.png").convert_alpha())
                else:
                    matchS.append(pygame.image.load(
                        "match-void.png").convert_alpha())

                matchLeftVoid = 0
                if i != 0:
                    matchLeftVoid = matchDim[0] / 2
                currentMatchPos = [secondMatchAreaPos[
                    0] + i * (matchLeftVoid + matchDim[0]), secondMatchAreaPos[1]]
                matchS[i] = pygame.transform.scale(
                    matchS[i], (matchDim[0], matchDim[1]))
                screen.blit(
                    matchS[i], (currentMatchPos[0], currentMatchPos[1]))
                i = i + 1

            indicatorFont = pygame.font.SysFont("monospace", 34)
            indicatorTextContent = str(
                currentNumberOfMatch) + "/" + str(numberOfInitialMatch)
            indicatorText = indicatorFont.render(
                indicatorTextContent, 1, (255, 255, 255))
            indicatorTextInformation.width, indicatorTextInformation.height = indicatorFont.size(
                indicatorTextContent)
            indicatorTextInformation.x = indicatorPosition[
                0] + (indicatorDim[0] - indicatorTextInformation.width) / 2
            indicatorTextInformation.y = indicatorPosition[1] + 5
            screen.blit(indicatorText, (indicatorTextInformation.x,
                                        indicatorTextInformation.y))

            if finalNormalUserInput:
                getFromAnalysis = trivialAnalysis(
                    currentNumberOfMatch, numberOfInitialMatch, wtw, finalNormalUserInput)
                finalNormalUserInput = False
                if getFromAnalysis[0] == True:
                    userPlayed = getFromAnalysis[2]
                    listOfTry.append(userPlayed)
                    print(listOfTry)
                else:
                    errorToDisplay = getFromAnalysis[1]

                if getFromAnalysis[0] == True:
                    computerPlayed = playTrivial(
                        currentNumberOfMatch - userPlayed)
                    listOfTry.append(computerPlayed)
                    print(listOfTry)

            currentNumberOfMatch = currentNumberOfMatch - userPlayed
            if currentNumberOfMatch == 0:
                winer = True
            else:
                currentNumberOfMatch = currentNumberOfMatch - computerPlayed
                if currentNumberOfMatch == 0:
                    winer = False

            numberOfMatchDelled = numberOfInitialMatch - currentNumberOfMatch

            if currentNumberOfMatch == 0:
                print("machin")
                weHaveAWiner = True
                timeOfEndOfGame = int(time.time()) - beginingOfGame

        else:
            print("we have a winer")
            timeOfEndOfGame = int(time.time()) - beginingOfGame

        if textToanalyse in allowedEntry:
            normalTextZone = myfont.render(
                "".join(textToanalyse), 1, (255, 255, 255))
            screen.blit(normalTextZone, (100, 100))

        makeTextZone("Trivial")
        timeZoneWidth = makeTimetZone(beginingOfGame)
        wtwZoneWidth = showVariant(screen, wtw, timeZoneWidth)

        if textToanalyse["mode"] == "normal":
            errorToDisplay = False
            normalText = myfont.render(
                "".join(textToanalyse["content"]), 1, (255, 255, 255))

            normalTextInformation.width, normalTextInformation.height = normalText.get_size()
            normalTextInformation.x = xSize - normalTextInformation.width - 5 - wtwZoneWidth - timeZoneWidth
            normalTextInformation.y = ySize - textZoneHeigh
            screen.blit(normalText, (normalTextInformation.x,
                                     normalTextInformation.y))

        if errorToDisplay != False:
            normalText = myfont.render(errorToDisplay, 1, red)

            normalTextInformation.width, normalTextInformation.height = normalText.get_size()
            normalTextInformation.x = xSize - normalTextInformation.width - 5 - wtwZoneWidth - timeZoneWidth
            normalTextInformation.y = ySize - textZoneHeigh
            screen.blit(normalText, (normalTextInformation.x,
                                     normalTextInformation.y))


#       testSurface = pygame.Surface((indicatorTextInformation.width, indicatorTextInformation.height))
#       testSurface.fill(red)
#       screen.blit(testSurface, (indicatorTextInformation.x,indicatorTextInformation.y))

        #####################
        pygame.display.flip()
        #####################

    while functionHaveToContinue and programHaveToContinue:
        winingFallingScreen(
            winer, wtw, numberOfInitialMatch, timeOfEndOfGame)
        functionHaveToContinue, textToanalyse = analyseTyping(
            "trivial", numberOfInitialMatch, wtw)
        makeTextZone("Trivial")

        #####################
        pygame.display.flip()
        #####################

    return False

programHaveToContinue = True
variant = None
generalState = whatToDo()


def main(variant="trivial", number=numberOfInitialMatch, wtw="ttl"):
    global generalState
    global programHaveToContinue
    while programHaveToContinue:
        if variant not in [0, None, ""]:
            variant = generalState.variant
        if number not in [0, None, ""]:
            number = generalState.number
        if wtw not in [0, None, ""]:
            wtw = generalState.wtw

        if variant == "trivial":
            trivial(number, wtw, screen)

main("trivial", numberOfInitialMatch, "ttl")
