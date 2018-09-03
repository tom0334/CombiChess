#!/usr/bin/env python

import chess
import chess.uci
import sys

# This class contains the inner workings of combiChess. If you want to change its settings or start it then
# Please go to launcher.py This file also lets you change what engines CombiChess uses.


class CombiChess:
    # after a stop command, ignore
    canceled = False

    engines = [None, None, None]
    moves = [None, None, None]

    # current board status, probably received from UCI position commands
    board = chess.Board()

    # Statistics for what engines are listened to.
    listenedTo = [0, 0, 0]

    # Initialized in the init function
    engineFolder = None
    engineFileNames = None

    def __init__(self, engineLocation, engineNames):
        self.exit = False
        self.engineFolder = engineLocation
        self.engineFileNames = engineNames
        printAndFlush("CombiChess 1.0 by T. Friederich")

    # This starts CombiChess.
    def start(self):
        # first start the engines
        for i in xrange(0, len(self.engines)):
            try:
                self.engines[i] = chess.uci.popen_engine("./" + self.engineFolder + self.engineFileNames[i])
            except:
                sys.stderr.write("CombiChess Error: could not load the engine at file path:" + self.engineFileNames[i])
                sys.stderr.write(
                    "\n\nDid you change the script to include the engines you want to use with Combichess?")
                sys.stderr.write("To do this, open Combichess.py and change the engineFilePaths.\n")
                sys.exit()

            # tell the engines to init and start a new game
            self.engines[i].uci()
            self.engines[i].ucinewgame()
        # starts the main program
        self.__mainloop()

    # Main program loop. It keep waiting for input after a command is finished
    def __mainloop(self):
        while not self.exit:
            userCommand = raw_input()

            if userCommand == "uci":
                printAndFlush("id name TomsCombiChess")
                printAndFlush("id author Tom Friederich")
                printAndFlush("uciok")

            if userCommand.startswith("option name"):
                printAndFlush("uciok")

            if userCommand == "isready":
                printAndFlush("readyok")

            if userCommand.startswith("go"):
                self.startEngines()

            elif userCommand.startswith("position"):
                self.handlePosition(userCommand)

            elif userCommand == "exit":
                self.exit = True
            elif userCommand == "stop":
                sleep(300)
                # TODO  fix this
                printAndFlush(self.moves[0])
                printAndFlush("readyok")
                printAndFlush("uciok")
            else:
                printAndFlush("unknown command")

    # on engine done callbacks. The number is the index in the engines array
    def onEngine0Finished(self, command):
        self.onFinished(command, 0)

    def onEngine1Finished(self, command):
        self.onFinished(command, 1)

    def onEngine2Finished(self, command):
        self.onFinished(command, 2)

    def startEngine(self, index, callback):
        self.engines[index].position(self.board)
        command = self.engines[index].go(movetime=990, async_callback=callback)

    # mprint("info string started engine " + str(index))

    def startEngines(self):

        self.moves = [None, None, None]
        self.canceled = False

        self.startEngine(0, self.onEngine0Finished)
        self.startEngine(1, self.onEngine1Finished)
        self.startEngine(2, self.onEngine2Finished)

    # this function is called after a engine is done. This means it is called multiple times!
    def onFinished(self, command, index):
        # if this callback is called after the UCI stop command,
        # we can just ignore it.
        if self.canceled:
            return

        engineMove, ponder = command.result()

        # log the result
        EngineName = self.engineFileNames[index]
        printAndFlush("info string " + EngineName + " says:\t" + str(engineMove))

        # set the move in the found moves
        self.moves[index] = engineMove

        # if engine 1 and 2 are done, and they agree on a move, do that move
        if self.moves[1] is not None and self.moves[1] == self.moves[2]:
            printAndFlush("info string listening to children")
            self.listenedTo[0] += 1
            bestMove = self.moves[1]

        # if engine 0 and another agree, do that move
        elif self.moves[0] is not None and (self.moves[0] == self.moves[1] or self.moves[0] == self.moves[2]):
            printAndFlush("info string listening to master and another")
            self.listenedTo[1] += 1
            bestMove = self.moves[0]

        # all engines are done and they dont agree. Listen to master
        elif None not in self.moves:
            printAndFlush("info string listening to master")
            self.listenedTo[2] += 1
            bestMove = self.moves[0]
        # we dont know our best move yet
        else:
            return

        self.printStats()

        self.canceled = True
        # stop remaining engines
        for engine in self.engines:
            engine.stop()

        printAndFlush("bestmove " + str(bestMove))

    # prints stats on how often was listened to master and how often to children
    def printStats(self):
        printAndFlush("info string listenStats [C, M+C, M] " + str(self.listenedTo))
        totalSum = self.listenedTo[0] + self.listenedTo[1] + self.listenedTo[2]
        masterSum = self.listenedTo[1] + self.listenedTo[2]
        masterPercent = (float(masterSum) / float(totalSum)) * 100.0
        printAndFlush("info string Master % " + str(masterPercent))

    # handle UCI position command
    def handlePosition(self, positionInput):
        words = positionInput.split()
        # if this is not true, it is not a position command
        assert words[0] == "position"
        try:
            # handle building up the board from a FEN string
            if words[1] == "fen":
                fen = positionInput.split(' ', 2)[2]
                printAndFlush("")
                self.board.set_fen(fen)
            # handle board from startpos command, building up the board with moves
            elif words[1] == "startpos":
                self.board.reset()
                for move in words[3:]:  # skip the first two words : 'position' and 'startpos'
                    printAndFlush("Adding " + move + " to stack")
                    self.board.push_uci(move)
            else:
                printAndFlush("unknown position type")
        except Exception as e:
            printAndFlush("something went wrong with the position. Please try again")
            printAndFlush(e)

        # show the board
        printAndFlush(self.board)


# UTILS
# This function flushes stdout after writing so the UCI GUI sees it
def printAndFlush(text):
    arg = str(text)
    sys.stdout.write(arg + "\n")
    sys.stdout.flush()
