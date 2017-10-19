#!/usr/bin/python

import sys, fileinput, os


def usage(argv):
  if len(argv) != 3:
    print "Error: \n    Usage: " + argv[0] + " filelist directory\n"
    sys.exit(1)


def ReadFromDir(): 
  for pattern in sys.argv[2:]: 
    listing = os.listdir(pattern)
  listing.sort()
  return listing 

def matchfnames(dirlist, flist): 
  mylist = []
  with open(flist,'r') as f:
    #is reading f as a single line. 
    myfile = f.read()
    for element in myfile.split("[]"): 
      #c= element[3]
      print str(element) + "\n"
      for item in dirlist:
        #print element, item
        if item.find(str(element)) != -1:
          #print element, item
          fname = item
          tup = element, item
          mylist.append(tup)
  return mylist


#take output from fileAligning.py

if __name__ == "__main__":
  usage(sys.argv)
  listing = ReadFromDir()
  #for item in listing:
  #  print item
  filelist = sys.argv[1]
  #print filelist
  c = matchfnames(listing,filelist)
  #print c
