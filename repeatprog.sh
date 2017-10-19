#!/bin/bash

#To repeat program acting on files from a single directory. 


#$1 program name


for i in *; do
	echo "Running "$1 " on "$i
	$1 $i 
done
