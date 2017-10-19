#!/usr/bin/python

import os, sys, fileinput, glob
'''
To work with the .csv files
part1: to extract the utterances from the csv
Then use encodeToHash.py to prepare for openHTMM
When openHTMM has been used, then use part2 to assign topics. 
part2: to assign topics to the csv
part3: to calculate transition matrices from the CSV files that have had topics assigned
part4: to calculate observation matrices from the CSV files that have topics assigned 
'''

def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " TopicModel CSVdirectory \n"
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

def extractAllUtts(infile,outfile):
  with open(infile, 'r') as f:
    with open(outfile,'w') as fout:
      for line in f:
        #print extractUtt(line)
        fout.write(str(extractUtt(line)+ " "))
'''
def extractDirUtts(directory):
  outlist = ReadFromDir(directory)
  for myFile in outlist:
    infile = myFile
    outfile = myFile+".utts"
    extractAllUtts(infile,outfile)
'''  

#transfer topic model into a set of dictionaries. Combine with removeEmptyDicts
def getTopics(topicfile):
  f = open(topicfile,'r')
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

'''
getTopics and removeEmptyDicts should be used in conjunction for robustness
'''


#Calculate the probabilities of the line occurring in each dictionary
def prodUtterance(dictionary, line):
  probability = 1
  #print dictionary
  for word in line.split():
    #print word
    value = dictionary[str(word)]
    #print word +" "+ value
    probability = probability * float(value)
  return probability

def removeRepeats(line):
  editedutterance = ''
  for word in line.split():
    #print word
    if word not in editedutterance:
      editedutterance = editedutterance + ' ' + word
      #print word
      #print editedutterance
  return editedutterance

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

#for a given line and set of dictionaries, return the topic for that line
def utteranceTopic(listofDicts, line): 
  inlist = topicDist(listofDicts,line)
  topic = greatestValue(inlist)
  #print line
  return topic

if __name__ == "__main__":
  usage(sys.argv)
  #infile = sys.argv[1]
  #outfile=sys.argv[1]+'.out'
  #extractAllUtts(infile,outfile)
  TopicModel = sys.argv[1]
  directory = sys.argv[2]
  
  infiles = ReadFromDir(directory)
  dictTopics = getTopics(TopicModel) #a list of dictionaries
  propTopics = removeEmptyDicts(dictTopics)
  #for i, key in propTopics[0].iteritems():
  #  print i, key

  for i in infiles: 
    outname = i + ".classed"
    f = open(i,'r')
    out = open(outname,'w')
    for line in f:
      #out.write(str(utteranceTopic(propTopics,line)) +'\n' )
      #print line
      #if not line:
      myline = extractUtt(line)
      split = splitUtt(line)
      #print myline
      out.write(str( split[0]+";"+ split[1]+";"+ myline+";"+ str(utteranceTopic(propTopics,myline))+ "\n"))
      #print line, utteranceTopic(propTopics,line), i
    f.close()
    #out.close()


