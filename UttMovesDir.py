#!/usr/bin/python

import sys, fileinput, os
import xml.etree.ElementTree as ET

def usage(argv):
  if len(argv) != 4:
    print "Error: \n    Usage: " + argv[0] + " filelist directory1 directory2\n"
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

def matchfnames(dirlist1, dirlist2, flist): 
  mylist = []
  with open(flist,'r') as f:
    for line in f: 
      myline = line.rstrip()
      #print line
      for item in dirlist1:
        #print myline ,item
        if item.find(str(myline)) != -1:
          for element in dirlist2:
            if element.find(str(myline)) != -1:
              move = myline
              fname1=item
              fname2= element
              tup = [move, fname1, fname2]
              #print tup
              mylist.append(tup)
  return mylist

def extractMoves( tree ):
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
  uttList=[]
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
              fout = move +" , " +start +" , " + end +" , " + myutt
              uttList.append(str(fout)+ "\n")
              myutt = ""
            else:
              myutt = text
              #print move +" , " +timedUnit+" , " + myutt
          elif timedUnit == end:
            #found end utterance
            myutt = myutt + text
            fout = move +" , " +start +" , " + end +" , " + myutt
            uttList.append(str(fout)+ "\n")
            myutt = ""
          else:
            #utterances that are neither start or end
            myutt = myutt + text
            #print move, start, end, myutt
  return uttList
#need to set getUtterances to return a set of strings; 


def getAllMoveUtt(tuplist):
  for c in tuplist:
    fname = c[0]+".TUMaligned"
    move = c[1]
    tu = c[2]
    tree = ET.parse(move)
    timetree = ET.parse(tu)
    myout = extractMoves(tree)
    fwrite = getUtterances(timetree, myout)
    #mywrite= str(fwrite).split()
    #print mywrite
    with open(fname,'w') as f:
      for item in fwrite:
        if item != None:
          #print item
          f.write(str(item))

  
if __name__ == "__main__":
  usage(sys.argv)
  
  filelist = sys.argv[1]
  directory1 = sys.argv[2]
  directory2= sys.argv[3]
  dir1 = ReadFromDir(directory1)
  dir2 = ReadFromDir(directory2)
  mylist = matchfnames(dir1, dir2, filelist)
  #print mylist
  getAllMoveUtt(mylist)
