import math
import sys
import time
import pandas as pd
import re
import os
import numpy as np

linecount = 0;
LineLimit = 5
tmpline = "";
seconds=0
index = 0
initialseconds = 0

file_exists = os.path.exists('corpus.txt')
#print("file_exists", file_exists)
if file_exists == True:
    print("Remove existing file")
    os.remove("corpus.txt")

for filename in os.listdir('./Data/Subtitles/'):
    if filename.endswith('.vtt'):       
        index = index + 1
#        print("file , index ", filename, index)
        with open(os.path.join('./Data/Subtitles', filename)) as f:
            for line in f:
                line = line.strip()
                confor = 0
                if (line == "webVTT"):
                    confor = 1
                    seconds = 0
                elif (line == "WEBVTT"):
                    confor = 1
                    seconds = 0
                elif (line == "[MUSIC]"):
                    confor = 1
                    seconds = 0
                elif (line == "[INAUDIBLE]"):
                    confor = 1
                    seconds = 0
                elif ((None != (re.search(r'\d', line)))):
                    if ( len(line) < 4):
                        confor = 1
                    elif (len(line) == 29):
                        #print("line ", line)
                        first = re.search(r'\d+:\d+:\d+.\d+', line)
                        #print("first", first)
                        if (first != None):
                            sec = first.group()
                            h = int(sec[0]) * 10 + int(sec[1])
                            m = int(sec[3]) * 10 + int(sec[4])
                            s = int(sec[6]) * 10 + int(sec[7])
                            if (seconds == 0):
                            #print("Seconds are zero, so update it");
                                seconds = (int(h) * 60 * 60) + ((int(m)) * 60) + (int(s))
                        #print("seconds ",(seconds))
                        #print(" h , m , s" , h, m, s)
                        #print("seconds ", seconds)
                        #t = first[0:1] * 60 * 60 + first[2:
                            confor = 1
                elif (len(line) == 0):
                    confor = 1
                
                if (confor == 0):
                    #line1 = line
                    if (linecount < 5):
                        linecount = linecount + 1
                        tmpline = tmpline + " " + line
                        if (linecount == 1):
                            initialseconds = seconds
                            #print("line ", line)
                    else:
                        #print("tmpline: ", seconds, " ", tmpline)
                        tmpline = tmpline.replace('[MUSIC]', '')
                        tmpline = tmpline.replace('[INAUDIBLE]', '')
                        tmpline = tmpline.replace('[SOUND]', '')
                        wline = str(index) + " " + str(seconds) + " " + tmpline
                        #print("wline ", wline)
                        with open('corpus.txt', 'a') as f:
                            f.write(wline)
                            f.write('\n')
                        linecount = 0
                        seconds = 0
                        tmpline = ""