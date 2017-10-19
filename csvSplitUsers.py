#!/usr/bin/python

import os, sys, fileinput, glob

'''
To work with the .csv files

SplitUsers: to separate the follower and guide utterances. Used for creating the transition matrices. 
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
'''


def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " CSVdirectory \n"
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

def readUser(inline):
  splitLine = splitUtt(inline)
  user = splitLine[0]
  return user

def filterF(inline):
  user = readUser(inline)
  if user == 'f':
    return inline
  else:
    return None

def filterG(inline):
  user = readUser(inline)
  if user == 'g':
    return inline
  else:
    return None

def filterAll(infile, user, outfile):
  with open(infile, 'r') as f:
    with open(outfile,'w') as fout:
      for line in f: 
        if user == 'g':
          myFilter = filterG(line)
        elif user == 'f':
          myFilter = filterF(line)
        if myFilter != None:
          fout.write(str(myFilter))

def filterDir(dirList, user):
  for i in dirList: 
    infile = i
    outfile = i + str(user) + '.out'
    filterAll(infile, user, outfile)



if __name__== "__main__":
  usage(sys.argv)
  directory = sys.argv[1]
  dirList = ReadFromDir(directory)

  filterDir(dirList, 'f')
  filterDir(dirList, 'g')
