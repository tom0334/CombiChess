from combiChess import CombiChess

# file names for the engines. YOU CAN CHANGE THESE
engineFolder = "/engines/"
engineFileNames = ["stockfish5", "komodo8", "andscacs"]

# This starts combichess. Do NOT change or remove this!
CombiChess(engineFolder, engineFileNames).start()