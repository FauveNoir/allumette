#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys
import time
import re
import copy
from tabulate import tabulate
from optparse import OptionParser
from trivial import *


version = "0.1"
helptabulation="       "


usage = "usage: %prog [ [ -n | --number-of-match ] <number of match> ]  [ [ -v | --variente ] <variente> ]  [ [ -w | --what-to-wine ] <wtw> ]\n" + helptabulation + "%prog [ -d | --descriptor ] <descriptor>\n" + helptabulation + "%prog [ -v | --version | --help]"
parser = OptionParser(usage=usage, version="%prog 0.1")

parser.add_option("-n", "--number-of-match", help="number of match",
                  default=15, action="store", dest="numberOfMatch")
parser.add_option("-v", "--varient",         help="the variant of Nim",
                  default="trivial", action="store", dest="varient")
parser.add_option("-w", "--what-to-wine",    help="mode, there is two values possibles “ttl” and “ltl”",
                  default="ttl", action="store", dest="wtw")
parser.add_option("-c", "--compture",        help="Set the computer as first player",
                  default="ttl", action="store", dest="wtw")

(options, args) = parser.parse_args()

newGameCommands=["new", "n"]
descriptorSyntax="^((?P<firstPlayer>(\+|-)) +)?(?P<variente>([a-zA-Z]*|-));(?P<seednumber>([0-9]+|-));(?P<wtw>ttl|ltl|-)$"

class anygame():
    def __init__(self):
        self.varient = "Trivial"
        self.wtw = ttl
        self.seedNumber = 8
        self.firstPlayer = True

listOfVarients=[]

class Varient():
    def __init__(self, name, seedNumber, description):
        self.name = name
        self.seedNumber = seedNumber
        self.description = description
        self.addToListOfVarients()

    def addToListOfVarients(self):
        global listOfVarients
        listOfVarients.append(self)

trivial = Varient("Trivial", 15, "Theire is one heap of match and eatch gamer have to take 1, 2, or 3 match per move.")
marienbad = Varient("Marienbad", 5, "Theire is different heap and each gamer should take one or more match from one heap pear move.")

def makeTableOfAvailableVarients():
    global listOfVarients
    table = []
    for varient in listOfVarients:
        line = []
        line.append(varient.name)
        line.append(varient.description)
        table.append(line)

    return table

def printListOfAvailableVarients():
    table = makeTableOfAvailableVarients()
    print(tabulate(table, tablefmt="plain"))


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


allKeyboardActions = []


class keyboardAction:
    def __init__(self):
        self.name=""
        self.longCom = None
        self.shortCom = None
        self.syntax = None
        self.syntaxHelp = None
        self.help = None
        self.addToListOfActions()

    def addToListOfActions(self):
        global allKeyboardActions
        allKeyboardActions.append(self)

    def isMatch(self, action):
        if re.match(self.syntax, action) is not None:
            return True
        else:
            return False

    def number(self, command):
        number = re.match(self.syntax, command)
        number = number.group("number")
        if number == None:
            return 1
        else:
            return number

    def oxilary(self, command):
        oxilary = re.match(self.syntax, command)
        oxilary = oxilary.group("oxilary")
        if oxilary == None:
            return None
        else:
            return oxilary

    def execute(self):
        print("Noting to do for this command")

    def associatedFunc(self, argument):
        print("Noting to do")

def syntaxOfAllAllowdedActions():
    syntax = "("
    global allKeyboardActions
    iterate=0
    while iterate < len(allKeyboardActions):
        action = allKeyboardActions[iterate]
        syntax += "(" + action.longCom + ")"
        syntax += "|"
        syntax += "(" + action.shortCom + ")"
        if iterate < len(allKeyboardActions)-1:
            syntax += "|"
        iterate += 1
    syntax += ")"

    return syntax

def quitGame():
    global stillPlaying
    stillPlaying = False
    print("Lefting %prog")

def printAllCommandsHelp():
    print("Help")
    table=[]
    for command in allKeyboardActions:
        line=[command.syntaxHelp,command.help]
        table.append(line)
    print(tabulate(table, tablefmt="plain"))

def findCommandAfterMatch(match):
    global allKeyboardActions
    for  action in allKeyboardActions:
        if action.isMatch(match):
            return action
    return None

def printACommandHelp(command):
    command=findCommandAfterMatch(command)
    print(command.syntaxHelp + "  " + command.help)

def isACommandExist(command):
    itExist = False
    for action in allKeyboardActions:
        if command in [action.shortCom, action.longCom]:
            itExist = True
    return itExist

def helpMessage(command):
    if command == None:
        printAllCommandsHelp()
    elif isACommandExist(command):
        printACommandHelp(command)
    else:
        print("The command “" + str(command) + "” not exist.")

undo = keyboardAction()
undo.name = "Undo"
undo.longCom = "undo"
undo.shortCom = "u"
undo.syntax = "^u(ndo)?( +(?P<number>[0-9]+))? *$"
undo.syntaxHelp = "u(ndo) <n>"
undo.help = "Undo the <n> previous moves"

redo = keyboardAction()
redo.name = "Redo"
redo.longCom = "redo"
redo.shortCom = "r"
redo.syntax = "^r(edo)?( +(?P<number>[0-9]+))? *$"
redo.syntaxHelp = "r(edo) <n>"
redo.help = "Redo the <n> undid previous moves"

about = keyboardAction()
about.name = "About"
about.longCom = "about"
about.shortCom = "r"
about.syntax = "^about$"
about.syntaxHelp = "about"
about.help = "Print about informations."

histCom = keyboardAction()
histCom.name = "History"
histCom.longCom = "history"
histCom.shortCom = "hist"
histCom.syntax = "^hist(ory)?$"
histCom.syntaxHelp = "hist(ory)"
histCom.help = "Print whole history sequence."

helpCom = keyboardAction()
helpCom.name = "Help"
helpCom.longCom = "help"
helpCom.shortCom = "h"
helpCom.syntax = "^h(elp)?( +(?P<oxilary>" + syntaxOfAllAllowdedActions() + "))? *$"
helpCom.syntaxHelp = "h(elp)"
helpCom.help = "Bring help about commands."
helpCom.execute = helpMessage

quit = keyboardAction()
quit.name = "Quit"
quit.longCom = "quit"
quit.shortCom = "q"
quit.syntax = "^(q|Q)(uit)?|x|X$"
quit.syntaxHelp = "Q(quit), q(uit), x, X"
quit.help = "Leave the game."

varientCom = keyboardAction()
varientCom.name = "List of varients"
varientCom.longCom = "varients"
varientCom.shortCom = "var"
varientCom.syntax = "^var(ients)?$"
varientCom.syntaxHelp = "var(ients)"
varientCom.help = "Get list of all varients."

instructions = keyboardAction()
instructions.name = "Instructions"
instructions.longCom = "instructions"
instructions.shortCom = "i"
instructions.syntax = "^i(nstr(uction(s)?)?)?$"
instructions.syntaxHelp = "i(nstr(uction(s)))"
instructions.help = "Explain the goal of the game."

def aboutMessage():
    print("This is Open Allumette version 0.1\nCC-by-sa 2019 Fauve\nhttps://fauvenoir.github.io/allumette/")

definedStyle="ascii"

class matchTipe:
    def __init__(self):
        self.latnStyle = ""
        self.asciiStyle = ""
        self.yotaStyle = ""
        self.chessStyle = ""

    def current():
        global definedStyle
        if  definedStyle == "latn":
            return self.latnStyle
        if  definedStyle == "ascii":
            return self.asciiStyle
        if  definedStyle == "yota":
            return self.yotaStyle
        if  definedStyle == "chess":
            return self.chessStyle

# R | I ♖ : allumette restante
# B _ i ♗ : allumette prise
# H # İ ♕ : allumette incandescente
# W @ Î ♔ : l’allumette à prendre
# F ! Ɨ ♗ : l’allumette mortelle
matchBurened=matchTipe()
matchBurened.latnStyle = "B"
matchBurened.asciiStyle = "_"
matchBurened.yotaStyle = "i"
matchBurened.chessStyle = "♗"

matchRemain=matchTipe()
matchRemain.latnStyle = "R"
matchRemain.asciiStyle = "|"
matchRemain.yotaStyle = "I"
matchRemain.chessStyle = "♖"

matchHot=matchTipe()
matchHot.latnStyle = "H"
matchHot.asciiStyle = "#"
matchHot.yotaStyle = "İ"
matchHot.chessStyle = "♕"

matchKing=matchTipe()
matchKing.latnStyle = "W"
matchKing.asciiStyle = "@"
matchKing.yotaStyle = "Î"
matchKing.chessStyle = "♔"

matchMortal=matchTipe()
matchMortal.latnStyle = "F"
matchMortal.asciiStyle = "!"
matchMortal.yotaStyle = "Ɨ"
matchMortal.chessStyle = "♗"


### --- Begin trivial block ---
class TrivialMove:
    """ Classe déffinissant un mouvement dans la variente Triviale caractérisé par:
    - Sa valeure jouée (devant se trouver dans [1,2,3])
    - Le moment auquel elle a été joué en temps unix
    - Sa position au sein de l’historique des mouvements
    - Le fait que se mouvement ai été annulé et soit toujours dans la mémoire tampon ou non
    - Le joueur (entre humain et ordinateur l’ayant joué)
    """
    def __init__(self):
        self.allowedRange=[1,2,3]
        self.played = 3
        self.time = time.time()
        self.position = 0
        self.isDo = True
        self.isUndo = not self.isDo
        self.player = True

    def isUndoMet(self):
        return not self.isDo

    def toggle(self):
        self.isDo   = not self.isDo
        self.isUndo = not self.isUndo

    def play(self, number):
        try:
            number=int(number)
            if number in self.allowedRange:
                self.played = number
        except:
            print("The played number should be a number between 1, 2, or 3")

class TrivialHistory:
    def __init__(self):
        self.history = []
        self.burrenedMatchs = 0

    def burrenedMet(self):
        remainingMatchs = 0
        for move in self.history:
            if move.isDo:
                remainingMatchs += move.played
        return remainingMatchs

    def sanitize(self):
        newHistory = []
        try:
           for move in self.history:
               if move.isDo:
                   newHistory.append(move)
        except:
            print("")
        return newHistory

    def appendMove(self, number, whom):
        newHistory = self.sanitize()
        newMove = TrivialMove()
        newMove.position = len(newHistory)
        newMove.played = int(number)
        newMove.player = whom
        newHistory.append(newMove)
        self.history = newHistory
        self.burrenedMatchs = self.burrenedMet()

    def printHist(self):
        finalChar = ""
        for move in self.history:
            doIndicator=""
            if move.isUndo:
                doIndicator="-"
            finalChar += str(move.position)
            finalChar += ": "
            finalChar += str(move.played)
            finalChar += doIndicator
            finalChar += ",  "
        print(finalChar)

class TrivialGame:
    def __init__(self):
        self.defaultAllowdedMoves = [1, 2, 3]
        self.name = "Trivial"
        self.wtw = ttl
        self.wtw.setVarient(self.name)
        self.firstPlayer = True
        self.whoIsPlayingNow = self.firstPlayer
        self.seed = 15
        self.descriptor = self.descriptorMaker()
        self.beginingTime = time.time()
        self.isStillPlay = True
        self.history = TrivialHistory()
        self.remainingMatchs = self.seed
        self.burrenedMatchs = 0
        self.remainingMoves = self.defaultAllowdedMoves
        self.whoHaveToPlay = self.firstPlayer
        self.winer = None
        self.passTime = 0

    def descriptorMaker(self):
        descriptor=makeDescriptor(self.firstPlayer, self.name, self.seed, self.wtw.shortname)
        return descriptor

    def togglePlayer(self):
        self.firstPlayer = not self.firstPlayer

    def abborting(self):
        self.isStillPlay = False

    def remainingMet(self):
        remainingMatchs = self.seed - self.history.burrenedMet()
        return remainingMatchs

    def stillAllowededMet(self):
        allowdedMoves = []
        for number in self.defaultAllowdedMoves:
            if number <= self.remainingMatchs:
                allowdedMoves.append(number)
        return allowdedMoves

    def isAMoveAlloweded(self, number):
        if number in self.remainingMoves:
            return True
        else:
            return False

    def playMove(self, number, whom):
        if self.isAMoveAlloweded( number):
            self.history.appendMove(number, whom)
            self.burrenedMatchs = self.history.burrenedMatchs
            self.remainingMatchs = self.remainingMet()
            self.remainingMoves = self.stillAllowededMet()
            self.whoHaveToPlay = not whom
            self.winerMet()
            return True
        else:
            return False

    def isTheCurrentGraphicalMatchInAGroup(self, position):
        if ( position%4 == self.wtw.modulator ):
            return " "
        else:
            return ""

    def isItHotSituation(self):
        if ( self.remainingMatchs < 4 + self.wtw.modulator ):
            return True
        else:
            return False

    def graphicalFirstMatch(self):
        if self.wtw == ttl:
            return "♔"
        elif  self.wtw == ltl:
            #return "☠"
            return "♗"

    def showGraphicalView(self):
        iterateGeneralMatchs=1
        if self.isItHotSituation():
            remainingMatchsRendering = "♕"
        else:
            remainingMatchsRendering = "♖"
        while (iterateGeneralMatchs <= self.remainingMatchs):
            separator=self.isTheCurrentGraphicalMatchInAGroup(iterateGeneralMatchs)
            if iterateGeneralMatchs==1:
                print(self.graphicalFirstMatch(), end=separator)
            else:
                print(remainingMatchsRendering, end=separator)
            iterateGeneralMatchs+=1
        while (iterateGeneralMatchs <= self.seed):
            separator=self.isTheCurrentGraphicalMatchInAGroup(iterateGeneralMatchs)
            print("♗", end=separator)
            iterateGeneralMatchs+=1
        print("")

    def lastPlayer(self):
        lastPlayer = self.history.history[-1].player
        return lastPlayer

    def winerMet(self):
        if self.remainingMatchs == 0:
            winerIs = self.lastPlayer()
            self.winer = winerIs
            return winerIs
        else:
            return None

    def end(self):
        endTime = time.time()
        passTime = self.bginingTime
        endTime = endTime-passTime
        self.passTime = endTime

    def undo(self, numberOfMoves):
        numberOfMoves=int(numberOfMoves)
        numberOfUndids = 0
        iterate = 1
        while (iterate <= len(self.history.history)) and (numberOfUndids < numberOfMoves ):
            move = self.history.history[-iterate]
            if move.isDo and move.player:
                self.history.history[-iterate].toggle()
                if self.history.history[-iterate+1].isDo:
                    self.history.history[-iterate+1].toggle()
                numberOfUndids += 1
            iterate += 1
        self.remainingMatchs = self.remainingMet()

    def redo(self, numberOfMoves):
        numberOfMoves=int(numberOfMoves)
        numberOfRedids = 0
        iterate = 0
        while (iterate < len(self.history.history)) and (numberOfRedids < numberOfMoves):
            move = self.history.history[-iterate]
            if move.isUndo and move.player:
                self.history.history[iterate].toggle()
                if self.history.history[iterate+1]:
                    self.history.history[iterate+1].toggle()
                numberOfRedids +=1
            iterate += 1
        self.remainingMatchs = self.remainingMet()



def trivialMakePrompt():
    thegame.history.printHist()
    print("")
    thegame.showGraphicalView()
    prompt = "["
    prompt += thegame.name
    prompt += " - "
    prompt += str(thegame.wtw.shortname)
    prompt += " | "
    prompt += str(thegame.remainingMatchs)
    prompt += "/"
    prompt += str(thegame.seed)
    prompt += "]> "
    return prompt


def trivialAnalyseHumanInputCommand(humanInput):
    try:
        humanInput=int(humanInput)
    except:
        print("“" + humanInput + "”" + " is not a valid move. See :help for furder informations.")


def trivialAnalyseHumanInput(humanInput):
    if humanInput == "":
        print("Noting to do.")
    elif isInputCommandValid(humanInput):
        playerCommand(humanInput)
    elif re.match("^[0-9]*$", humanInput):
        if int(humanInput) in thegame.remainingMoves:
            thegame.playMove(int(humanInput), True)
            print("")
        else:
            print("“" + humanInput + "” is not a valid move.")
    else:
        print("“" + humanInput + "”" + " is not a valid move or command. See :help for furder informations.")

def trivialComputerPlay():
    modulator=thegame.wtw.modulator

    if thegame.remainingMatchs != 0:
        if ((thegame.remainingMatchs - 1) % 4) == modulator:
            answer = 1
        elif ((thegame.remainingMatchs - 2) % 4) == modulator:
            answer = 2
        elif ((thegame.remainingMatchs - 3) % 4) == modulator:
            answer = 3
        else:
            answer = random.randint(1, 3)
    else:
        answer = 0

    return answer

def trivialMain():
    while thegame.isStillPlay and (thegame.winer == None) and stillPlaying:

        if thegame.whoHaveToPlay:
            prompt=trivialMakePrompt()
            choice=input(prompt)
            trivialAnalyseHumanInput(choice)
        else:
            prompt=trivialMakePrompt()
            print("")
            print(prompt, end=" ")
            computerAnswer=trivialComputerPlay()
            print(computerAnswer)
            thegame.playMove(computerAnswer, False)

    if thegame.winer != None:
        finalGameMessage()

### --- End trivial block ---


class wtw:
    """ Condition de victoire définie par:
    - un nom court
    - un nom long
    - une description
    """
    def __init__(self):
        self.shortname=""
        self.fullname=""
        self.desc=""
        self.modulator=0

    def setVarient(self, varientName):
        if (varientName == "Trivial"):
            if self.shortname == "ttl":
                modulator = 0
            elif self.shortname == "ltl":
                modulator = 1
            self.modulator = modulator


ttl = wtw()
ttl.shortname="ttl"
ttl.fullname="Take the Last"
ttl.desc="The player should take the last remaining match to win"

ltl = wtw()
ltl.shortname="ltl"
ltl.fullname="Let the Last"
ltl.desc="The player should force his opponent to take the last remaning match to win"

def translateFirstPlayerSourceToDescriptor(firstPlayer):
    """ Fonction transcrivant les valeures boléennes du premier joueur en symbol de Descriptor, tel que :
    + pour le joueur humain
    - pour le joueur mécanique
    """
    try:
        if firstPlayer == True:
            return "+"
        elif firstPlayer == False:
            return "-"
        elif firstPlayer == None:
            return ""
    except:
        print("First player code should be “h” or “c”")


def makeDescriptor(firstPlayer, varientName, seedNumber, wtw):
    """ fonction rendant un Descriptor et prenant pour celà en entrée :
    - La valeure du premier joueur en boléen
    - Le nom de la variente à jouer
    - Le nombre graine
    - La condition de victoire
    """
    separator = ";"
    firstPlayerCode=translateFirstPlayerSourceToDescriptor(firstPlayer)
    formatedDescriptor=firstPlayerCode + separator + varientName + separator + str(seedNumber) + separator +  wtw
    return formatedDescriptor




def isInputCommandValid(humanInput):
    if re.match("^:.*$", humanInput) is not None:
        return True
    return False

def playerCommand(humanInput):
    pertinantSelection="(:)?(?P<pertinant>.*)"
    command = re.match(pertinantSelection, humanInput)
    command = command.group("pertinant")

    global undo
    if undo.isMatch(command):
        numberToUndo=undo.number(command)
        print("Undo " + str(numberToUndo) + " moves.")
        thegame.undo(numberToUndo)

    elif redo.isMatch(command):
        numberToRedo=redo.number(command)
        print("Redo " + str(numberToRedo) + " moves.")
        thegame.redo(numberToRedo)

    elif about.isMatch(command):
        aboutMessage()

    elif helpCom.isMatch(command):
        commandToKnow=helpCom.oxilary(command)
        helpCom.execute(None)

    elif varientCom.isMatch(command):
         printListOfAvailableVarients()

    elif quit.isMatch(command):
        quitGame()

    else:
        print("“" + humanInput + "”" + " is not a valid move or command. See :help for furder informations.")


def finalGameMessage():
    if thegame.winer == True:
        print("Congratulations, you win!")
    elif thegame.winer == False:
        print("Ow… it seems the computer win, but try again!")


stillPlaying=True

def shouldWeQuit():
    thePlayerChoose=query_yes_no("Would-you like to replay?")
    if not thePlayerChoose:
        quitGame()

def welcomMessage():
    print("This is Open Allumette version 0.1\nCC-by-sa 2019 Fauve\nhttps://fauvenoir.github.io/allumette/")

def isDescriptorValid(descriptor):
    global descriptorSyntax
    if re.match(descriptorSyntax, descriptor):
        return True
    else:
        return False

def newGameByDescriptor(descriptor):
    if isDescriptorValid(descriptor):
        match=re.match(descriptorSyntax, descriptor)
        newVarient=match.group("varient")
        newFirstPlayer=match.group("firstPlayer")
        newSeedNumber=match.group("seedNumber")
        newWtw=match.group("wtw")

def newGameByOptions(varient, seednumber, wtw, firstPlayer):
    pass

def mainFunc():
    global stillPlaying
    global thegame

    welcomMessage()
    while stillPlaying:
        thegame = TrivialGame()
        trivialMain()
        if stillPlaying:
            shouldWeQuit()

mainFunc()
