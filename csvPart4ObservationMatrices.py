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
    print "Error: \n    Usage: " + argv[0] + " topicNumber CSVDirectory \n"
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
unused
def extractAllUtts(infile,outfile):
  with open(infile, 'r') as f:
    with open(outfile,'w') as fout:
      for line in f:
        #print extractUtt(line)
        fout.write(str(extractUtt(line)+ " "))
'''

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

def getMoveList(mymatrix):
  movelist = []
  for key in mymatrix: 
    c = key.split(';')
    move = c[2]
    movelist.append(move)
  myout = sorted(set(movelist))
  return myout

''' 
getObsList is for when the observations are not equal to the action set. 
'''
def getObsList(mymatrix):
  movelist = []
  for key in mymatrix: 
    c = key.split(';')
    move = c[4]
    movelist.append(move)
  myout = sorted(set(movelist))
  return myout

'''
Need to test this function - mostly for the conditional
If it works, then copy it over to csvPart3 for the transition matrices
This matters for the Laplace smoothing
'''
def addMissingItems(matrix, actlist, statesize, obslist):
  mymatrix = matrix
  for action in actlist:
    for x in range(0,statesize):
      for obs in obslist:
        for y in range(0,statesize):
          mykey = 'f' + " ; " + str(x) + " ; " +obs+ " ; " +str(y)+ " ; " +action+ " ; " +'g'
          if mykey in matrix.keys():
            continue
            #c = key.split(";")
          else:
            mymatrix[mykey] = 0
  return mymatrix
            
#need to check that key is in matrix            


'''
Ordering the matrix by  action,s2,observation, s1.  
Will need to add in any missing tuples here with a key value of 0
'''
def ordMatrix( matrix, movelist, statesize, obslist): 
  mylist = []
  #for obs in obslist: #observation is matrixkey[2]
    #print obs
  for action in movelist:   
    #print obs, action

    for x in range(0,statesize):
      myActSlice = []
      #print obs, action, x
      for obs in obslist: #observation is matrixkey[2]
        myslice=[]
        for y in range(0,statesize):
          #print obs, action, x, y
          
          for key,item in matrix.iteritems():
            c = key.split(";")
            #print obs, action, x, y 
            if obs == c[2] and action == c[4] and c[3].find(str(x)) != -1  and c[1].find(str(y)) != -1:
              #print item, c[0], c[5], "obs=",c[2], "action=",c[4], "s2=",c[3], "s1=", c[1]
              myitem = key.rstrip() ,  item
              myslice.append(myitem)
        if len(myslice) != 0:
          #print myslice  
          myActSlice.append(myslice)    
      if len(myActSlice) !=0:
        #print myActSlice
        mylist.append(myActSlice)
  return mylist


def getObsProbs( ordmatrix, movelist, statesize, obslist): 
  K = len(movelist)*(statesize)*len(obslist)
  print "O(o2,a1,s2) = [count(a1,s2,o2)+1]/[count(a1,s2) + K] where K = |S|*|A|*|O| "
  print "s1, a1, s2, o2, count(a1,s2,o2)+1, count(a1,s2) + K , O(o2,a1,s2)"
  print "K =", K
  mylist = []
  for actSlice in ordmatrix: 
    myoutDict = []
    counta1s2 = 0
    #print actSlice
    myNom = 0

    myinDict = OrderedDict()
    for myslice in actSlice:

      countObsa1s2 = 0
      #print myslice
      for element in myslice:
        key = element[0]
        value = element[1]
        #print key, value
        countObsa1s2 += value
        mykey = key.split(";")

        mynewkey = mykey[1]+" ; "+ mykey[2]+" ; "+ mykey[3]+" ; "+mykey[4]
      myNom+=countObsa1s2
      #print mynewkey, countObsa1s2 
      myinDict[mynewkey] = countObsa1s2
    myoutDict.append(myinDict)
    myoutDict.append(myNom)
    mylist.append(myoutDict)

  for myOutDict in mylist:
    #print myOutDict[0], myOutDict[1],"\n"
    print "count(a1,s2)=", myOutDict[1] 
    for myinDict, key in myOutDict[0].iteritems():
      mydenom = myOutDict[1] + K
      print myinDict, key, mydenom, (key+1)/mydenom
  print "s1, a1, s2, o2, count(a1,s2,o2), count(a1,s2) + K , O(o2,a1,s2)"

 

if __name__== "__main__":
  usage(sys.argv)
  topicNumber = int(sys.argv[1])
  classedDir = sys.argv[2]
  outlist = ReadFromDir(classedDir)

  mymatrix= countMoveTopic(outlist) 
  movelist = getMoveList(mymatrix)
  obslist = movelist
  #myFullMatrix = addMissingItems(mymatrix, movelist, topicNumber, obslist)
  ordm = ordMatrix(mymatrix, movelist, topicNumber, obslist)
  getObsProbs(ordm, movelist, topicNumber,obslist)

'''
  for i in ordm:
    for k in i:
      for j in k:
        print j
  #getTransProbs(ordm, movelist, topicNumber)

  for i, k in myFullMatrix.iteritems():
    print i, k
'''
