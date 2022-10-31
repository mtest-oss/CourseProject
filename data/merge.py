import math
import sys
import time
import metapy
import pytoml
import time
import pandas as pd
import re


linecount = 0;
LineLimit = 5
tmpline = "";
seconds=0
#valuedict = dict()
index = 0

finalDf = pd.DataFrame(columns=['Index','Time','Strvalue'])

tempDf = pd.DataFrame(columns=['Index','Time','Strvalue'])

#with open('cranfield/subtitle.dat') as f:
with open('cranfield/subtitles-en.vtt') as f:
    for line in f:
        confor = 0
        line = line.strip()
        #print("line ", line)
        #line = f.readline().strip()
        #print("line: len of line ", line, len(line));
        if (line == "webVTT"):
            #print("line:", line)
            confor = 1
            seconds = 0
        elif (line == "WEBVTT"):
            #print("line:", line)
            confor = 1
            seconds = 0
        elif (line == "[MUSIC]"):
            #print("line", line)
            confor = 1
            seconds = 0
        elif ((None != (re.search(r'\d', line)))):
            if ( len(line) < 4):
                #print("number 1: ", line)
                #seconds = 0
                confor = 1
            elif (len(line) == 29):
                first = re.search(r'\d+:\d+:\d+.\d+', line)
                #print("Time 1: ", line)
                #print("Time sliced: ", first)
                sec = first.group()
                #print("Time firstpart: ", first.group())
                #print("sec", sec[1:2])
                h = int(sec[0]) * 10 + int(sec[1])
                m = int(sec[3]) * 10 + int(sec[4])
                s = int(sec[6]) * 10 + int(sec[7])
                if (seconds == 0):
                    print("Seconds are zero, so update it");
                    seconds = (int(h) * 60 * 60) + ((int(m)) * 60) + (int(s))
                print("seconds ",(seconds))
                #+ (type(int(m))) * 60 + type(int(s)) 
                #print(" h , m , s" , h, m, s)
                #print("seconds ", seconds)
                #t = first[0:1] * 60 * 60 + first[2:
                confor = 1
        elif (len(line) == 0):
            confor = 1
        #print(re.search(r'\d+', line));
        #time_struct = time.strptime(line, '%H:%M:%S')
        #print("time_struct ", time_struct);
        
        #line1 = f.readline().strip()
        #print("Line ", line)
        if (confor == 0):
            #line1 = line
            if (linecount < 5):
                linecount = linecount + 1
                tmpline = tmpline + " " + line
                if (linecount == 1):
                    #if ((math.isnan(seconds) == False)):
                        finalDf.loc[len(finalDf)] = [index,seconds,tmpline]
                        finalDf
                        index = index + 1
            else:
                print("tmpline: ", seconds, " ", tmpline)
                linecount = 0
                seconds = 0
                tmpline = "" 
        
            
        
    print("tmpline: ", seconds, " ", tmpline)
    print("dict: :,", finalDf)
    #print("line1: ", line1)
    #line2 = f.readline().strip()
    #print( line1 + " " + line2)
    #print("line2: ", line2)
    #if (linecount < 4) then:
    #    tmpline = tmpline + line1
    #else:
    #    linecount = 0
    #    tmpline = ""
    #for other_line in f:
    #    print other_line.strip()