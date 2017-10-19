#!/usr/bin/python

import nltk
import os, sys, fileinput

##Probably should edit this for efficiency.  
#To apply to a different corpus of dialogues, just change the paths.  
#path='/home/grace/Downloads/SACTI_corpora/SACTI-1/SACTI-1-ANVIL/dialogues_edited'
#newpath='/home/grace/Downloads/SACTI_corpora/SACTI-1/SACTI-1-ANVIL/NumberedTranscripts/'
#tmppath='/home/grace/Downloads/SACTI_corpora/SACTI-1/SACTI-1-ANVIL/OutDialogues/tmp'

listing=os.listdir(path)
TotalVocab={}
id = 0
#print listing
for infile in listing: 
    print infile
    myfile=os.path.join(path,infile)
    outfile = infile + ".proc"
    fname=os.path.join(newpath,outfile)
    f=open(myfile,'r')
    fout = open(fname,'w')
    for line in f:
        #A count of the number of words in the line
        wordcountLine = 0
        for word in line.split():
            wordcountLine = wordcountLine +1
        fout.write(str(wordcountLine) + " ")
	#Writing the number in. 
        for word in line.split():
            if word not in TotalVocab.keys(): 
                #print word
                id = id+1
                TotalVocab[word] = id
            wordKey = TotalVocab[word]
            fout.write(str(wordKey) + " ")
        fout.write("\n")
    fout.close()
    #ftmp.close()
    print len(TotalVocab)

#for value in range(1,10):
    #for key, value in TotalVocab.iteritems():
        #print key, value
#print TotalVocab
print len(TotalVocab)
VocabName=os.path.join(newpath,"Vocab.out")
Vocabulary=open(VocabName,'w')
for key, value in TotalVocab.iteritems():
    Vocabulary.write(str(value)+" " + str(key))
    Vocabulary.write("\n")
Vocabulary.close()

            
