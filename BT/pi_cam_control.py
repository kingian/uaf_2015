import traceback
import sys
import subprocess
import time
import commands
import json
import pexpect
import glob
import socket


class CamControl:

	cleaner_pid = 0
	motion_pid = 0
	REMOTE_USER = "ubuntu" 
	TARGET_PW = "ubuntu"
	HOST = "10.6.66.10"
	REMOTE_PATH = ""
	LOCAL_PATH = ""
	LOCAL_FILE = ""
	MOTION_DIRECTORY = "/tmp/motion"
	HOSTNAME = ""
	
	def __init__(self):
		HOSTNAME = socket.gethostname()
		pass;

	def getConfig(self,filename):
		try:
			confile = open(filename,'r+')
			configurations = json.load(confile)
			self.LOCAL_PATH = configurations['LOCAL']
			self.REMOTE_PATH = configurations['REMOTE']
		except:
			return ("An error occured reading the configuration file.\n" + traceback.format_exc())
			
	
	def compressDir(self):
		try:
			self.LOCAL_FILE = str(int(time.time())) + '.tar.gz'
			subprocess.check_output(["tar", "-cvf", self.LOCAL_FILE, "-C", self.MOTION_DIRECTORY, "."])
		except:
			return ("An error occured compressing the motion folder.\n" + traceback.format_exc()) 

	def cleanImg(self):
		try:
			rm_list = glob.glob('*.tar.gz')
			for n in rm_list:
				subprocess.check_output(['rm', n ])
		except:
			return ("An exception occured, file cleaning failed.\n" + traceback.format_exc()) 			
	
	def moveImages(self):
		try:
			FILE = self.LOCAL_PATH + '/' + self.LOCAL_FILE 
			COMMAND="scp %s %s@%s:%s" % (FILE, self.REMOTE_USER, self.HOST, self.REMOTE_PATH)
			TARGET = "%s@%s:%s" % (self.REMOTE_USER, self.HOST, self.REMOTE_PATH)
			print (COMMAND + '\n' + TARGET)
			subprocess.check_output(['scp', FILE, TARGET])
#			child = pexpect.spawn(COMMAND)
#			child.expect(pexpect.EOF)
#			print child.before
		except:
			return ("An error occured compressing the motion folder.\n" + traceback.format_exc())


	def makeDirectories(self):
		try:
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam1"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam2"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam3"])
		except:
			return ("An error occured making motion directories.\n" + traceback.format_exc())

			
	
	def startServices(self):
		err = self.makeDirectories()
		self.motion_pid
		self.cleaner_pid
		try:
			cleaner = subprocess.Popen(["./cleaner.sh", "&"])
			subprocess.call(["sudo", "service","motion", "start"])
			time.sleep(0.05)
			self.cleaner_pid = cleaner.pid
			self.motion_pid = int(subprocess.check_output(["pgrep","motion"]))
#           DEBUGGING LINES
#			print (subprocess.check_output(["pgrep","motion"]))
#			print ("Motion PID:%d" % self.motion_pid)
#			print ("Cleaner PID:%d" % self.cleaner_pid)
			print ("Motion and Cleaner services sucessfully started.\n")
			return [self.motion_pid,self.cleaner_pid]
		except Exception, err:
			return ("An exception occured, Motion and Cleaner didn't start.\n" + traceback.format_exc())

	def startCleaner(self):
		
		
		
	def pauseServices(self):
		try:
			subprocess.check_output(["sudo","kill","-STOP","%d" % self.motion_pid])
			subprocess.check_output(["kill","-9","%d" % self.cleaner_pid])
		except:
			return ("An error occured pausing services.\n" + traceback.format_exc())
	
	
	def resumeServices(self):
		try:
			subprocess.check_output(["kill","-CONT","%d" % self.cleaner_pid])
			subprocess.check_output(["sudo","kill","-CONT","%d" % self.motion_pid])
		except:
			return ("An error occured resuming services.\n" + traceback.format_exc())

		
	def endServices(self):
		try:
			subprocess.check_output(["sudo","kill","-9","%d" % self.motion_pid])
			subprocess.check_output(["kill","-9","%d" % self.cleaner_pid])
		except:
			return ("An error occured ending services.\n" + traceback.format_exc())

		
	def evalCommand(self,com):
		if (com == 'stop'):
			err = this.pauseServices()
			msg = HOSTNAME + ': Paused Services\n' + err
			return msg
		elif (com=='start'):
			err = this.resumeServices()
			msg = HOSTNAME + ': Started Services\n' + err
			return msg
		elif (com == 'comp'):
			err = this.compressDir()
			msg = HOSTNAME + ': Compresed Motion Directory\n' + err
			return msg
		elif (com == 'send'):
			err = this.moveImages()
			msg = HOSTNAME + ': Tarball Sent\n' + err
			return msg
		elif (com == 'clean'):
			err = this.cleanImg()
			msg = HOSTNAME + ': Tarball Cleanded\n' + err
			return msg
		elif (com == 'end'):
			err = this.endServices()
			msg = HOSTNAME + ': Tarball Cleanded\n' + err
			return msg		
		else:
			return (com + " is not a recognized command")
		
		

	
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