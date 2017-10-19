#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " anvil_file\n"
    sys.exit(1)

def extractMoveLabel( tree , outfile ):
  #open outputfile
  f=open(outfile, 'w')
  # search in the anvil file for the body
  root = tree.getroot()
  for child in root: 
    if child.tag == 'move':
      for c in child.attrib:
        if c =='label':
          f.write(str(child.attrib[c]))
          f.write('\n')
  f.close()


if __name__ == "__main__":
  usage(sys.argv)
  tree = ET.parse(sys.argv[1])

  outfile=sys.argv[1]+".out"
  extractMoveLabel(tree, outfile)
  
