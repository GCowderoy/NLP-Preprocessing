#!/usr/bin/python

import sys

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " file\n"
    sys.exit(1)

def removeLineBreaks(infile, outfile):
  inf = open(infile, 'r')
  mylist = []
  with open(outfile,'w') as outf: 
    for line in inf:
      aline = line[0]        
      if aline == "<":
        if len(mylist) > 0:
          #print mylist
          newlist =[]
          for item in mylist: 
            c=item.rstrip()
            newlist.append(c)
          out = " ".join(newlist)
          outf.write(str(out+"\n"))
        mylist = []
        outf.write(str(line))
      else:
        #print line
        mylist.append(line)
  inf.close()
  outf.close()

if __name__ == "__main__":
  usage(sys.argv)
  inputfile = sys.argv[1]
  outputfile = sys.argv[1]+".lines"
  removeLineBreaks(inputfile, outputfile)
