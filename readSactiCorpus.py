#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " anvil_file\n"
    sys.exit(1)

def extractActorTranscriptions( tree, actorType , outfile ):
  #open outputfile
  f=open(outfile, 'w')
  # search in the anvil file for the body
  root = tree.getroot()
  for child in root:
    # when we have found the body, interrogate it
    if child.tag == "body":
      # read each element one at a time
      for elements in child.iter('el'):
        # assume no transcription found yet
        transcriptionFound = False
        # examine each element looking for a transcription associated with WIZARD_TYPE
        for attribute in elements.iter('attribute'):
          if ( attribute.attrib['name'] == 'type' ):
            if ( attribute.text == actorType ):
              transcriptionFound = True
  
        if transcriptionFound == True:
          # examine each element looking for a transcription associated with WIZARD_TYPE
          for attribute in elements.iter('attribute'):
            if ( attribute.attrib['name'] == 'transcription' ):
              f.write( attribute.text)
              f.write('\n')
              #print attribute.text
  f.close()
  return f

def orderedActorTranscriptions( tree, outfile ):
  f=open(outfile, 'w')
  # search in the anvil file for the body
  root = tree.getroot()
  for child in root:
    # when we have found the body, interrogate it
    if child.tag == "body":
      # read each element one at a time
      for elements in child.iter('el'):
        # assume no transcription found yet
        transcriptionFound = False
        # examine each element looking for a transcription associated with WIZARD_TYPE
        for attribute in elements.iter('attribute'):
          if ( attribute.attrib['name'] == 'type' ):
            if ( attribute.text == 'WIZARD_TALKING' ) or ( attribute.text == 'TYPIST_TYPING' ):
              transcriptionFound = True
  
        if transcriptionFound == True:
          # examine each element looking for a transcription associated with WIZARD_TYPE
          for attribute in elements.iter('attribute'):
            if ( attribute.attrib['name'] == 'transcription' ):
              #print attribute.text
              f.write(attribute.text)
              f.write('\n')
  f.close()
              

def WriteToFile(output,outfile):
  f=open(outfile,'w')
  f.write(outfile)
  f.close

if __name__ == "__main__":
  usage(sys.argv)
  tree = ET.parse(sys.argv[1])
  outfile=sys.argv[1]+".out"
  #print outfile

  #extractActorTranscriptions( tree, 'WIZARD_TALKING' , outfile )
  #extractActorTranscriptions( tree, 'TYPIST_TYPING', outfile )

  orderedActorTranscriptions(tree , outfile )
  
