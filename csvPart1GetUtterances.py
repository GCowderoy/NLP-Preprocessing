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


def extractAllUtts(infile,outfile):
  with open(infile, 'r') as f:
    with open(outfile,'w') as fout:
      for line in f:
        #print extractUtt(line)
        fout.write(str(extractUtt(line)+ " \n"))

def extractDirUtts(directory):
  outlist = ReadFromDir(directory)
  for myFile in outlist:
    infile = myFile
    outfile = myFile+".utts"
    extractAllUtts(infile,outfile)
  


if __name__ == "__main__":
  usage(sys.argv)
  #infile = sys.argv[1]
  #outfile=sys.argv[1]+'.out'
  #extractAllUtts(infile,outfile)
  
  directory = sys.argv[1]
  extractDirUtts(directory)
