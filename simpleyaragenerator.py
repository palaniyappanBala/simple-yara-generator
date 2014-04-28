#!/usr/bin/python

#To reduce false positive
#TODO: "and not" commonCleanString (>90) not in badTotal

#To reduce false positive
#TODO: offset for bad strings

#To reduce false negative
#TODO: "or" with minimal group search in bad, if no intersection

import os
import sys
from subprocess import Popen, PIPE

fullStringList = []
badTotal = []
cleanTotal = []

badStringList = []
nbBadFile = 0
for file in os.listdir("./BAD/"):
	#tmpArray = Popen(['./ngram', "./BAD/"+file], stdout=PIPE).stdout.read().split("\n")
	tmpArray = Popen(['strings', "./BAD/"+file], stdout=PIPE).stdout.read().split("\n")
	tmpArray = list(set(tmpArray))
	badStringList.append(tmpArray);
	fullStringList.append(tmpArray);
	badTotal += tmpArray
	nbBadFile = nbBadFile+1
	
cleanStringList = []
nbCleanFile = 0
for file in os.listdir("./CLEAN/"):
	#tmpArray = Popen(['./ngram', "./CLEAN/"+file], stdout=PIPE).stdout.read().split("\n")
	tmpArray = Popen(['strings', "./CLEAN/"+file], stdout=PIPE).stdout.read().split("\n")
	tmpArray = list(set(tmpArray))
	cleanStringList.append(tmpArray);
	fullStringList.append(tmpArray);
	cleanTotal += tmpArray
	nbCleanFile = nbCleanFile+1

badCleanIntersec = reduce(set.intersection,map(set,fullStringList))
badIntersec = reduce(set.intersection,map(set,badStringList))
cleanIntersec = reduce(set.intersection,map(set,cleanStringList))

#List of common clean string
commonCleanString = []
for cleanString in cleanTotal:
	if cleanString not in commonCleanString:
		tmpCount = cleanTotal.count(cleanString)
		if tmpCount > int(nbCleanFile*0.40):
			commonCleanString.append(cleanString)
commonCleanString = set(commonCleanString)
onlyBadIntersec = badIntersec - commonCleanString
#onlyBadIntersec = badIntersec - cleanIntersec

#Create Yara Signature
print "rule AUTO_TEST{"
print "\tmeta:"
print "\t\tdescription=\"Auto\""
print ""
print "\tstrings:"
i = 0
for term in onlyBadIntersec:
	if term:
		print "\t\t$s"+str(i)+"=\""+term+"\"";
	i=i+1

print ""
print "\tcondition:"
for j in range(0,i):
	print "$s"+str(j)
	if j < i-1:
		print "\t\tand ",
print "}"

