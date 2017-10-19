#!/usr/bin/python

import sys, fileinput, os


def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " outfile directory\n"
    sys.exit(1)

def ReadFromDir(): 
  for pattern in sys.argv[2:]: 
    listing = os.listdir(pattern)
  #print listing
  return listing 

def stripfile(listing):
  mylist = []
  for fname in listing:
    newname = fname.rstrip("moves.xml")
    mylist.append(newname)
  return mylist


if __name__ == "__main__":
  usage(sys.argv)
  listing = ReadFromDir()
  mylist = stripfile(listing)
  outfile = sys.argv[1]
  mylist.sort()
  with open(outfile,'w') as f: 
    for item in mylist:
      f.write(str(item) + "\n")
