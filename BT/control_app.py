#!/usr/bin/env python
from pi_cam_control import *

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


if __name__ == "__main__":
	camcon = CamControl()
	pids = camcon.startServices()
	
#        motion_pid = pids[0]
#        cleaner_pid = pids[1]

	printMenu("Services started")
	while True:
		s = raw_input()
		
		if (s == "pause"):
			camcon.pauseServices()
			printMenu("Services Paused")
		elif (s == "continue"):
			camcon.resumeServices()
			printMenu("Services Resumed")
		elif (s == "end"):
			camcon.endServices()
			print ("Services terminated.")
			quit()
		else:
		    print ( s + " is not a recognized command")
			
