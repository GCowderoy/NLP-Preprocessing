#!/usr/bin/python

import sys, fileinput, os
import xml.etree.ElementTree as ET


def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " Gamefile \n"
    sys.exit(1)
#give this function the game xml, e.g. q4nc4.games.xml
def getmoveIDs(gametree): 
  root = gametree.getroot()
  gamelist = []
  for child in root: 
    for element in child:
      #this section should 
      hrefline = element.get('href')
      #print hrefline
      if hrefline != None:

        myhref = extractTimes(hrefline)
        my1move = myhref[0].strip('id()') 
        my2move = myhref[2].strip('id()')
        if my2move != '':
          mymove = [my1move, my2move]
        else:
          mymove = [my1move]
        gamelist.append(mymove)
  return gamelist



def extractFname (hrefline): 
  #splits the href line by the # deliminater, to discard the filename
  out = hrefline.split("#")
  return out 

def extractTimes ( hrefline):
  #splits the ids up into a tuple
  split = extractFname(hrefline)
  newline = split[1]
  out = newline.partition("..")
  #print out
  return out


if __name__ == "__main__":
  usage(sys.argv)
  gametree = ET.parse(sys.argv[1])
  print getmoveIDs(gametree)

