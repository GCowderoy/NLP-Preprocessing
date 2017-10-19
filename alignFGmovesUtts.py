#!/usr/bin/python

import sys, fileinput, os
import xml.etree.ElementTree as ET
from collections import OrderedDict
#from itertools import islice
'''Script to align guide-moves and follower-moves with utterances into single file 
This is to produce the observation matrices '''

def usage(argv):
  if len(argv) != 6:
    print "Error: \n    Usage: " + argv[0] + " Game fMoves gmoves fTU gTU \n"
    sys.exit(1)

#given a directory path, returns a sorted full path list
def ReadFromDir(directory): 
  #for pattern in directory: 
  listing = os.listdir(directory)
  listing.sort()
  outlist = []
  for item in listing:
    fullitem = os.path.join(directory,item)
    outlist.append(fullitem)
  return outlist 

#give this function the game xml, e.g. q4nc4.games.xml. Need to remove duplicates? 
def getmoveIDs(gametree): 
  root = gametree.getroot()
  gamelist = []
  for child in root: 
    for element in child:
      #Check that this goes through every element - some items are missing from gamelist
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

def extractMoves( tree ):
  #this function gives the 'move label' and the tuple 'start', 'end' for every node in the tree for follower/guide moves
  #It will also give the move id (the if attrib == id condition)
  root = tree.getroot()
  myout = []
  for child in root:
    #searching for the move tags
    if child.tag == 'move':
      mylist =[]
      #getting the move labels - these correspond to the coding scheme
      for attribute in child.attrib:
        #This condition writes the id to the list
        if attribute =='id':
          #print child.attrib[attribute]
          mylist.append(child.attrib[attribute])
        #This condition writes the move to the list
        if attribute =='label':
          mylist.append( child.attrib[attribute] )
      #getting the time units out
      for element in child:
        hrefline = element.get('href')
        #need to parse the href
        mylist.append(extractTimes(hrefline))
      myout.append(mylist)
  return myout



def extractFname (hrefline): 
  #splits the href attrib line by the # deliminater, to discard the filename
  out = hrefline.split("#")
  return out
  
def extractTimes ( hrefline):
  #splits the href attrib ids up into a tuple
  #split[0] is the filename; this returns the timed unit sections
  split = extractFname(hrefline)
  newline = split[1]
  out = newline.partition("..")
  #print out
  return out

def getUtterances(timetree, myout):
  '''this function gives the moveid (from move.xml, and corresponding in the game.xml), the move label (from the move.xml) and the utterance (from timed-units.xml)
  This is as an OrderedDict, so it retains the input order'''
  root = timetree.getroot()
  myutt=""
  #uttList=OrderedDict()
  uttList = []
  for item in myout:
    #myout is a list of moveid, move,(start,end). This part loops through them, and ignores the deliminator.
    moveid= item[0]
    move = item[1]
    tup = item[2]
    
    mystart = tup[0]
    #print mystart
    start = mystart.strip('id()')
    myend = tup[-1]
    end = myend.strip('id()')
    if end == "":
      end = start
    #print item, start, end, tup

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
              #fout =  move+", " + myutt
              #print fout
              #uttList[moveid]=fout
              fout = moveid + ", "+move+", "+myutt
              uttList.append(fout)
              myutt = ""
            else:
              myutt = text
              #print tup, move +" , " +timedUnit+" , " + myutt
          elif timedUnit == end:
            #found end utterance
            myutt = myutt + text
            #fout =  move +", "   + myutt
            #print fout
            #uttList[moveid]=fout
            fout = moveid + ", "+move+", "+myutt
            uttList.append(fout)
            myutt = ""
          else:
            #utterances that are neither start or end
            myutt = myutt + text
            #print move, start, end, myutt
    
  return uttList

def moveList(uttList):
  movelist = []
  for item in uttList: 
    out =item.split(",")
    moveid = out[0]
    movelist.append(moveid)
  return movelist

def toDict(uttList):
  movelist = moveList(uttList)
  uttDict = OrderedDict()
  #uttDict ={}
  for item in uttList: 
    out = item.split(",")
    c = out[1:]
    for element in movelist: 
      if out[0] == element: 
        uttDict[element] = c
  return uttDict

#gamelist from getmoveIDs(gametree); fUtts from getUtterances on follower; gUtts from getUtterances on guide;
def alignFG(gamelist, fUtts, gUtts):
  flist = moveList(fUtts)
  fdict =toDict(fUtts)
  glist =moveList(gUtts)
  gdict = toDict(gUtts)
  loc1 = None
  loc2 = None
  for item in gamelist:
    moveStart = item[0]
    if len(item) == 2:
      moveEnd = item[1]
    else:
      moveEnd = None 
    #if moveStart.find('f') != -1: 
    #  print moveStart, moveEnd , ","
    for moveid in flist:     
      if moveid  == moveStart and moveEnd == None:
        print moveid , fdict[moveid]
      if moveEnd != None and moveEnd.find('f') != -1: 
        #print moveEnd, moveid
        if moveid == moveStart: 
          loc1 = flist.index(moveid)
          #print moveid, loc1
          continue
        elif moveid == moveEnd:
          #print moveEnd
          loc2 = flist.index(moveid)
          #print moveid, loc2
    
    if loc1 != None and loc2 != None: 
      #want to find locations of loc1, loc2 in flist, get a sublist of flist. Then iterate over sublist, printing out key, values that match from fdict. 
      sublist = flist[loc1:loc2+1]
      #print sublist
      for item in sublist: 
        print item, fdict[item]
      loc1, loc2 = None, None

    if loc2 == None and loc1 != None: 
      moveid = flist[loc1]
      print moveid, fdict[moveid]
      loc1, loc2 = None, None

    for moveid in glist:     
      if moveid  == moveStart and moveEnd == None:
        print moveid , gdict[moveid]
      if moveEnd != None and moveEnd.find('g') != -1: 
        #print moveEnd, moveid
        if moveid == moveStart: 
          loc1 = glist.index(moveid)
          #print moveid, loc1
          continue
        elif moveid == moveEnd:
          #print moveEnd
          loc2 = glist.index(moveid)
          #print moveid, loc2
    
    if loc1 != None and loc2 != None: 
      #want to find locations of loc1, loc2 in flist, get a sublist of glist. Then iterate over sublist, printing out key, values that match from gdict. 
      sublist = glist[loc1:loc2+1]
      #print sublist
      for item in sublist: 
        print item, gdict[item]
      loc1, loc2 = None, None

    if loc2 == None and loc1 != None: 
      moveid = glist[loc1]
      print moveid, gdict[moveid]
      loc1, loc2 = None, None



    '''for moveid, f  in fdict.iteritems(): 
      if moveid == moveStart and moveEnd == None: 
        print moveid, f
      if moveEnd != None:
         if moveid == moveStart: 
           loc1 = moveid
           #print moveid, f
         elif moveid == moveEnd: 
           #print moveid, f
           loc2 = moveid
    #if loc1 != None and loc2 != None: 
      #So, loc1 is the start key, loc2 is the end key. Want to slice the dictionary up, and print the values for this slice. 
      #print fUtts.keys()[loc1: loc2]
      #print fUtts. 

#when it works for f, copy paste for gUtts - or to a separate function'''
    
        


if __name__ == "__main__":
  usage(sys.argv)
  gametree = ET.parse(sys.argv[1])
  fmoves = ET.parse(sys.argv[2])
  gmoves = ET.parse(sys.argv[3])
  ftimetree = ET.parse(sys.argv[4])
  gtimetree = ET.parse(sys.argv[5])
  gamelist = getmoveIDs(gametree)
  fmovelist = extractMoves(fmoves)
  gmovelist = extractMoves(gmoves)

  #for item in gamelist:
  #  print item
  #for item in fmovelist:
  #  print item
  #for item in gmovelist:
  #  print item

  fUtts = getUtterances(ftimetree, fmovelist)
  gUtts = getUtterances(gtimetree, gmovelist)
  #glist = getmovelist(gUtts)
  alignFG(gamelist, fUtts, gUtts)
  #for item, value in orderedDict(fUtts).iteritems():
  #  print item, value
  #flist = moveList(fUtts)
  fdict = toDict(fUtts)
  gdict =toDict(gUtts)
  '''for key, item in gdict.iteritems(): 
    print key, item
  for element in gamelist: 
    print element'''
#for item in element:
      #if item.find('.f.') != -1:
      #print element


  
  
  
