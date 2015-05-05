#!/usr/bin/env python
from pi_cam_control import *

cleaner_pid = 0
motion_pid = 0


if __name__ == "__main__":
	pids = startServices()
        
#        motion_pid = pids[0]
#        cleaner_pid = pids[1]

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