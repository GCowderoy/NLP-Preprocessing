#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys

def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " moves timed-units"
    sys.exit(1)

def extractMoves( tree  ):
  #this function gives the 'move' and the tuple 'start', 'end' for every node in the tree
  root = tree.getroot()
  myout = []
  for child in root:
    #searching for the move tags
    if child.tag == 'move':
      mylist =[]
      #getting the move labels - these correspond to the coding scheme
      for attribute in child.attrib:
        if attribute =='label':
          mylist.append( child.attrib[attribute] )
      #getting the time units out
      for element in child:
        hrefline = element.get('href')
        #need to parse the href
        mylist.append( extractTimes(hrefline))
      myout.append( mylist)
  return myout

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

def getUtterances(timetree, myout):
  root = timetree.getroot()
  myutt=""
  for item in myout:
    #myout is a list of move,(start,end). This part loops through them, and ignores the deliminator.
    move= item[0]
    tup = item[1]
    mystart = tup[0]
    start = mystart.strip('id()')
    if '..' in tup:
      myend = tup[2]
    else:
      myend = tup[0]
    end = myend.strip('id()')

    for child in root:
      #if child.tag == "tu":
      for attribute in child.attrib:
        if attribute == 'id':
          timedUnit = child.attrib[attribute]
          if child.text == None:
            text = ""
          else: 
            text = child.text + " "            
          if timedUnit == start :
            #when the start utterance
            if timedUnit == end:
              #for the one word utterances
              myutt = child.text
              print move +" , " +start +" , " + end +" , " + myutt
              myutt = ""
            else:
              myutt = text
              #print move +" , " +timedUnit+" , " + myutt
          elif timedUnit == end:
            #found end utterance
            myutt = myutt + text
            print move +" , " +start +" , " + end +" , " + myutt
            myutt = ""
          else:
            #utterances that are neither start or end
            myutt = myutt + text
            #print move, start, end, myutt



if __name__ == "__main__":
  usage(sys.argv)
  tree = ET.parse(sys.argv[1])
  timetree = ET.parse(sys.argv[2])
  myout= extractMoves(tree)
  #for item in myout:
  #  print item
  getUtterances(timetree, myout)
