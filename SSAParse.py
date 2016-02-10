#!/usr/bin/env python

# SSA Subtitle file parser by ne0d34th
# should be still buggy
# feel free to copy as long credit is given

class SSAParse(object):
	__file = None
	__styles = []
	__subtitle = []

	IN_SECONDS = 1

	def __init__(self, file):
		self.__file = open(file, "r")
		content = self.__file.read()

		style = content.split("[V4 Styles]\n")[1]
		style = style.split("[Events]")[0]

		getFormat = style.split("Format: ")[1]
		styleListRaw = getFormat.split("\n",1)[1]
		getFormat = getFormat.split("\n")[0]

		getFormats = getFormat.split(",")
		listProp = []
		for properties in getFormats:
			listProp.append(properties.strip())

		styleListRawArray = styleListRaw.split("\n")
		for styleOne in styleListRawArray:
			if(styleOne==""):
				break
			styleOne = styleOne.split("Style:")[1]
			styleOneList = styleOne.split(",")
			styleOneDict = {}
			for x in xrange(0, len(styleOneList)):
				styleOneDict[listProp[x]] = styleOneList[x].strip()
			self.__styles.append(styleOneDict)

		subtitlePart = content.split("[Events]\n")[1]

		getFormat = subtitlePart.split("Format: ",1)[1]
		subListRaw = getFormat.split("\n",1)[1]
		getFormat = getFormat.split("\n")[0]

		getFormats = getFormat.split(",")
		listProp = []
		for properties in getFormats:
			listProp.append(properties.strip())

		subListRawArray = subListRaw.split("\n")
		for subOne in subListRawArray:
			if(subOne==""):
				break
			subOne = subOne.split("Dialogue:")[1]
			subOneList = subOne.split(",")
			subOneDict = {}
			for x in xrange(0, len(subOneList)):
				subOneDict[listProp[x]] = subOneList[x].strip()
			self.__subtitle.append(subOneDict)

	def getSubtitle(self):
		return self.__subtitle

	def getStyle(self):
		return self.__styles
