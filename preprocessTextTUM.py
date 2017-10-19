#!/usr/bin/python

import re
import string
import nltk
import string
import sys
 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
 
def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " inputfile\n"
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



#this is the main function from John, but removes all line breaks
def ProcessText(inputfilepath,outfilepath):
  infile = open(inputfilepath, 'r')
  with open(outfilepath, 'w') as outfile:
    for line in infile:
      myline = extractUtt(line)
      c = splitUtt(line)
      myutt = ""

      #convert all the text in the file to unicode
      #(this attempts to remove strange characters)
      text = unicode(myline,errors='ignore')
      #remove punctuation symbols from the file
      exclude = set(string.punctuation)
      table = {ord(c): unicode(" ") for c in exclude}
      no_punctuation = text.translate(table)
      #convert all the text to lowercase
      no_punctuation = no_punctuation.lower()
      #split the text up into tokens
      tokens = word_tokenize(str(no_punctuation))
      #remove the stopwords - this doesn't work on maptask. remove the commented out code to make this work. 
      #stopset = stopwords.words('english')
      #no_stopwords = [w for w in tokens if not w in stopset]
      #remove the numbers
      #no_digits = [w for w in no_stopwords if not str(w).isdigit()]
      no_digits = [w for w in tokens if not str(w).isdigit()]
      #out to normalised text to the output file
      for w in no_digits:
        myutt = myutt + w +  " " 
        #outfile.write(str(w + " "))
      #print str(c[0]) +","+ str(c[1]) +","+ str(c[2])+ ", " + myutt
      outfile.write(str(c[0]) +","+ str(c[1]) +","+ str(c[2])+ ", " + myutt+ "\n")
  infile.close()
  #print no_digits
  #return no_digits
#outfile.close()


def editText(inputfilepath, tempfilepath):
  infile = open(inputfilepath, 'r')
  with open(tempfilepath,'w') as tempfile: 
    text = unicode(infile.read(),errors='ignore')
    exclude = set(string.punctuation)
    table = {ord(c): unicode(" ") for c in exclude}
    no_punctuation = text.translate(table)
    no_punctuation = no_punctuation.lower()
    #print no_punctuation
    tempfile.write(no_punctuation)
    infile.close()
  tempfile.close()
  return no_punctuation

def replaceText(tempfilepath, no_digits, outfilepath): 
  tempfile = open(tempfilepath, 'r')
  with open(outfilepath, 'w') as outfile:
    for line in tempfile:
      #myline = extractUtt(line)
      for word in line.split():
        #print word
        if word in no_digits: 
          #print str(word +" ")
          outfile.write(str(word + " "))
      #print "\n"
      outfile.write("\n")
  outfile.close()

if __name__ == "__main__":
  usage(sys.argv)
  inputfilepath = sys.argv[1]
  outfilepath = sys.argv[1]+".proc"
  #tempfilepath = sys.argv[1]+".tmp"
  noDigits = ProcessText(inputfilepath,outfilepath)
  #editText(inputfilepath, tempfilepath)
  #replaceText(tempfilepath, noDigits, outfilepath)

