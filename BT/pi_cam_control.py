import traceback
import sys
import subprocess
import time
import commands
import json
import glob
import socket
from enum import *

camConStates = Enum(['active','paused','compressed','sent'])


class CamControl:

	cleaner_pid = 0
	motion_pid = 0
	REMOTE_USER = "ubuntu"
	TARGET_PW = "ubuntu"
	HOST = "192.168.1.106"
	REMOTE_PATH = ""
	LOCAL_PATH = ""
	LOCAL_FILE = ""
	MOTION_DIRECTORY = "/tmp/motion"
	HOSTNAME = "default"
	SUCCESS_VALUE = 0


	def __init__(self):
		self.cleaner = None
		pass;

	def getConfig(self,filename):
		try:
			confile = open(filename,'r+')
			configurations = json.load(confile)
			self.LOCAL_PATH = configurations['LOCAL']
			self.REMOTE_PATH = configurations['REMOTE']
			return self.SUCCESS_VALUE
		except:
			return ("An error occured reading the configuration file.\n" + traceback.format_exc())
			
	
	def compressDir(self):
		try:
			self.LOCAL_FILE = str(int(time.time())) + '.tar.gz'
			comp = subprocess.Popen(["tar", "-cvf", self.LOCAL_FILE, "-C", self.MOTION_DIRECTORY, "."])
			comp.wait()
			TARGET = "%s@%s:%s" % (self.REMOTE_USER, self.HOST, self.REMOTE_PATH)
			print ("Images compressed into tarball.")
			return self.SUCCESS_VALUE
		except:
			return ("An error occured compressing the motion folder.\n" + traceback.format_exc()) 

	def cleanImg(self):
		try:
			rm_list = glob.glob('*.tar.gz')
			for n in rm_list:
				subprocess.check_output(['rm', n ])
			return self.SUCCESS_VALUE
		except:
			return ("An exception occured, file cleaning failed.\n" + traceback.format_exc()) 			
	
	def moveImages(self):
		try:

			TARGET = "%s@%s:%s" % (self.REMOTE_USER, self.HOST, self.REMOTE_PATH)
			send = subprocess.Popen(['scp', self.LOCAL_FILE, TARGET])
			send.wait()
			print ("Tarball sent and cleaned")
			self.cleanImg()
#			child = pexpect.spawn(COMMAND)
#			child.expect(pexpect.EOF)
#			print child.before
			return self.SUCCESS_VALUE
		except:
			return ("An error occured compressing the motion folder.\n" + traceback.format_exc())


	def makeDirectories(self):
		try:
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam1"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam2"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam3"])
			return self.SUCCESS_VALUE
		except:
			return ("An error occured making motion directories.\n" + traceback.format_exc())


	
	def startServices(self):
		self.HOSTNAME = socket.gethostname()
		err = self.makeDirectories()
		self.motion_pid
		self.cleaner_pid
		try:
			# cleaner = subprocess.Popen(["./cleaner.sh", "&"])
			self.startCleaner()
			subprocess.call(["sudo", "service","motion", "start"])
			time.sleep(0.05)
			# self.cleaner_pid = cleaner.pid
			self.motion_pid = int(subprocess.check_output(["pgrep","motion"]))
#           DEBUGGING LINES
#			print (subprocess.check_output(["pgrep","motion"]))
#			print ("Motion PID:%d" % self.motion_pid)
#			print ("Cleaner PID:%d" % self.cleaner_pid)
			conState = camConStates.active
			print ("Motion and Cleaner services sucessfully started.\n")
			return [self.motion_pid,self.cleaner_pid]
		except Exception, err:
			return ("An exception occured, Motion and Cleaner didn't start.\n" + traceback.format_exc())

	def startCleaner(self):
		self.cleaner = subprocess.Popen(["./cleaner.sh", "&"])
		self.cleaner_pid = self.cleaner.pid
		return self.SUCCESS_VALUE
		
		
	def pauseServices(self):
		try:
			subprocess.check_output(["sudo","kill","-STOP","%d" % self.motion_pid])
			self.cleaner.terminate()
			self.cleaner.wait()
			return self.SUCCESS_VALUE
		except:
			return ("An error occured pausing services.\n" + traceback.format_exc())
	
	
	def resumeServices(self):
		try:
			self.startCleaner()
			subprocess.check_output(["sudo","kill","-CONT","%d" % self.motion_pid])
			return self.SUCCESS_VALUE
		except:
			return ("An error occured resuming services.\n" + traceback.format_exc())

		
	def endServices(self):
		try:
			subprocess.check_output(["sudo","kill","-9","%d" % self.motion_pid])
			if (not(self.cleaner.poll())):
				self.cleaner.terminate()
				self.cleaner.wait()
			return self.SUCCESS_VALUE
		except:
			return ("An error occured ending services.\n" + traceback.format_exc())

		
	def evalCommand(self,com):
	# If the command is for a specific controller check_output
	# to see if the check to see if its for the this one.
		print 'BLAH 1: ' + com 
		if ((com.find('pi')>-1) and (com.find(':')>-1)):
			print ('BLAH conditional')
			try:
				tmp = com.split(':')
				if(tmp[0]!=self.HOSTNAME):
					return
				else:
					com = tmp[1]				
			except:
				pass
			
		print 'BLAH 2: ' + self.conState
			
			
		if com == 'stop':
			if self.conState == camConStates.paused:
				print ('Already stopped')
				return
			print("COMMAND: stop")
			err = self.pauseServices()
			if (err != None):
				msg = self.HOSTNAME + ':paused##' + str(err)
			else:
				msg = self.HOSTNAME + ':paused\n'
			self.conState = camConStates.paused
			return msg
		elif com=='start':
			if self.conState == camConStates.active:
				print ('Already started')
				return
			print("COMMAND: start")
			err = self.resumeServices()
			if (err != None):
				msg = self.HOSTNAME + ':started##' + str(err)
			else:
				msg = self.HOSTNAME + ':started\n'
			self.conState = camConStates.active
			return msg
		elif com == 'comp':
			if self.conState == camConStates.compressed:
				print ('Already compressed')
				return
			print("COMMAND: comp")
			err = self.compressDir()
			if (err != None):
				msg = self.HOSTNAME + ':compressed##' + str(err)
			else:
				msg = self.HOSTNAME + ':compressed\n'
			self.conState = camConStates.compressed
			return msg
		elif com == 'send':
			if self.conState == camConStates.sent:
				print ('Already sent')
				return			
			print("COMMAND: send")
			err = self.moveImages()
			if (err != None):
				msg = self.HOSTNAME + ':sent##' + str(err)
			else:
				msg = self.HOSTNAME + ':sent\n'
			self.conState = camConStates.sent
			return msg
		elif com == 'clean':
			print("COMMAND: clean")
			err = self.cleanImg()
			if (err != None):
				msg = self.HOSTNAME + ':cleaned##' + str(err)
			else:
				msg = self.HOSTNAME + ':cleaned\n'
			return msg
		elif com == 'end':
			print("COMMAND: end")
			err = self.endServices()
			if (err != None):
				msg = self.HOSTNAME + ':ended##' + str(err)
			else:
				msg = self.HOSTNAME + ':ended\n'			
			return msg		
		else:
			return com + " is not a recognized command"



	def printMenu(self,message,error):
		subprocess.call("clear")
		print (message)
		print (error)
		print ("Motion PID:%d" % self.motion_pid + " Cleaner PID:%d" % self.cleaner_pid)
		print ("The following are valid commands:")
		print ("  stop (pause services)")
		print ("  start (start services)")
		print ("  comp (compress directory)")
		print ("  send (send compressed directory)")
		print ("  clean (delete compressed directory)")
		print ("  end (end all services)")
	
	def get_ip_address(self):
		intf = 'eth0'
		intf_ip = commands.getoutput("ip address show dev " + intf).split()
		intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
		return intf_ip