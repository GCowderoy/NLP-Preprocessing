#!/usr/bin/python

import os, sys, fileinput, glob
'''
To run on a preprocessed corpus, before giving to openHTMM
Will produce a Vocabulary.txt, size of vocabulary.
In cmd, use ls directory > listing.txt to produce the training file.
Then, will only need number of topics, alpha, beta, and number of iterations
'''
def usage(argv):
  """Usage statement to ensure you run the script correctly"""
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " directory\n"
    sys.exit(1)

def ReadFromDir(): 
  for pattern in sys.argv[1:]: 
    listing = os.listdir(pattern)
  return listing 

def ListFullPath():
  listing = ReadFromDir()
  PathList = []
  for item in listing: 
    fullpath = os.path.join(str(sys.argv[1]), item)
    PathList.append( fullpath)
  return PathList

def HashTable( PathList ):
  HashTable = {}
  counter = 1
  for item in PathList: 
    f=open(item, 'r')
    foutname = item + ".proc"
    fout = open(foutname, 'w')
    for line in f:
      Count = 0
      for word in line.split():
        Count = Count +1
      fout.write(str(Count) + " ")
      for word in line.split():
        if word not in HashTable.keys():
          HashTable[word] = counter 
          counter = counter +1
        fout.write(str(HashTable[word]) + " ")
      fout.write("\n")
    f.close()
    fout.close() 
  return HashTable

def SaveVocabulary( HashTable ):
  saveVocab = open('Vocabulary.txt', 'w')
  for key, item in HashTable.iteritems(): 
    saveVocab.write(str(item) + " " + str(key))
    saveVocab.write("\n")
  saveVocab.close()
  print len(HashTable)

if __name__ == "__main__":
  usage(sys.argv)
  out =  ListFullPath()
  Vocab = HashTable(out)
  SaveVocabulary(Vocab) 
