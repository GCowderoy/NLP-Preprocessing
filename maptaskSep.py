#!/usr/bin/python

import sys

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " anvil_file\n"
    sys.exit(1)

def maptaskSep(infile, outfwr, outguide):
  inf = open(infile, 'r')
  tmpfilename =infile+".tmp"
  outfile = open(tmpfilename,'w')
  with open(outfwr,'w') as outfollower:
    with open(outguide, 'w') as outguide: 
      for line in inf:
        aline = line[0]        
        if aline == "<":
          if line.find("who=") == False:
            print line
          else: 
            j=line.find("who=") + 4
            if line[j] =='F':
              outfile = outfollower
            elif line[j] =='G':
              outfile=outguide
        else:
          for word in line.split(): 
            #if word == "\n":
            #  outfile.write(" ")
            #else:
            outfile.write(word + " ")
        outfile.write("\n")
  outguide.close()
  outfollower.close()
  inf.close()


if __name__ == "__main__":
  usage(sys.argv)
  inputfile = sys.argv[1]
  outfilefollower=sys.argv[1]+".follower"
  outfileguide =sys.argv[1]+".guide"
  maptaskSep(inputfile, outfilefollower, outfileguide)
