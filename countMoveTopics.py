#!/usr/bin/python

import os, sys, fileinput, glob
from collections import defaultdict
#matrix = collections.defaultdict()
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

        #manage(content[i-1],content[i])
       

def manage(line1, line2):
  line1=line1.split(',')
  line2 =line2.split(',')
  m1 =line1[0]
  m2=line2[0]
  t1=line1[-1]
  t2=line2[-1]
  mykey = str(t1) + " , " + m1 +" , " + str(t2)

  #matrix[t1+m1+t2]++
  
def getMoveList(mymatrix):
  movelist = []
  for key in mymatrix: 
    c = key.split(',')
    


if __name__== "__main__":
  usage(sys.argv)
  directory = sys.argv[1]
  outlist = ReadFromDir(directory)
  mymatrix= countMoveTopic(outlist) 
  #print mymatrix
  for key,item in mymatrix.iteritems():
    print key.rstrip() + " : "+ str(item)
  

