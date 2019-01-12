#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys
import time
import re
import copy
from optparse import OptionParser


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

humanPlayerArrow="←"
computerPlayerArrow="→"
quitCommands=["x", "X", "quit", "q", "Q"]
newGameCommands=["new", "n"]
helpCommands=["help", "h", "?"]
aboutCommands=["about"]
backCommands=["u", "undo"]
historyCommands=["hist", "history"]

allowdedCommands=quitCommands + newGameCommands + helpCommands + aboutCommands + backCommands + historyCommands

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
        self.isUndo = self.isUndoMet()
        self.player = True

    def isUndoMet(self):
        return not self.isDo

    def toggle(self):
        self.isDo = not self.isDo

    def play(self, number):
        try:
            number=int(number)
            if number in self.allowedRange:
                self.played = number
        except:
            print("The played number should be a number between 1, 2, or 3")


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
        self.history.append(newMove)
        self.burrenedMatchs = self.burrenedMet()

    def printHist(self):
        finalChar = ""
        for move in self.history:
            finalChar += str(move.position)
            finalChar += ": "
            finalChar += str(move.played)
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

    def descriptorMaker(self):
        descriptor=makeDescriptor(self.firstPlayer, self.name, self.seed, self.wtw.shortname)
        return descriptor
    def togglePlayer(self):
        self.firstPlayer = not self.firstPlayer
    def abborting(self):
        self.isStillPlay = False
    def remainingMet(self):
        remainingMatchs = self.seed - self.history.burrenedMatchs
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

    def showGraphicalView(self):
        iterateGeneralMatchs=1
        while (iterateGeneralMatchs <= self.remainingMatchs):
            separator=self.isTheCurrentGraphicalMatchInAGroup(iterateGeneralMatchs)
            print("|", end=separator)
            iterateGeneralMatchs+=1
        while (iterateGeneralMatchs <= self.seed):
            separator=self.isTheCurrentGraphicalMatchInAGroup(iterateGeneralMatchs)
            print(":", end=separator)
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


def trivialMakePrompt():
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

def isInputCommandValid(humanInput):
    if re.match("^:.*$", humanInput) is not None:
        return True
    return False

def trivialAnalyseHumanInputCommand(humanInput):
    try:
        humanInput=int(humanInput)
    except:
        print("“" + humanInput + "”" + " is not a valid move. See :help for furder informations.")


def trivialAnalyseHumanInput(humanInput):
    if isInputCommandValid(humanInput):
        print("This command is true.")
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

def finalGameMessage():
    if thegame.winer == True:
        print("Congratulations, you win!")
    elif thegame.winer == False:
        print("Ow… it seems the computer win, but try again!")

def trivialMain():
    while thegame.isStillPlay and (thegame.winer == None):

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


stillPlaying=True
def quitGame():
    global stillPlaying
    stillPlaying = False
    print("Lefting %prog")

def shouldWeQuit():
    thePlayerChoose=query_yes_no("Would-you like to replay?")
    if not thePlayerChoose:
        quitGame()

def mainFunc():
    global stillPlaying
    global thegame

    while stillPlaying:
        thegame = TrivialGame()
        trivialMain()
        if stillPlaying:
            shouldWeQuit()

mainFunc()
