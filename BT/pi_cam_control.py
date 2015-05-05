import traceback
import sys
import subprocess
import time

cleaner_pid = 0
motion_pid = 0
remote_target = ""

def compressImgDir(targetfile,targetdirectory):
	subprocess.check_output(["tar","-zcvf",targetfile,targetdirectory])


def startServices():
	global motion_pid
	global cleaner_pid
	try:
		cleaner = subprocess.Popen(["./cleaner.sh", "&"])
		subprocess.call(["sudo", "service","motion", "start"])
		time.sleep(0.05)
		cleaner_pid = cleaner.pid
		motion_pid = int(subprocess.check_output(["pgrep","motion"]))
#           DEBUGGING LINES
#	    print (subprocess.check_output(["pgrep","motion"]))
#	    print ("Motion PID:%d" % m_pid)
#	    print ("Cleaner PID:%d" % c_pid)
		print ("Motion and Cleaner services sucessfully started.\n")
		return [m_pid,c_pid]
	except Exception, err:
		print ("An exception occured, Motion and Cleaner didn't start.\n")
		print traceback.format_exc()

def pauseServices():
	global motion_pid
	global cleaner_pid
	subprocess.check_output(["sudo","kill","-STOP","%d" % motion_pid])
	subprocess.check_output(["kill","-STOP","%d" % cleaner_pid])

def resumeServices():
	global motion_pid
	global cleaner_pid
	subprocess.check_output(["kill","-CONT","%d" % cleaner_pid])
	subprocess.check_output(["sudo","kill","-CONT","%d" % motion_pid])

	
def endServices():
	global motion_pid
	global cleaner_pid
	subprocess.check_output(["sudo","kill","-9","%d" % motion_pid])
	subprocess.check_output(["kill","-9","%d" % cleaner_pid])

def printMenu(message):
	global motion_pid
	global cleaner_pid
	subprocess.call("clear")
	print (message)
	print ("Motion PID:%d" % motion_pid + " Cleaner PID:%d" % cleaner_pid)
	print ("The following are valid commands:")
	print ("  pause")
	print ("  continue")
	print ("  end")