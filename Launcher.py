#!/usr/bin/env python3

import argparse
import logging

from combiChess import CombiChess

# file names for the engines. YOU CAN CHANGE THESE
engineFolder = "./engines"
engineFileNames = ["stockfish5", "komodo8", "andscacs"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', help='Verbose output. Changes log level from INFO to DEBUG.')
    args = parser.parse_args()

    logger = logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO)

    # This starts combichess. Do NOT change or remove this!
    CombiChess(engineFolder, engineFileNames).start()
