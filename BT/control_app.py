#!/usr/bin/env python
from pi_cam_control import *




if __name__ == "__main__":
	camcon = CamControl()
	camcon.getConfig('config.json')
	pids = camcon.startServices()
	
        motion_pid = pids[0]
        cleaner_pid = pids[1]

	camcon.printMenu("Services started")
	while True:
		s = raw_input()
		
		if (s == "stop"):
			camcon.pauseServices()
			camcon.printMenu("Services paused")
		elif (s == "start"):
			camcon.resumeServices()
			camcon.printMenu("Services resumed")
		elif (s == "comp"):
			camcon.compressDir()
			camcon.printMenu("Directory compressed")
		elif (s == "send"):
			camcon.moveImages()
			camcon.printMenu("Tarball copied to remote host")
		elif (s == "clean"):
			camcon.cleanImg()
			camcon.printMenu("Tarball deleted")
		elif (s == "end"):
			camcon.endServices()
			print ("Services terminated.")
			quit()
		else:
		    print ( s + " is not a recognized command")


