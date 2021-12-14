import math
import random

import numpy as np
import cv2 as cv
import imageio
from MusicUtils import MusicUtils
from Function import Function
from music21 import *
import argparse
import copy
from MyQR import myqr as mq

def main():
    parser = argparse.ArgumentParser(description='Convert an .mxl file into a factal image')
    parser.add_argument('mxlFile', metavar='mxlFile', type=str, nargs='+',
                        help='a file for the program to analyze')
    parser.add_argument('-s, --show', dest='show',
                        action='store_true', default=False,
                        help='State whether to show the fractal at the end of the program running')
    parser.add_argument('-g, --gif', dest='gif',
                        action='store_true', default=False,
                        help='State whether to show the fractal being created when running')
    args = parser.parse_args()

    # Specify resolution
    resolution = (3000, 3000)
    # Specify video codec
    codec = cv.VideoWriter_fourcc(*"mp4v")
    # Specify name of Output file
    video_name = "Recording.mp4"
    # Specify frames rate. We can choose any
    # value and experiment with it
    fps = 60.0
    # Creating a VideoWriter object
    out = cv.VideoWriter('test1.mp4',codec, fps, resolution,True)

    fileName = parseFileName(args.mxlFile[0])

    size = 3000
    sizeOfImage = int(size*.45)
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
    image_gif = []

    MusicUtils.setupNotesForSongWithMusic21(notesFile, notes, notesPlayed)

    beatCounter = 0
    for loopNote in notes:

        if not isinstance(loopNote,list):
            notesPerBeat = 1
        else:
            notesPerBeat = len(loopNote)

        currThetaVals = []
        functions = []

        # determines how wide initial vals can move from x-axis
        rand = random.randint(0,600)
        r = (rand / 600) + .05

        if notesPerBeat == 1:
            currThetaVals.append((loopNote.freq * math.pi / 180.0) * 5)
        else:
            for note in loopNote:
                currThetaVals.append((note.freq * math.pi / 180.0) * 5)

        for j in range(0, len(currThetaVals)):
            val = currThetaVals[j]
            #why .7 ?
            #Function here is for circles; if you adjust the +/- of the variables, the image changes
            functions.append(
                Function(r * math.cos(val), -r * math.sin(val), .7, r * math.sin(val), r * math.cos(val), .7,
                         loopNote.color if notesPerBeat == 1 else loopNote[j].color))

        for i in range(0, 10000):
            tx = x
            ty = y

            rndInt = random.randint(0,notesPerBeat)

            if(rndInt < len(functions)):
                #ax + by + c = x | y
                x = functions[rndInt].val1 * tx + functions[rndInt].val2 * ty + functions[rndInt].val3
                y = functions[rndInt].val4 * tx + functions[rndInt].val5 * ty + functions[rndInt].val6
                tempCol = functions[rndInt].color
            else:
                x = tx * .5
                y = ty * .5
                tempCol = (255, 255, 255)

            rad = math.sqrt(x*x + y*y)

            # Determines thickness of annuli
            if i % 2000 == 0:
                r_star=(rad+beatCounter) / 250

            #Required for always positive radii
            if x < 0:
                r_star = r_star * -1

            if x != 0:
                theta = math.tan(y / x)
            else:
                theta = 0
            x_star = r_star * math.cos(theta)
            y_star = r_star * math.sin(theta)

            intx = int(x_star * (sizeOfImage*.9)) + int(size/2)
            inty = int(y_star * (sizeOfImage*.9)) + int(size/2)

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
        if args.show and args.gif:
            out.write(myColorMap)
            colorMapCopy = copy.deepcopy(myColorMap)
            image_gif.append(colorMapCopy)
            cv.imshow('Window', myColorMap)
            cv.waitKey(10)


        beatCounter =  beatCounter + notesPerBeat
        print(beatCounter)
    out.release()
    cv.imwrite('music/createdImages/'+fileName+'.jpg', myColorMap)
    #
    #
    # imageio.mimsave('movie.gif', image_gif, duration=.015 )
    #
    #
    # mq.run(words = 'https://www.topcoder.com', version = 1,
    #        picture = 'movie.gif',
    #        colorized = True,
    #        save_name = 'myQRCode.gif')


    print('Done!')
    if args.show and not args.gif:
        cv.imshow('Window', myColorMap)
        # cv.waitKey(0)


def parseFileName(curr_file_name):
    character_to_split_on = '/' if '/' in curr_file_name else '\\'
    myArray = curr_file_name.split(character_to_split_on)
    adjustedFileName = myArray[len(myArray)-1][:-4]
    return adjustedFileName


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
