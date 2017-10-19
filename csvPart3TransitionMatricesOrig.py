#!/usr/bin/python
from __future__ import division
import os, sys, fileinput, glob
from collections import defaultdict
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
        move1 =line1[1]
        move2=line2[1]
        topic1=line1[-1]
        topic2=line2[-1]
        mykey = str(topic1.rstrip()) + " ; " + move1 +" ; "  + str(topic2.rstrip())
        matrix[mykey]+=1
  return matrix

def getMoveList(mymatrix):
  movelist = []
  for key in mymatrix: 
    c = key.split(';')
    move = c[1]
    movelist.append(move)
  myout = sorted(set(movelist))
  return myout

'''Ordering the matrix by action, s1, s2 '''
def ordMatrix( matrix, movelist, statesize): 
  mylist = []
  for action in movelist:
    for x in range(0,statesize):
      myslice=[]
      for y in range(0,statesize):
        for key,item in mymatrix.iteritems():
          c = key.split(";")
          #print c[0], c[1], c[2]  
          if action == c[1] and c[0].find(str(x)) != -1 and c[2].find(str(y)) != -1:
            myitem = key.rstrip() ,  item
            myslice.append(myitem)
      mylist.append(myslice)
  return mylist

def getTransProbs( ordmatrix, movelist, statesize): 
  K = len(movelist)*(statesize**2)
  print "T(s1,a1,s2) = [count(s1,a1,s2)+1]/[count(s1,a1) + K] where K = |S|^2 * |A| \n K; s1; a1; s2; count +1; count + K; probability"
  for partition in ordmatrix: 
    count = 0
    for item in partition:
      key = item[0]
      value = item[1]
      count += value
    denom = count + K
    for item in partition:
      key = item[0]
      value =item[1]
      nom = value +1
      prob = nom / denom
      print K, key, nom, denom, prob


if __name__== "__main__":
  usage(sys.argv)
  topicNumber = int(sys.argv[1])
  classedDir = sys.argv[2]
  outlist = ReadFromDir(classedDir)
  mymatrix= countMoveTopic(outlist) 
  movelist = getMoveList(mymatrix)

  ordm = ordMatrix(mymatrix, movelist, topicNumber)
  getTransProbs(ordm, movelist, topicNumber)
