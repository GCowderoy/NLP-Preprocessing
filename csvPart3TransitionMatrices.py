#!/usr/bin/python
from __future__ import division
import os, sys, fileinput, glob
from collections import defaultdict, OrderedDict
'''
To work with the .csv files
part1: to extract the utterances from the csv
Then use encodeToHash.py to prepare for openHTMM
When openHTMM has been used, then use part2 to assign topics. 
part2: to assign topics to the csv

part3: to calculate transition matrices from the CSV files that have had topics assigned 
Need to edit for sparse data, similar to part 5.
Script to calculate transition probabilities from Action-State pairs 
Works by taking a directory as input, reading listed files.
Then it creates an unordered hash table/dictionary to count the number of times the tuple s1,a1,s2 occur, for s1,s2 in S, a1 in A
This table is ordered and split into sets of s1,a1 
Then loop through the ordered matrix to calculate the count of s1,a1
This is used with Laplace smoothing to calculate T(s1,a1,s2) = [count(s1,a1,s2)+1]/[count(s1,a1) + K] where K = |S|^2 * |A|

part4: to calculate observation matrices from the CSV files that have topics assigned 
Use part 5 instead (more complete)
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

def keyList(dirList, user):
  keysList = set()
  for myfile in dirList:
    #print myfile
    with open(myfile, 'r') as infile:
      for line in infile:
        key = splitUtt(line)
        speaker = key[0]
        move = key[1]
        topic = key[3]
        if user==speaker.strip():
          mykey = speaker +" ; "+move+" ; "+topic
        #print mykey
        #if mykey not in keysList:
        keysList.add(str(mykey).rstrip())
  #for i in keysList:
  #  print i
  return keysList

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

'''
createkeys gives keys ordered by action, state1, state2
'''
def createkeys(actlist, statesize, user1, user2):
  mykeys = []
  for action in actlist:
    for x in range(0,statesize):
      for y in range(0,statesize):
        mykey = user1 +" ; "+str(x)+" ; " +action+" ; " +str(y)+" ; " +user2
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
      for i in range(0, len(content)):
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
        #if str(user).strip() == speaker1.strip():
        mykey = speaker1 + " ; " +str(topic1.rstrip()) + " ; " + move1 +" ; "  + str(topic2.rstrip())+" ; "  +speaker2
        matrix[mykey]+=1
  #for i,k in matrix.iteritems():
  #  print i,k
  return matrix

'''
This combines countMoveTopic and createkeys to give a dictionary ordered by action, state1, state2
'''
def addMissingEntries(matrix, mykeys):
  myord = OrderedDict()
  for key in mykeys:
    #print key
    if key in matrix:
      myord[key] = matrix[key]
      continue
    else:
      myord[key] = 0
  return myord

def sliceTransMatrix(ordMatrix, actionList, statesize):
  myordList = []
  for action in actionList:
    myActSlice = []  
    for x in range(0, statesize):
      myOrd=OrderedDict()
      for y in range(0,statesize):
        for key,value in ordMatrix.iteritems():
          mykey = key.split(";")
          if action == mykey[2].strip() and mykey[1].find(str(x)) != -1 and mykey[3].find(str(y)) != -1:
            myOrd[key] = value
      myActSlice.append(myOrd)
    myordList.append(myActSlice)
  return myordList

def getTransProbs( slicedMatrix, movelist, statesize): 
  #K = len(movelist)*(statesize**2)
  K = statesize
  #print "T(s1,a1,s2) = [count(s1,a1,s2)+1]/[count(s1,a1) + K] where K = |S| =",K,"\n K; s1; a1; s2; count +1; count + K; probability"
  #print movelist
  for actslice in slicedMatrix: 
    count = 0
    #print "act:"
    for ordM in actslice:
      #print ordM
      denom = sum(ordM.values()) + K
      #print "count(a1,s1)=" , sum(ordM.values()), "count(a1,s1)+K = ", denom  #ordM.items[1] 
      for key,value in ordM.iteritems():
        #print key, '\t',value, denom, '\t', (value+1)/denom        
        print (value+1)/denom
    #print '\n'

if __name__== "__main__":
  usage(sys.argv)
  topicNumber = int(sys.argv[1])
  classedDir = sys.argv[2]
  outlist = ReadFromDir(classedDir)

  mymatrix= countMoveTopic(outlist) 
  keysList = keyList(outlist,'g')
  actionList = getmoves(keysList, 'g')
  #mykeys1 = createkeys(actionList, topicNumber, 'g','g')
  mykeys2=createkeys(actionList, topicNumber, 'g','f')
  #mykeys = mykeys1+mykeys2
  mykeys = mykeys2
  #To adjust for other users, or for only g/f utterance pairs, change ordMatrix to take mykeys2
  ordMatrix = addMissingEntries(mymatrix, mykeys)
  #
  slicedMatrix = sliceTransMatrix(ordMatrix, actionList, topicNumber)
  #
  getTransProbs(slicedMatrix, actionList, topicNumber)
  
