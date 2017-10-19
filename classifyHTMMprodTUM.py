#!/usr/bin/python

import os, sys, fileinput, glob

def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " TopicModel directory \n"
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

def ReadFromDirec(): 
  for pattern in sys.argv[2:]: 
    listing = os.listdir(pattern)
  #print listing
  return listing.sort()

def ListFullPath():
  listing = ReadFromDirec()
  PathList = []
  for item in listing: 
    fullpath = os.path.join(str(sys.argv[2]), item)
    PathList.append(fullpath)
  return PathList

#read TopicModel file
def load_file_contents(fname):
  # Open the file, read the contents and close the file
  f = open(fname, 'r')        
  fcontents = f.read()
  f.close()
  #print fcontents
  return fcontents

def getTopics(infile):
  f = open(infile,'r')
  text = f.read()
  topics = text.split('\n\n')
  mylist=[]
  for topic in topics:
    mydict = {}
    topic_elements = topic.strip().split('\n')
    for element in topic_elements[2:]:
      item = element.strip().split('\t')
      word =item[0]
      key = item[1]
      mydict[word] = key
    #print mydict
    mylist.append(mydict)
  #print mylist
  return mylist

def removeEmptyDicts(listofDicts):
  mylist = listofDicts
  for i, j in enumerate(listofDicts):
    dictionary = listofDicts[i]
    if len(dictionary) == 0 :
      mylist.remove(dictionary)
  return mylist


def extractUtt(moveline):
  c=moveline.split(",")
  move = c[0]
  time1 = c[1]
  time2 = c[2]
  utterance = c[3]
  t= utterance.rstrip()
  return t.strip()


def splitUtt(moveline):
  c=moveline.split(",")
  return c

#Difference is here
def removeRepeats(line):
  editedutterance = ''
  for word in line.split():
    #print word
    if word not in editedutterance:
      editedutterance = editedutterance + ' ' + word
      #print word
      #print editedutterance
  return editedutterance

#difference is here
def prodUtterance(dictionary, line):
  probability = 1
  #print dictionary
  #print line
  #some error in the looping
  for word in line.split():
    #print word
    if word not in dictionary: 
      continue
    else:
      value = dictionary[str(word)]
      #print word +" "+ value
      probability = probability * float(value)
  #print probability
  #print line
  return probability

#Gives a vector of probabilities for one line
#Need to give it a list of dictionaries - as in topicset [{}, {}, ...,{}]
def topicDist(listofDicts,line):
  dist = []
  for i, v in enumerate(listofDicts):
    dictionary = listofDicts[i]
    utterance=removeRepeats(line)
    probability = prodUtterance(dictionary, utterance)
    dist.append(probability)
  #print dist
  #print line +' '
  return dist

#gives a normalised list
def calcNorm(dist):
  mydist=[]
  value = 0
  for i in dist:
    value = value + dist[i]
  normconst = value
  for i in dist:
    mydist[i] = dist[i] / normconst
  return mydist
  
  

#gives the position
def greatestValue(inputlist):
  c=0
  #print inputlist
  for i in range(len(inputlist)):
    if inputlist[i] > c:
      c = inputlist[i]
  #print inputlist.index(c)
  return inputlist.index(c)

#for a given line and set of dictionaries, return the topic for that line
def utteranceTopic(listofDicts, line): 
  inlist = topicDist(listofDicts,line)
  topic = greatestValue(inlist)
  #print line
  return topic


if __name__ == "__main__":
  usage(sys.argv)
  topicmodel = sys.argv[1]
  directory=sys.argv[2]
  listing=ReadFromDir(directory)
  dictTopics = getTopics(topicmodel)
  propTopics=removeEmptyDicts(dictTopics)

  #print topicmodel
  #print listing
  #print propTopics
  for i in listing:
    outname = i+'.topics'
    f = open(i,'r')
    #print i
    out = open(outname,'w')
    for line in f:
      myline = extractUtt(line)
      #print myline
      c = splitUtt(line)
      mytop = utteranceTopic(propTopics,myline)
      #print str(c[0]) +","+ str(c[1]) +","+ str(c[2])+ ", " + myline +" , "  + str(mytop)
      out.write(str(c[0]) +","+ str(c[1]) +","+ str(c[2])+ ", " + myline +" , "  + str(mytop) +"\n")
      #out.write(line)
      #out.write(str(utteranceTopic(propTopics,myline)) +'\n' )
      #print line
      #c = topicDist(propTopics,line)
      #print c,greatestValue(c),'\n\n'
    f.close()
    #out.close()'''

#blerch
