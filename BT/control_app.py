#!/usr/bin/env python
from pi_cam_control import *




if __name__ == "__main__":
	camcon = CamControl()
	err = camcon.getConfig('config.json')
	pids = camcon.startServices()
	
        motion_pid = pids[0]
        cleaner_pid = pids[1]

	camcon.printMenu("Services started",err)
	while True:
		s = raw_input()
		
		if (s == "stop"):
			err = camcon.pauseServices()
			camcon.printMenu("Services paused", err)
		elif (s == "start"):
			err = camcon.resumeServices()
			camcon.printMenu("Services resumed", err)
		elif (s == "comp"):
			err = camcon.compressDir()
			camcon.printMenu("Directory compressed", err)
		elif (s == "send"):
			err = camcon.moveImages()
			camcon.printMenu("Tarball copied to remote host", err)
		elif (s == "clean"):
			err = camcon.cleanImg()
			camcon.printMenu("Tarball deleted", err)
		elif (s == "end"):
			err = camcon.endServices()
			print ("Services terminated.", err)
			quit()
		else:
		    print ( s + " is not a recognized command")


