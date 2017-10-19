#!/bin/bash

#To repeat program acting on files from a single directory. 


#$1 program name


for f in *; do
	grep . "$f" > "$f.tmp"
done
