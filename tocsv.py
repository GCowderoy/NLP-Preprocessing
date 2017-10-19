#!/usr/bin/python

import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		exit(0)

	out = open('out.csv', 'w+')

	with open(sys.argv[1]) as ifile:
		text = ifile.read()
		topics = text.split('\n\n')		
		for topic in topics:
			topic_elements = topic.strip().split('\n')
			print(topic_elements[0])
			out.write("{0}\n".format(topic_elements[0]))
			for element in topic_elements[2:]:
				item = element.strip().split('\t')
				out.write("{0},{1}\n".format(item[0], item[1]))

	out.close()
