#!/usr/bin/python

import sys, fileinput, os


def usage(argv):
  if len(argv) != 5:
    print "Error: \n    Usage: " + argv[0] + " filelist outfile directory1 directory2\n"
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
              print tup
              mylist.append(tup)
  return mylist



if __name__ == "__main__":
  usage(sys.argv)
  filelist = sys.argv[1]
  directory1 = sys.argv[3]
  directory2= sys.argv[4]
  print directory1, directory2
  #will need to give full path names. 
  listing1 = ReadFromDir(directory1)
  listing2 = ReadFromDir(directory2)

  c = matchfnames(listing1, listing2,filelist)
  outfile = sys.argv[2]
  #print c
  #with open(outfile,'w') as f:
  #  f.write(str(c))
