import math
import random

import numpy as np
import cv2 as cv
from MusicUtils import MusicUtils
from Function import Function
from music21 import *
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert an .mxl file into a factal image')
    parser.add_argument('mxlFile', metavar='mxlFile', type=str, nargs='+',
                        help='a file for the program to analyze')
    parser.add_argument('-s, --show', dest='show',
                        action='store_true', default=False,
                        help='State whether to show the fractal at the end of the program running')
    args = parser.parse_args()

    fileName = parseFileName(args.mxlFile[0])

    size = 1000
    sizeOfImage = int(size*.35)
    myCanvas = np.zeros((size,size),dtype='uint8')
    myColorMap = np.zeros((size, size,3), dtype='uint8')
    notesFile = converter.parse(args.mxlFile[0])
    notesPlayed = []
    notes = []
    x = 0.0
    y = 0.0
    tx = 0.0
    ty = 0.0
    r_star = 0.0
    tempCol = 0

    MusicUtils.setupNotesForSongWithMusic21(notesFile, notes, notesPlayed)

    noteIndex = 0
    beatCounter = 0
    for loopNote in notes:

        if not isinstance(loopNote,list):
            notesPerBeat = 1
        else:
            notesPerBeat = len(loopNote)

        currThetaVals = []
        functions = []

        noteIndex = noteIndex + int(notesPerBeat)

        r = random.randint(0, 600) / 1000 + .05

        if notesPerBeat == 1:
            currThetaVals.append((loopNote.freq * math.pi / 180.0) * 5)
        else:
            for note in loopNote:
                currThetaVals.append((note.freq * math.pi / 180.0) * 5)

        for i in range(0, len(currThetaVals)):
            val = currThetaVals[i]
            functions.append(
                Function(r * math.cos(val), -r * math.sin(val), .7, r * math.sin(val), r * math.cos(val), .7,
                         loopNote.color if notesPerBeat == 1 else loopNote[i].color))

        notesPlayedIndex = 0
        for i in range(0, 10000):
            tx = x
            ty = y

            rndInt = random.randint(0,notesPerBeat)

            if(rndInt < len(functions)):
                x = functions[rndInt].val1 * tx + functions[rndInt].val2 * ty + functions[rndInt].val3
                y = functions[rndInt].val4 * tx + functions[rndInt].val5 * ty + functions[rndInt].val6
                tempCol = functions[rndInt].color
            else:
                x = tx * .5
                y = ty * .5
                tempCol = (255, 255, 255)

            rad = math.sqrt(x*x + y*y)

            # Figure out what this does
            if i % 2000 == 0:
                r_star=(rad+beatCounter) / 450

            if x < 0:
                r_star = r_star * -1

            if x != 0:
                theta = math.tan(y / x)
            else:
                theta = 0
            x_star = r_star * math.cos(theta)
            y_star = r_star * math.sin(theta)

            intx = int(x_star * (sizeOfImage*.7)) + int(size/2)
            inty = int(y_star * (sizeOfImage*.7)) + int(size/2)

            if intx < size and intx >= 0 and inty < size and inty >= 0:
                myCanvas[intx,inty] = myCanvas[intx,inty] + 1
                r = int((1.0 * int(myCanvas[intx,inty]) * int(myColorMap[intx,inty,2]) + tempCol[2]) / (int(myCanvas[intx,inty])+1))
                r = int((r + myColorMap[intx,inty,2]) /2)
                g = int((1.0 * int(myCanvas[intx,inty]) * int(myColorMap[intx,inty,1]) + tempCol[1]) / (int(myCanvas[intx,inty])+1))
                g = int((g + myColorMap[intx,inty,1])/2)
                b = int((1.0 * int(myCanvas[intx,inty]) * int(myColorMap[intx,inty,0]) + tempCol[0]) / (int(myCanvas[intx,inty])+1))
                b = int((b + myColorMap[intx,inty,0])/2)
                myColorMap[intx:intx+2, inty:inty+2, 2] = r
                myColorMap[intx:intx+2, inty:inty+2, 1] = g
                myColorMap[intx:intx+2, inty:inty+2, 0] = b

        currThetaVals = []
        functions = []
        beatCounter =  beatCounter + 1
        print(beatCounter)
    cv.imwrite('music/createdImages/'+fileName+'.jpg', myColorMap)
    print('Done!')

    if args.show:
        cv.imshow('Window', myColorMap)
        cv.waitKey(0)


def parseFileName(curr_file_name):
    character_to_split_on = '/' if '/' in curr_file_name else '\\'
    myArray = curr_file_name.split(character_to_split_on)
    adjustedFileName = myArray[len(myArray)-1][:-4]
    return adjustedFileName


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
