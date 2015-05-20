#!/usr/bin/env python
from pi_cam_control import *




if __name__ == "__main__":
	camcon = CamControl()
	pids = camcon.startServices()
	
        motion_pid = pids[0]
        cleaner_pid = pids[1]

	camcon.printMenu("Services started")
	while True:
		s = raw_input()
		
		if (s == "pause"):
			camcon.pauseServices()
			camcon.printMenu("Services Paused")
		elif (s == "continue"):
			camcon.resumeServices()
			camcon.printMenu("Services Resumed")
		elif (s == "end"):
			camcon.endServices()
			print ("Services terminated.")
			quit()
		else:
		    print ( s + " is not a recognized command")


