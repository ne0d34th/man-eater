#!/usr/bin/env python2

class SSAParse(object):
	__file = None
	__styles = []
	__subtitle = []

	__styleFormat = []
	__subFormat = []

	# time format
	IN_SECONDS = 1

	#color format
	HEXADECIMAL = 1
	DECIMAL = 2

	def __init__(self, file):
		with open(file, "r") as self.__file:
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

		self.__styleFormat = listProp

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

		self.__subFormat = listProp

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

	def getSubtitleFormatted(self,*args):
		styleFormat = []
		subFormat = []
		
		for searchFormat in args:
			found = False
			for styleFormatOne in self.__styleFormat:
				if(searchFormat==styleFormatOne):
					styleFormat.append(styleFormatOne)
					found = True
					break

			if(found==True):
				continue

			for subFormatOne in self.__subFormat:
				if(searchFormat==subFormatOne and searchFormat!="Name"):
					subFormat.append(subFormatOne)
					found = True
					break

			if(found==False):
				raise ValueError("Format Name '"+searchFormat+"' not Found!")

		formattedSub = []

		for sub in self.__subtitle:
			subOne = {}
			for subFOne in subFormat:
				subOne[subFOne] = sub[subFOne]
			if(len(styleFormat)!=0):
				styleName = sub["Style"]
				styleIndex = self.__getStyleIndex(styleName)
				for styleOne in styleFormat:
					subOne[styleOne] = self.__styles[styleIndex][styleOne]
			formattedSub.append(subOne)
		return formattedSub

	def convertTime(self, type):
		if(type==self.IN_SECONDS):
			for x in xrange(0, len(self.__subtitle)):
				timeStart = SSAParse.parseTime(self.__subtitle[x]["Start"])
				timeStartNew = float(timeStart["hours"]*3600)+float(timeStart["minutes"]*60)+timeStart["seconds"]
				self.__subtitle[x]["Start"] = timeStartNew

				timeEnd = SSAParse.parseTime(self.__subtitle[x]["End"])
				timeEndNew = float(timeEnd["hours"]*3600)+float(timeEnd["minutes"]*60)+timeEnd["seconds"]
				self.__subtitle[x]["End"] = timeEndNew


	def __getStyleIndex(self, name):
		for x in xrange(0,len(self.__styles)):
			if(self.__styles[x]["Name"]==name):
				return x
		raise ValueError("Style name not found")

	def defineDefaultStyle(self, dict):
		try:
			index = self.__getStyleIndex("Default")
		except ValueError:
			try:
				dict["Name"] = "Default"
				self.__styles.append(dict)
			except:
				raise

	def convertColor(self, type):
		colorProp = ["PrimaryColour", "SecondaryColour", "TertiaryColour", "BackColour"]
		if(type==self.HEXADECIMAL):
			for x in xrange(0, len(self.__styles)):
				for colorOne in colorProp:
					dec = self.__styles[x][colorOne]
					if(dec.find("&H")!=-1):
						continue
					hexa = hex(int(dec))
					result = hexa.split("0x")[1]
					if(len(result)==7):
						result = "0"+result
					while(len(result)<6):
						result = "0"+result
					result = "&H"+result
					self.__styles[x][colorOne] = result
					return
		elif(type==self.DECIMAL):
			for x in xrange(0, len(self.__styles)):
				for colorOne in colorProp:
					dec = self.__styles[x][colorOne]
					if(dec.find("&H")==-1):
						continue
					dec = dec.split("&H")[1]
					if(dec.find("&")!=-1):
						dec = dec.split("&")[0]
					result = int(dec, 16)
					self.__styles[x][colorOne] = result
					return

	@staticmethod
	def parseTime(time):
		try:
			dict = {}
			times = time.split(":")
			dict["hours"] = int(times[0])
			dict["minutes"] = int(times[1])
			dict["seconds"] = float(times[2])
			return dict
		except:
			raise
