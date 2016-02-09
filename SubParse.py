#!/usr/bin/env python

# Subtitle file parser class by ne0d34th
# currently only support srt 
# feel free to copy as long credit is given, it's a crap anyway

class SubParse(object):
	__file = None
	__subtitle = []

	IN_SECONDS = 1

	def __init__(self, file):
		self.__file = open(file, "r")
		lines = []
		for line in self.__file:
			lines.append(line)
		count = 0
		unfinished = True
		while(unfinished):
			number = int(lines[count])
			count+=1
			interval = lines[count]
			intervalFrom = interval.split(" --> ")[0]
			intervalTo = interval.split(" --> ")[1].split("\n")[0]
			count+=1
			text = ""
			text += lines[count].split("\n")[0]
			while(lines[count+1]!="\n"):
				count+=1
				text += "\n"+lines[count].split("\n")[0]
				if(count+1>=len(lines)):
					break
			count+=2
			subLine = (number, intervalFrom, intervalTo, text)
			self.__subtitle.append(subLine)
			if(count>=len(lines)):
				unfinished=False

	def convertTime(self, type):
		if(type==1):
			for x in xrange(0, len(self.__subtitle)):
				number = self.__subtitle[x][0]
				intervalFrom = self.__subtitle[x][1]
				intervalTo = self.__subtitle[x][2]
				text = self.__subtitle[x][3]
				intervalFromSplit = intervalFrom.split(":")
				fromHours = int(intervalFromSplit[0])
				fromMinutes = int(intervalFromSplit[1])
				fromSeconds = float(intervalFromSplit[2].replace(",","."))
				fromSeconds += float(fromHours*3600)
				fromSeconds += float(fromMinutes*60)
				intervalToSplit = intervalTo.split(":")
				toHours = int(intervalToSplit[0])
				toMinutes = int(intervalToSplit[1])
				toSeconds = float(intervalToSplit[2].replace(",","."))
				toSeconds += float(toHours*3600)
				toSeconds += float(toMinutes*60)
				subLine = (number, fromSeconds, toSeconds, text)
				self.__subtitle.pop(x)
				self.__subtitle.insert(x, subLine)

	def getSubtitle(self):
		return self.__subtitle
