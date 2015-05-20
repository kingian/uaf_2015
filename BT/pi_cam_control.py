import traceback
import sys
import subprocess
import time
import commands
import json


class CamControl:

	cleaner_pid = 0
	motion_pid = 0
	remote_target = ""
	local_target = ""
	image_tarball = ""
	mot_dir = "/tmp/motion"


	def getConfig(self,filename):
		confile = open(filename,'r+')
		configurations = json.load(filename)
		self.local_target = configurations['LOCAL']
		self.remote_target = configurations['REMOTE']
	
	def compressDir(self):
		self.image_tarball = str(int(time.time())) + '.tar.gz'
		subprocess.check_output(["tar","-zcvf",image_tarball,mot_dir])

	
	def moveImages(self):
		subprocess.check_output(["scp",self.local_target,self.remote_target])
	
	
	def startServices(self):
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
		subprocess.check_output(["sudo","kill","-STOP","%d" % self.motion_pid])
		subprocess.check_output(["kill","-STOP","%d" % self.cleaner_pid])
	
	
	def resumeServices(self):
		subprocess.check_output(["kill","-CONT","%d" % self.cleaner_pid])
		subprocess.check_output(["sudo","kill","-CONT","%d" % self.motion_pid])
	
	def endServices(self):
		subprocess.check_output(["sudo","kill","-9","%d" % self.motion_pid])
		subprocess.check_output(["kill","-9","%d" % self.cleaner_pid])

	
	def printMenu(self,message):
		subprocess.call("clear")
		print (message)
		print ("Motion PID:%d" % self.motion_pid + " Cleaner PID:%d" % self.cleaner_pid)
		print ("The following are valid commands:")
		print ("  pause")
		print ("  continue")
		print ("  end")
	
	def get_ip_address(self):
		intf = 'eth0'
		intf_ip = commands.getoutput("ip address show dev " + intf).split()
		intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
		return intf_ip