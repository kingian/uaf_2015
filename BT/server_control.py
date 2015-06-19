import traceback
import sys
import subprocess
import time
import commands
import json
import glob
import socket
from enum import *

conStates = Enum(['active','paused','compressed','sent'])

class ServerControl:
		
	
	def __init__(self):
		self.conStates = Enum(['active','paused','compressed','sent'])
		self.controllerList = []
		self.transferFlag = False
		self.compressFlag = False
		self.registerFlag = False
		self.startFlag = False
		self.stopFlag = False
		self.transferInterator = 0

# Response parser
	def parseResponse(self, response):
		cmdStr = ""
		msgerrStr = ""
		commandList = []
		# Strip off the message/error if it's there
		try:
			tmp = response.split('##')
			cmdStr = tmp[0]
			msgerrStr = tmp[1]
		except:
			cmdStr = response

		
		# Split response into the commandList
		try:
			commandList = cmdStr.split(':')
			
		except:
			print ('Error splitting to commandList' +
				   traceback.format_exc())
			
		if (msgerrStr!=''):
			commandList.append(msgerrStr)
		
		return commandList
	
	
	
	def issueCommand(self, com):
		print com
		return com
	

	def sequenceTransfer(self):
		if(self.transferInterator < len(self.controllerList)):
			self.issueCommand('pi' + str(self.transferInterator) + ':send')
			self.transferInterator += 1
		else:
			self.transferInterator = 0
			self.transferFlag = False
			print ('All controllers have trasfered their tarballs.')
	
	
	def camConResponse(self, response):
		
		self.evalComList(self.parseResponse(response))
		
		if((self.stopFlag) and (self.checkConListState(conStates.paused))):
			self.stopFlag = False
			self.compressFlag = True
			self.issueCommand('comp')
			print ('All controllers stopped, starting compression.')
		elif((self.compressFlag) and (self.checkConListState(conStates.compressed))):
			self.compressFlag = False
			self.transferFlag = True
			self.sequenceTransfer()
			print ('All controllers have completed compressing their folders.')
		elif(self.transferFlag):
			self.sequenceTransfer()
		elif((self.startFlag) and (self.checkConListState(conStates.active))):
			self.startFlag = False
			
				
		
	
	def evalComList(self, cl):
		try:
			if(cl[1] == 'register'):
				self.camConRegister(cl)
			elif(cl[1] == 'paused'):
				self.camConPaused(cl)
			elif(cl[1] == 'started'):
				self.camConStarted(cl)
			elif(cl[1] == 'compressed'):
				self.camConCompressed(cl)
			elif(cl[1] == 'sent'):
				self.camConPaused(cl)
			else:
				print "Something's wonky with this: " + ', '.join(cl)
		except:
			print "Command evaluation failed!! Most likely the list was empty." + ', '.join(cl)
	
	
# Takes a CamConPointer and adds it to the list
	def camConRegister(self, comlist):
		if(self.getConPtr(comlist[0])==None):
			self.controllerList.append(CamConPointer(comlist[0]))

	
# Finds a CamConPointer by name
	def getConPtr(self, name):
		for ptr in self.controllerList:
			if (ptr.conName == name):
				return ptr
			
# Checks to see if all CamConPointers are in the same state	
	def checkConListState(self, stateToCheck):
		for ptr in self.controllerList:
			if (ptr.state != stateToCheck):
				return False
		return True
			
# Updates CamConPointer state to sent	
	def camConSent(self, cl):
		try:
			self.getConPtr(cl[0]).state = conStates.sent
		except:
			print(traceback.format_exc())

	
# Updates CamConPointer state to active		
	def camConStarted(self, cl):
		try:
			self.getConPtr(cl[0]).state = conStates.active
		except:
			print(traceback.format_exc())


# Updates CamConPointer state to paused		
	def camConPaused(self, cl):
		try:
			self.getConPtr(cl[0]).state = conStates.paused
		except:
			print(traceback.format_exc())
			

# Updates CamConPointer state to compressed	
	def camConCompressed(self, cl):
		try:
				self.getConPtr(cl[0]).state = conStates.compressed
		except:
			print(traceback.format_exc())

	
	
	def listControllers(self):
		print len(self.controllerList)
		for ptr in self.controllerList:
			print ptr.ToString()
	
	

	
class CamConPointer():
	
	def __init__(self,inName):
		self.state = conStates.active
		self.conName = inName

	
	def ToString(self):
		return self.conName + ' ' + self.state