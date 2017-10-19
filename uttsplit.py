#!/usr/bin/python

import os, sys, fileinput

def usage(argv):
  if len(argv) != 2:
    print "Error: \n    Usage: " + argv[0] + " TUMfile \n"
    sys.exit(1)


def extractUtt(moveline):
  c=moveline.split(",")
  move = c[0]
  time1 = c[1]
  time2 = c[2]
  utterance = c[3]
  t= utterance.rstrip()
  return t.strip()

def splitUtt(moveline):
  c=moveline.split(",")
  return c


if __name__== "__main__":
  usage(sys.argv)
  infile = sys.argv[1]
  with open(infile, 'r') as f: 
    for line in f:
      utt= splitUtt(line)
      #utt.append("3")
      print utt
      print line.rstrip() #+ " ser"
