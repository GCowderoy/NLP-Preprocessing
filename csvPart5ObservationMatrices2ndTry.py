#!/usr/bin/python
from __future__ import division
import os, sys, fileinput, glob
from collections import OrderedDict, defaultdict
'''
To work with the .csv files
part1: to extract the utterances from the csv
Then use encodeToHash.py to prepare for openHTMM
When openHTMM has been used, then use part2 to assign topics. 
part2: to assign topics to the csv

part3: to calculate transition matrices from the CSV files that have had topics assigned 
Script to calculate transition probabilities from Action-State pairs 
Works by taking a directory as input, reading listed files.
Then it creates an unordered hash table/dictionary to count the number of times the tuple s1,a1,s2 occur, for s1,s2 in S, a1 in A
This table is ordered and split into sets of s1,a1 
Then loop through the ordered matrix to calculate the count of s1,a1
This is used with Laplace smoothing to calculate T(s1,a1,s2) = [count(s1,a1,s2)+1]/[count(s1,a1) + K] where K = |S|^2 * |A|

part4: to calculate observation matrices from the CSV files that have topics assigned 
Takes the CSV directory, works similar to part 3. Counts s1,a1,s2,o1, where o1 is the move from follower.  
'''

def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " topicNumber ClassedDirectory \n"
    sys.exit(1)
'''
NB that Classed files have 4 elements in line: f/g; move; utterance;topic#
'''

def ReadFromDir(directory): 
  #for pattern in directory: 
  listing = os.listdir(directory)
  listing.sort()
  outlist = []
  for item in listing:
    fullitem = os.path.join(directory,item)
    outlist.append(fullitem)
  return outlist 


def splitUtt(inline):
  outline = inline.split(";")
  return outline

def extractUtt(inline):
  outtup = splitUtt(inline)
  myUtterance = outtup[2]
  utterance= myUtterance.replace("null ","")
  utterance = utterance.replace(">","")
  utterance = utterance.strip('<')
  utterance = utterance.replace('"<','')
  #butterance = autterance.rstrip('>')
  #print utterance
  #utterance = butterance.rstrip()
  return utterance.rstrip()

'''
Note that getMoveList and getObsList both depend on mymatrix
'''

def keyList(dirList):
  keysList = set()
  for myfile in dirList:
    #print myfile
    with open(myfile, 'r') as infile:
      for line in infile:
        key = splitUtt(line)
        speaker = key[0]
        move = key[1]
        topic = key[3]
        mykey = speaker +" ; "+move+" ; "+topic
        #print mykey
        #if mykey not in keysList:
        keysList.add(str(mykey).rstrip())
  return keysList
'''
user should be 'g' to get the moves, and 'f' to get the observations 
'''
def getmoves(keysList, user):
  actlist = []
  for item in keysList:
    myitem = splitUtt(item)
    #print myitem[0], user
    if str(myitem[0]).strip() == user:
      act = myitem[1].strip()
      actlist.append(act)
  myout = sorted(set(actlist))
  return myout

def createkeys(actlist, obslist, statesize, user1, user2):
  mykeys = []
  for action in actlist:
    for x in range(0,statesize):
      for obs in obslist:
        for y in range(0,statesize):
           mykey = user1 +" ; " + str(y) +" ; " + obs +" ; " +str(x)+" ; " +action+" ; " +user2
           mykeys.append(mykey)
  return mykeys


'''
Give countMoveTopic the directory of classified utterances
'''
def countMoveTopic(dictlist):
  matrix = defaultdict(int)
  mydict = {}
  for infile in dictlist: 
    with open(infile, 'r') as f: 
      content = f.readlines()
      for i in range(1, len(content)):
        line1 = content[i-1]
        line2 = content[i]
        line1=splitUtt(line1)
        line2 =splitUtt(line2)
        speaker1 = line1[0]
        speaker2 = line2[0]
        move1 =line1[1]
        move2=line2[1]
        topic1=line1[-1]
        topic2=line2[-1]
        if speaker1 == speaker2:
          continue
        elif speaker2 =='g': #NB that this hardcodes it to search for the guide. The key is of the form f;s1;lastObs;s2;Action;g 
            mykey = str(speaker1 +" ; "+ topic1.rstrip()) + " ; " + move1 +" ; "  + str(topic2.rstrip() +" ; "+move2+" ; " + speaker2)
            matrix[mykey]+=1
  return matrix

def addMissingEntries(matrix, mykeys):
  myord = OrderedDict()
  for key in mykeys:
    if key in matrix:
      myord[key] = matrix[key]
      continue
    else:
      myord[key] = 0
  return myord

#Need to slice up myord by action, s2, observation

def slicingMatrix(ordMatrix, actlist, obslist, statesize):
  myOrdList = []
  for action in actlist:
    myActSlice = []
    for x in range(0, statesize):
      myStateSlice=[]
      for obs in obslist:
        myObsSlice =OrderedDict()
        #for y in range(0,statesize):
        for key,value in ordMatrix.iteritems():
          mykey = key.split(";")
          #print mykey[4], action, '\t' ,mykey[3], x, '\t' ,mykey[2], obs
          if action == mykey[4].strip() and mykey[3].find(str(x)) != -1 and obs == mykey[2].strip(): 
            myObsSlice[key] = value
            #print key, value
        myStateSlice.append(myObsSlice)
      myActSlice.append(myStateSlice)
    myOrdList.append(myActSlice)
  return myOrdList

'''
def getObsProbs(ordmatrix, movelist, statesize, obslist):
 K = len(movelist)*(statesize)*len(obslist)
  print "O(o2,a1,s2) = [count(a1,s2,o2)+1]/[count(a1,s2) + K] where K = |S|*|A|*|O| "
  print "s1, a1, s2, o2, count(a1,s2,o2)+1, count(a1,s2) + K , O(o2,a1,s2)"
  print "K =", K
  myoutdict = getObsValues(ordmatrix, movelist, statesize, obslist)
  for actstate in myinDict:
        print "count(a1,s1)=" , sum(actstate.values())
        denom = sum(actstate.values()) + K
        print "count(a1,s1)+K=", denom
        for key, value in actstate.iteritems():
          print key, value, denom, (value+1)/denom
        print '\n'

  print "s1, a1, s2, o2, count(a1,s2,o2), count(a1,s2) + K , O(o2,a1,s2)"

'''

def obsValues(OrdMatrix):
  myOrdList = []
  for actslice in OrdMatrix:
    myActList = []
    for stateslice in actslice:
      #print '\n'
      myObsSlice = OrderedDict()
      for obsslice in stateslice:        
        mykey = obsslice.keys()[-1]
        #print mykey," ; ", sum(obsslice.values())  
        myObsSlice[mykey] = sum(obsslice.values())
      myActList.append(myObsSlice)
    myOrdList.append(myActList)
  return myOrdList

def getObsProbs(OrdMatrix, movelist, statesize, obslist):
  #K = len(movelist)*(statesize)*len(obslist)
  K = len(movelist)
  #print "O(o2,a1,s2) = [count(a1,s2,o2)+1]/[count(a1,s2) + K] where K =  |A|" #|S|*|A|*|O|
  #print "s1, a1, s2, o2, count(a1,s2,o2)+1, count(a1,s2) + K , O(o2,a1,s2)"
  #print "K =", K
  for action in OrdMatrix:
    for obsDict in action:
      denom = sum(obsDict.values()) +K
      #print "count(a1,s1)+K=", denom
      for i,k in obsDict.iteritems():
        #print i,k, denom, (k+1)/denom
        print (k+1)/denom
      #print '\n'  

if __name__== "__main__":
  usage(sys.argv)
  topicNumber = int(sys.argv[1])
  classedDir = sys.argv[2]
  outlist = ReadFromDir(classedDir)
 
  mykeys = keyList(outlist)

  actions = getmoves(mykeys, 'g')
  obslist = getmoves(mykeys,'f')
  
  mykeys = createkeys(actions, obslist, topicNumber, 'f', 'g')
  
  mymatrix= countMoveTopic(outlist) 

  ordm = addMissingEntries(mymatrix, mykeys)
  #ordm = ordMatrix(myFullMatrix, moves, topicNumber, obs)
  #getObsProbs(myFullMatrix, moves, topicNumber,obs)
  mySlices = slicingMatrix(ordm, actions, obslist, topicNumber)
  #print mySlices
  #getObsValues( mySlices, actions, topicNumber, obslist)
  obsV = obsValues(mySlices)
  getObsProbs(obsV, actions, topicNumber, obslist)
'''
  for actslice in mySlices:
    for stateslice in actslice:
      print '\n'
      for obsslice in stateslice:
        mykey = obsslice.keys()[0]
        print mykey, sum(obsslice.values())
        #for i,k in obsslice.iteritems():
        #  print i, '\t', k



  for i,k in orm.iteritems():
    print i,k


for i, k in myFullMatrix.iteritems():
    print i, k
  for i in ordm:
    for k in i:
      for j in k:
        print j
  #getTransProbs(ordm, movelist, topicNumber)
'''
