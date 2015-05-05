#!/usr/bin/env python
import traceback
import sys
import subprocess
import time

cleaner_pid = 0
motion_pid = 0



def startServices():
	try:
	    cleaner = subprocess.Popen(["./cleaner.sh", "&"])
	    subprocess.call(["sudo", "service","motion", "start"])
	    time.sleep(0.05)
		c_pid = cleaner.pid
	    m_pid = int(subprocess.check_output(["pgrep","motion"]))
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
	subprocess.check_output(["sudo","kill","-STOP","%d" % motion_pid])
	subprocess.check_output(["kill","-STOP","%d" % cleaner_pid])

def resumeServices():
	subprocess.check_output(["kill","-CONT","%d" % cleaner_pid])
	subprocess.check_output(["sudo","kill","-CONT","%d" % motion_pid])

	
def endServices():
	subprocess.check_output(["sudo","kill","-9","%d" % motion_pid])
	subprocess.check_output(["kill","-9","%d" % cleaner_pid])

def printMenu(message):
	subprocess.call("clear")
	print (message)
        print ("Motion PID:%d" % motion_pid + " Cleaner PID:%d" % cleaner_pid)
	print ("The following are valid commands:")
	print ("  pause")
	print ("  continue")
	print ("  end")



if __name__ == "__main__":
	pids = startServices()
        
        motion_pid = pids[0]
        cleaner_pid = pids[1]

	printMenu("Services started")
	while True:
		s = raw_input()
		
		if (s == "pause"):
			pauseServices()
			printMenu("Services Paused")
		elif (s == "continue"):
			resumeServices()
			printMenu("Services Resumed")
		elif (s == "end"):
			endServices()
			print ("Services terminated.")
			quit()
		else:
		    print ( s + " is not a recognized command")