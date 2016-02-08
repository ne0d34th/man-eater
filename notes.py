#!/usr/bin/env python27

# Schedule / To-do list / Notes / whatevs~ System
# by ne0d34th
#
# feel free to copy as long credit is given, it's a crap anyway

import sqlite3
import sys
import os
import time

def clearscreen():
	os.system('cls' if os.name == 'nt' else 'clear')
	return

connection = sqlite3.connect("data")
cursor = connection.cursor()

color = "\033[31m"
resetColor = "\033[0m"
title = "Here's your to do list, "+color+"onee-sama"+resetColor+"~"

def printSchedule(schedule):
	print ""
	print "\t%s%-40s%s %-20s" % (color,schedule[0],resetColor, schedule[1])
	return

cursor.execute("select count(*) from sqlite_master where type='table' and name='schedule'")
tableExists = cursor.fetchone()[0]

if(tableExists==0):
	cursor.execute("create table schedule ( \
					title varchar(100), \
					progress varchar(50) \
					)")

if(len(sys.argv)==1):
	clearscreen()
	cursor.execute("select count(*) from sqlite_master where type='table' and name='time'")
	tableExists = cursor.fetchone()[0]
	if(tableExists>0):
		cursor.execute("drop table time")
		connection.commit()

	cursor.execute("create table time ( \
					timeTab datetime \
					)")
	cursor.execute("select count(*) from time")
	first = cursor.fetchone()
	cursor.execute("select * from schedule")
	scheduleList = cursor.fetchall()
	print title
	for schedule in scheduleList:
		printSchedule(schedule)
	while(True):
		try:
			cursor.execute("select count(*) from time")
			current = cursor.fetchone()
			if(current!=first):
				clearscreen()
				cursor.execute("select * from schedule")
				scheduleList = cursor.fetchall()
				print title
				for schedule in scheduleList:
					printSchedule(schedule)
				first=current
			time.sleep(1)
		except KeyboardInterrupt:
			sys.exit(0)

else:
	if(sys.argv[1]=="-n"):
		if(len(sys.argv)!=4):
			print "Error: Incorrect arguments!"
		else:
			insertTup = (sys.argv[2], sys.argv[3])
			cursor.execute("insert into schedule (title, progress) values (?,?)", insertTup)
			connection.commit()
			cursor.execute("insert into time values (datetime())")
			connection.commit()
	elif(sys.argv[1]=="-f"):
		inputs = raw_input("Are you sure to flush all schedule? [y/N]: ")
		if(inputs=="y" or inputs=="Y"):
			cursor.execute("drop table schedule")
			connection.commit()
	elif(sys.argv[1]=="-d"):
		if(len(sys.argv)==2):
			cursor.execute("select rowid, title, progress from schedule")
			scheduleList = cursor.fetchall()
			for schedule in scheduleList:
				print "[%d] - %-40s %-20s" % (schedule[0], schedule[1], schedule[2])
		else:
			id = sys.argv[2]
			try:
				id = int(id)
			except:
				print "Error: Incorrect arguments! id must in integer!"
				sys.exit(0)
			else:
				selectTup = (id,)
				cursor.execute("select * from schedule where rowid=?", selectTup)
				idCheck = cursor.fetchone()
				if not idCheck:
					print "Error: Index out of bound!"
					sys.exit(0)
				inputs = raw_input("Are you sure to delete schedule with id="+str(id)+"? [y/N]: ")
				if(inputs=="y" or inputs=="Y"):
					cursor.execute("delete from schedule where rowid=?",selectTup)
					connection.commit()
					cursor.execute("insert into time values (datetime())")
					connection.commit()
	elif(sys.argv[1]=="-e"):
		if(len(sys.argv)==2):
			cursor.execute("select rowid, title, progress from schedule")
			scheduleList = cursor.fetchall()
			for schedule in scheduleList:
				print "[%d] - %-40s %-20s" % (schedule[0], schedule[1], schedule[2])
		else:
			id = sys.argv[2]
			try:
				id = int(id)
			except:
				print "Error: Incorrect arguments! id must in integer!"
				sys.exit(0)
			else:
				if(len(sys.argv)!=4):
					print "Error: Incorrect arguments!"
					sys.exit(0)
				editProgress = sys.argv[3]
				updateTup = (editProgress, id)
				cursor.execute("update schedule set progress=? where rowid=?", updateTup)
				connection.commit()
				cursor.execute("insert into time values (datetime())")
				connection.commit()
	else:
		print "Schedule - To do List - Notes System by ne0d34th"
		print ""
		print "Usage: "
		print "\t"+sys.argv[0]
		print "\tLive feed of your lists or notes"
		print "\n\t"+sys.argv[0]+" -n <title> <other description / progress>"
		print "\tAdd new notes, title and other description must be included"
		print "\n\t"+sys.argv[0]+" -d"
		print "\tPrint all notes with it's index"
		print "\n\t"+sys.argv[0]+" -d <id>"
		print "\tDelete a notes with index <id>"
		print "\n\t"+sys.argv[0]+" -e <id> <description>"
		print "\tEdit description for a note with index <id> with <description>"
		print "\n\t"+sys.argv[0]+" -f"
		print "\tFlush all your notes (reset everything)"
		print "\n\t"+sys.argv[0]+" --help OR -h"
		print "\tPrint this help"
		print ""
