#!/usr/bin/python
from __future__ import division
import os, sys, fileinput, glob
from collections import defaultdict
'''Script to calculate transition probabilities from Action-State pairs 
Works by taking a directory as input, reading listed files.
Then it creates an unordered hash table/dictionary to count the number of times the tuple s1,a1,s2 occur, for s1,s2 in S, a1 in A
This table is ordered and split into sets of s1,a1 
Then loop through the ordered matrix to calculate the count of s1,a1
This is used with Laplace smoothing to calculate T(s1,a1,s2) = [count(s1,a1,s2)+1]/[count(s1,a1) + K] where K = |S|^2 * |A|'''

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " directory \n"
    sys.exit(1)

def ReadFromDir(directory): 
  #for pattern in directory: 
  listing = os.listdir(directory)
  listing.sort()
  outlist = []
  for item in listing:
    fullitem = os.path.join(directory,item)
    outlist.append(fullitem)
  return outlist 

'''Function to get the counts of how often the state-action-state tuples occur. Returns an unordered dictionary'''
def countMoveTopic(dictlist):
  matrix = defaultdict(int)
  mydict = {}
  for infile in dictlist: 
    with open(infile, 'r') as f: 
      content = f.readlines()
      for i in range(1, len(content)):
        line1 = content[i-1]
        line2 = content[i]
        line1=line1.split(',')
        line2 =line2.split(',')
        m1 =line1[0]
        m2=line2[0]
        t1=line1[-1]
        t2=line2[-1]
        mykey = str(t1.rstrip()) + " , " + m1 +" , " + str(t2.rstrip())
        matrix[mykey]+=1
  return matrix

  
def getMoveList(mymatrix):
  movelist = []
  for key in mymatrix: 
    c = key.split(',')
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
          c = key.split(",")
          #print c[0], c[1], c[2]  
          if action == c[1] and c[0].find(str(x)) != -1 and c[2].find(str(y)) != -1:
            myitem = key.rstrip() ,  item
            myslice.append(myitem)
      mylist.append(myslice)
  return mylist

def getTransProbs( ordmatrix, movelist, statesize): 
  K = len(movelist)*(statesize**2)
  #print K
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
  directory = sys.argv[1]
  outlist = ReadFromDir(directory)
  mymatrix= countMoveTopic(outlist) 
  movelist = getMoveList(mymatrix)
  ordm = ordMatrix(mymatrix, movelist, 5)
  #for item in ordm:
  #  print item
  getTransProbs(ordm, movelist, 5)
  
  #getTransProbs(mymatrix, movelist, 5)
