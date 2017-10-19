#!/usr/bin/python

import sys

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " TopicModel \n"
    sys.exit(1)

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
  print mylist
  return mylist

def getTheTopics(fname):
  f = open(fname,'r')
  #print f
  topicset=[]
  initdict={}
  count = 0
  for line in f:
    #print line
    #edit the if statement
    if (line.find('\t') == True):
      print line #Error here
      loc=line.find('\t')
      word = line[:loc]
      key=line[loc:]
      initdict[word] = key
      print initdict
    elif (line.find("---------") == True): 
      print line 
      topicset.append(count)
      count = count +1    

    else:
      if len(initdict) != 0: #check dictionary non-empty, then append to list
        topicset.append(initdict)    
        initdict = {} 
  print topicset
  f.close()
  return topicset


if __name__ == "__main__":
  usage(sys.argv)
  infile = sys.argv[1]
  getTopics(infile)
