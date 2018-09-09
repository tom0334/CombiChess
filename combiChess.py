import os
import sys

import chess
import chess.uci

# This class contains the inner workings of combiChess. If you want to change its settings or start it then
# Please go to launcher.py This file also lets you change what engines CombiChess uses.


class CombiChess:
    # after a stop command, ignore the finish callback. See onFinished.
    _canceled = False

    # the pythonChess engine objects, loaded from the filePath and fileName
    _engines = [None, None, None]

    # The current move decided by the engine. None when it doesn't know yet
    _moves = [None, None, None]

    # current board status, probably received from UCI position commands
    board = chess.Board()

    # Statistics for how often is listened to each engine.
    listenedTo = [0, 0, 0]

    # Initialized in the init function. These are the folder path and a list of filenames in that folder
    engineFolder = None
    engineFileNames = None

    def __init__(self, engineLocation, engineNames):
        self.engineFolder = engineLocation
        self.engineFileNames = engineNames
        printAndFlush("CombiChess 1.0 by T. Friederich")

    # This starts CombiChess.
    def start(self):
        # first start the engines
        for i in range(0, len(self._engines)):
            try:
                self._engines[i] = chess.uci.popen_engine(os.path.join(self.engineFolder, self.engineFileNames[i]))
            except:
                sys.stderr.write("CombiChess Error: could not load the engine at file path:" + self.engineFileNames[i])
                sys.stderr.write(
                    "\n\nDid you change the script to include the engines you want to use with Combichess?")
                sys.stderr.write("To do this, open Combichess.py and change the engineFilePaths.\n")
                sys.exit()

            # tell the engines to init and start a new game
            self._engines[i].uci()
            self._engines[i].ucinewgame()
        # starts the main program
        self._mainloop()

    # Main program loop. It keep waiting for input after a command is finished
    def _mainloop(self):
        exit = False
        while not exit:
            userCommand = input()

            if userCommand == "uci":
                printAndFlush("id name TomsCombiChess")
                printAndFlush("id author Tom Friederich")
                printAndFlush("uciok")

            elif userCommand.startswith("setoption name"):
                # Skip button type options
                if " value " not in userCommand:
                    continue
                options = {}
                parts = userCommand.split(" ", 2)
                parts = parts[-1].split(" value ")
                options[parts[0]] = parts[1]
                for engine in self._engines:
                    engine.setoption(options)

            elif userCommand == "isready":
                printAndFlush("readyok")

            elif userCommand.startswith("go"):
                parts = userCommand.split(" ")
                go_commands = {}
                for command in ("movetime", "wtime", "btime", "winc", "binc", "depth", "nodes"):
                    if command in parts:
                        go_commands[command] = parts[parts.index(command) + 1]
                self._startEngines(go_commands)

            elif userCommand.startswith("position"):
                self.handlePosition(userCommand)

            elif userCommand == "quit":
                exit = True
            elif userCommand == "stop":
                for en in self._engines:
                    en.stop()
            else:
                printAndFlush("unknown command")

    # on engine done callbacks. The number is the index in the engines array
    def _onEngine0Finished(self, command):
        self._onFinished(command, 0)

    def _onEngine1Finished(self, command):
        self._onFinished(command, 1)

    def _onEngine2Finished(self, command):
        self._onFinished(command, 2)

    def _startEngine(self, index, callback, cmds):
        self._engines[index].position(self.board)
        command = self._engines[index].go(
            wtime=cmds.get("wtime"),
            btime=cmds.get("btime"),
            winc=cmds.get("winc"),
            binc=cmds.get("binc"),
            depth=cmds.get("depth"),
            nodes=cmds.get("nodes"),
            movetime=cmds.get("movetime"),
            async_callback=callback)

    # mprint("info string started engine " + str(index))

    def _startEngines(self, go_commands):
        self._moves = [None, None, None]
        self._canceled = False

        self._startEngine(0, self._onEngine0Finished, go_commands)
        self._startEngine(1, self._onEngine1Finished, go_commands)
        self._startEngine(2, self._onEngine2Finished, go_commands)

    # this function is called after a engine is done. This means it is called multiple times!
    def _onFinished(self, command, index):
        # if this callback is called after the UCI stop command,
        # we can just ignore it.
        if self._canceled:
            return

        engineMove, ponder = command.result()

        # log the result
        EngineName = self.engineFileNames[index]
        printAndFlush("info string " + EngineName + " says:\t" + str(engineMove))

        # set the move in the found moves
        self._moves[index] = engineMove

        # if engine 1 and 2 are done, and they agree on a move, do that move
        if self._moves[1] is not None and self._moves[1] == self._moves[2]:
            printAndFlush("info string listening to children")
            self.listenedTo[0] += 1
            bestMove = self._moves[1]

        # if engine 0 and another agree, do that move
        elif self._moves[0] is not None and (self._moves[0] == self._moves[1] or self._moves[0] == self._moves[2]):
            printAndFlush("info string listening to master and another")
            self.listenedTo[1] += 1
            bestMove = self._moves[0]

        # all engines are done and they dont agree. Listen to master
        elif None not in self._moves:
            printAndFlush("info string listening to master")
            self.listenedTo[2] += 1
            bestMove = self._moves[0]
        # we dont know our best move yet
        else:
            return

        self.printStats()

        self._canceled = True
        # stop remaining engines
        for engine in self._engines:
            engine.stop()

        printAndFlush("bestmove " + str(bestMove))

    # handle UCI position command
    def handlePosition(self, positionInput):
        words = positionInput.split()
        # if this is not true, it is not a position command
        assert words[0] == "position"
        try:
            # handle building up the board from a FEN string
            if words[1] == "fen":
                rest = positionInput.split(' ', 2)[2]
                if "moves" in rest:
                    rest = rest.split()
                    fen, moves = " ".join(rest[:6]), rest[7:]
                    self.board.set_fen(fen)
                    for move in moves:
                        self.board.push_uci(move)
                else:
                    self.board.set_fen(rest)
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
        # printAndFlush(self.board)

    # prints stats on how often was listened to master and how often to children
    def printStats(self):
        printAndFlush("info string listenStats [C, M+C, M] " + str(self.listenedTo))
        totalSum = self.listenedTo[0] + self.listenedTo[1] + self.listenedTo[2]
        masterSum = self.listenedTo[1] + self.listenedTo[2]
        masterPercent = (float(masterSum) / float(totalSum)) * 100.0
        printAndFlush("info string Master % " + str(masterPercent))


# UTILS
# This function flushes stdout after writing so the UCI GUI sees it
def printAndFlush(text):
    print(text, flush=True)
