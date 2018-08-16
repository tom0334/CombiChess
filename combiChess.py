#!/usr/bin/env python

import chess
import chess.uci
import sys

#file names for the engines
enginePath= "/engines/"
engineFileNames = ["stockfish5", "komodo8" , "andscacs"]

#current board status, probably received from UCI position commands
board = chess.Board()

#after a stop command, ignore 
canceled= False

engines=[None, None, None]
moves= [None, None, None]

#Statistics for what engines are listened to.
listenedTo=[0,0,0]

#on engine done callbacks. The number is the index in the engines array	
def onEngine0Finished(command):
	onFinished(command, 0)

def onEngine1Finished(command):
	onFinished(command, 1)

def onEngine2Finished(command):
	onFinished(command, 2)


def loadEngines():
	for i in xrange(0, len(engines)):
		try:
			engines[i] = chess.uci.popen_engine("./" + enginePath + engineFileNames[i])
		except:
			sys.stderr.write("CombiChess Error: could not load the engine at file path:" + engineFileNames[i])
			sys.stderr.write("\n\nDid you change the script to include the engines you want to use with Combichess?")
			sys.stderr.write("To do this, open Combichess.py and change the engineFilePaths.\n")
			sys.exit()
			
		engines[i].uci()
		engines[i].ucinewgame()

def startEngine(index, callback):
	engines[index].position(board)
	command = engines[index].go(movetime=990, async_callback=callback)
	#mprint("info string started engine " + str(index))

def startEngines():
	global moves
	global canceled
	
	moves= [None, None, None]
	canceled = False

	startEngine(0,onEngine0Finished)
	startEngine(1,onEngine1Finished)
	startEngine(2,onEngine2Finished)

def onFinished(command, index):
	global canceled
	global moves
	global listenedTo


	#if this callback is called after the UCI stop command, 
	#we can just ignore it.
	if canceled:
		return

	engineMove, ponder = command.result()

	#log the result
	EngineName = engineFileNames[index]
	mprint("info string " + EngineName + " says:	       " + str(engineMove))

	#set the move in the found moves
	moves[index] = engineMove

	bestmove = None

	#if engine 1 and 2 are done, and they agree on a move, do that move
	if moves[1] != None and moves[1] == moves[2]:
		mprint("info string listening to children")
		listenedTo[0]+=1
		bestmove = moves[1]

	#if engine 0 and another agree, do that move
	elif moves[0] != None and (moves[0] == moves[1] or moves[0] == moves[2]):
		mprint("info string listening to master and another")
		listenedTo[1]+=1
		bestmove = moves[0]

	#all engines are done and they dont agree. Listen to master
	elif None not in moves:
		mprint("info string listening to master")
		listenedTo[2]+=1
		bestmove = moves[0]
	#we dont know our best move yet
	else:
		return

	printStats()

	canceled = True
	#stop remaining engines
	for engine in engines:
		engine.stop()

	mprint("bestmove " + str(bestmove) )

#prints stats on how often was listened to master and how often to children
def printStats():
	mprint("info string listenStats [C, M+C, M] " + str(listenedTo))
	totalSum = listenedTo[0] + listenedTo[1] + listenedTo[2]
	masterSum = listenedTo[1] + listenedTo[2]
	masterPercent =(float(masterSum) / float(totalSum)) * 100.0 
	mprint("info string Master % " + str(masterPercent))

#handle UCI position command
def handlePosition(input):
	try:
		words = input.split()
		#word 0 is position
		if words[1] == "fen":
			fen = input.split(' ', 2)[2]
			mprint("")
			#mprint(fen)
			board.set_fen(fen)
		elif words[1] == "startpos":
			board.reset()
			for move in words[3:]: #skip the first two
				mprint("Adding " + move + " to stack")
				board.push_uci(move)
		else:
			mprint("unknown position type")
	except Exception as e:
		mprint("something went wrong. Pls try again")
		mprint(e)

	mprint(board)

def mprint(text):
	arg = str(text) 
	sys.stdout.write(arg +"\n")
	sys.stdout.flush()


#MAIN SCRIPT:

loadEngines()
exit = False


mprint("CombiChess 1.0 by T. Friederich ")
while( not exit):
	userCommand = raw_input()

	if userCommand == "uci":
		mprint("id name TomsCombiChess")
		mprint("id author tommie")
		mprint("uciok")

	if userCommand.startswith("option name"):
		mprint("uciok")

	if userCommand == "isready" :
		mprint("readyok")
	
	if userCommand.startswith("go"):
		startEngines()

	elif userCommand.startswith("position"):
		handlePosition(userCommand)

	elif userCommand == "exit":
		exit = True
	elif userCommand == "stop":
		sleep(300)
		mprint(moves[0])
		mprint("readyok")
		mprint("uciok")
	else:
		mprint("unknown command")
