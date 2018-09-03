#!/usr/bin/env python

import chess
import chess.uci
import sys

# file names for the engines
engineFolder = "/engines/"
engineFileNames = ["stockfish5", "komodo8", "andscacs"]


class CombiChess:
    # after a stop command, ignore
    canceled = False

    engines = [None, None, None]
    moves = [None, None, None]

    # current board status, probably received from UCI position commands
    board = chess.Board()

    # Statistics for what engines are listened to.
    listenedTo = [0, 0, 0]

    engineFolder = None
    engineFileNames = None

    def __init__(self, engineLocation, engineNames):
        self.exit = False
        self.engineFolder = engineLocation
        self.engineFileNames = engineNames
        mprint("CombiChess 1.0 by T. Friederich")

    def start(self):
        for i in xrange(0, len(self.engines)):
            try:
                self.engines[i] = chess.uci.popen_engine("./" + engineFolder + engineFileNames[i])
            except:
                sys.stderr.write("CombiChess Error: could not load the engine at file path:" + engineFileNames[i])
                sys.stderr.write(
                    "\n\nDid you change the script to include the engines you want to use with Combichess?")
                sys.stderr.write("To do this, open Combichess.py and change the engineFilePaths.\n")
                sys.exit()

            self.engines[i].uci()
            self.engines[i].ucinewgame()
        self.__mainloop()

    def __mainloop(self):
        while not self.exit:
            userCommand = raw_input()

            if userCommand == "uci":
                mprint("id name TomsCombiChess")
                mprint("id author Tom Friederich")
                mprint("uciok")

            if userCommand.startswith("option name"):
                mprint("uciok")

            if userCommand == "isready":
                mprint("readyok")

            if userCommand.startswith("go"):
                self.startEngines()

            elif userCommand.startswith("position"):
                self.handlePosition(userCommand)

            elif userCommand == "exit":
                self.exit = True
            elif userCommand == "stop":
                sleep(300)
                # TODO  fix this
                mprint(self.moves[0])
                mprint("readyok")
                mprint("uciok")
            else:
                mprint("unknown command")

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

    def onFinished(self, command, index):

        # if this callback is called after the UCI stop command,
        # we can just ignore it.
        if self.canceled:
            return

        engineMove, ponder = command.result()

        # log the result
        EngineName = engineFileNames[index]
        mprint("info string " + EngineName + " says:\t" + str(engineMove))

        # set the move in the found moves
        self.moves[index] = engineMove

        # if engine 1 and 2 are done, and they agree on a move, do that move
        if self.moves[1] is not None and self.moves[1] == self.moves[2]:
            mprint("info string listening to children")
            self.listenedTo[0] += 1
            bestMove = self.moves[1]

        # if engine 0 and another agree, do that move
        elif self.moves[0] is not None and (self.moves[0] == self.moves[1] or self.moves[0] == self.moves[2]):
            mprint("info string listening to master and another")
            self.listenedTo[1] += 1
            bestMove = self.moves[0]

        # all engines are done and they dont agree. Listen to master
        elif None not in self.moves:
            mprint("info string listening to master")
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

        mprint("bestmove " + str(bestMove))

    # prints stats on how often was listened to master and how often to children
    def printStats(self):
        mprint("info string listenStats [C, M+C, M] " + str(self.listenedTo))
        totalSum = self.listenedTo[0] + self.listenedTo[1] + self.listenedTo[2]
        masterSum = self.listenedTo[1] + self.listenedTo[2]
        masterPercent = (float(masterSum) / float(totalSum)) * 100.0
        mprint("info string Master % " + str(masterPercent))

    # handle UCI position command
    def handlePosition(self, positionInput):
        try:
            words = positionInput.split()
            # word 0 is position
            if words[1] == "fen":
                fen = positionInput.split(' ', 2)[2]
                mprint("")
                # mprint(fen)
                self.board.set_fen(fen)
            elif words[1] == "startpos":
                self.board.reset()
                for move in words[3:]:  # skip the first two
                    mprint("Adding " + move + " to stack")
                    self.board.push_uci(move)
            else:
                mprint("unknown position type")
        except Exception as e:
            mprint("something went wrong. Pls try again")
            mprint(e)

        mprint(self.board)


# UTILS
def mprint(text):
    arg = str(text)
    sys.stdout.write(arg + "\n")
    sys.stdout.flush()


# MAIN SCRIPT
combiChess = CombiChess(engineFolder, engineFileNames)
combiChess.start()
