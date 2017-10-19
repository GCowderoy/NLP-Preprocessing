#!/usr/bin/python

from optparse import OptionParser
import re
import os, sys 

def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " wordlist directory \n"
    sys.exit(1)

def ReadFromDir(directory): 
  #for pattern in directory: 
  listing = []
  for fname in os.listdir(directory):
    path = os.path.join(directory, fname)
    if os.path.isdir(path):
      continue
    listing.append(path)
  return listing

# Returns the contents of a file as a string
def load_file_contents(fname):
  # Open the file, read the contents and close the file
  f = open(fname, "r")        
  fcontents = f.read()
  f.close()
  return fcontents

# Loads a file containing the words to be found in each
# document. Returns a list of words.
def load_word_list(fname):
  # Load the file
  tmp = load_file_contents(fname)
  # Split the contents of the file on a newline
  # and return the result as an array
  #print [x for x in tmp.split("\n") if x]
  return [x for x in tmp.split("\n") if x]

def extractUtt(moveline):
  c=moveline.split(",")
  #print c
  move = c[0]
  time1 = c[1]
  time2 = c[2]
  utterance = c[3]
  t= utterance.rstrip()
  return t.strip()

def splitUtt(moveline):
  c=moveline.split(",")
  return c


def replaceText(tempfilepath, landmarks, outfilepath): 
  tempfile = open(tempfilepath, 'r')
  with open(outfilepath, 'w') as outfile:
    for line in tempfile:
      myline = extractUtt(line)
      c = splitUtt(line)
      outfile.write(str(c[0]) +","+ str(c[1]) +","+ str(c[2])+ ", ")
      for word in myline.split():
        #print word
        if word in landmarks: 
          #print str(word +" ")
          outfile.write(str("[landmark] "))
        else:
          outfile.write(str(word)+ " ")
      #print "\n"
      outfile.write("\n")
  outfile.close()


if __name__== "__main__":
  usage(sys.argv)
  #inputdir = sys.argv[1]
  #incontents = load_file_contents(inputfile)

  wordlist = sys.argv[1]
  directory = sys.argv[2]
  files = ReadFromDir(directory)
  mylist = load_word_list(wordlist)
  for i in files: 
    outfile = i + ".LM"
    replaceText(i, wordlist, outfile)



