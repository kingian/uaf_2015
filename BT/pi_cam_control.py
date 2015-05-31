import traceback
import sys
import subprocess
import time
import commands
import json
import pexpect


class CamControl:

	cleaner_pid = 0
	motion_pid = 0
	REMOTE_USER = "ubuntu" 
	TARGET_PW = "ubuntu"
	HOST = "10.6.66.118"
	REMOTE_PATH = ""
	LOCAL_PATH = ""
	LOCAL_FILE = ""
	MOTION_DIRECTORY = "/tmp/motion"


	def getConfig(self,filename):
		try:
			confile = open(filename,'r+')
			configurations = json.load(confile)
			self.LOCAL_PATH = configurations['LOCAL']
			self.REMOTE_PATH = configurations['REMOTE']
		except:
			print ("An error occured reading the configuration file.\n")
			print traceback.format_exc()
			
	
	def compressDir(self):
		try:
			self.LOCAL_FILE = str(int(time.time())) + '.tar.gz'
			subprocess.check_output(["tar", "-zcvf", self.LOCAL_FILE, self.MOTION_DIRECTORY])
		except:
			print ("An error occured compressing the motion folder.\n")
			print traceback.format_exc()

	def cleanImg(self):
		try:
			subprocess.check_output(['rm', '*.tar.gz'])
		except:
			print ("An exception occured, file cleaning failed.\n")
			print traceback.format_exc()			
	
	def moveImages(self):
		FILE = self.LOCAL_PATH + '/' +self.LOCAL_FILE 
		COMMAND="scp -oPubKeyAuthentication=no %s %s@%s:%s" % (FILE, self.REMOTE_USER, self.HOST, self.REMOTE_FILE)
		child = pexpect.spawn(COMMAND)
		child.expect('password:')
		child.sendline(PASS)
		child.expect(pexpect.EOF)
		print child.before
		
#		try:
#			sendReq = pexpect.spawn('scp',[self.local_target + self.image_tarball , self.remote_target])
#			sendReq.expect('Password:')
#			time.sleep(0.1)
#			sendReq.sendline(target_pw)
#		except:
#			print ("An error occured compressing the motion folder.\n")
#			print traceback.format_exc()


	def makeDirectories(self):
		try:
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam1"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam2"])
			subprocess.call(["sudo", "mkdir","/tmp/motion/cam3"])
		except:
			print ("An error occured making motion directories.\n")
			print traceback.format_exc()
			
	
	def startServices(self):
		makeDirectories()
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
			print ("An exception occured, Motion and Cleaner didn't start.\n")
			print traceback.format_exc()

		
	def pauseServices(self):
		try:
			subprocess.check_output(["sudo","kill","-STOP","%d" % self.motion_pid])
			subprocess.check_output(["kill","-STOP","%d" % self.cleaner_pid])
		except:
			print ("An error occured pausing services.\n")
			print traceback.format_exc()
	
	
	def resumeServices(self):
		try:
			subprocess.check_output(["kill","-CONT","%d" % self.cleaner_pid])
			subprocess.check_output(["sudo","kill","-CONT","%d" % self.motion_pid])
		except:
			print ("An error occured resuming services.\n")
			print traceback.format_exc()

		
	def endServices(self):
		try:
			subprocess.check_output(["sudo","kill","-9","%d" % self.motion_pid])
			subprocess.check_output(["kill","-9","%d" % self.cleaner_pid])
		except:
			print ("An error occured ending services.\n")
			print traceback.format_exc()

	
	def printMenu(self,message):
		subprocess.call("clear")
		print (message)
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