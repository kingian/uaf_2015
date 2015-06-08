import subprocess


def moveImages(self):
#	try:
		
		COMMAND="scp ~/uaf_2015/BT/test.txt ubuntu@10.6.66.108:~/Documents/btimg"
		print (COMMAND)
		subprocess.check_output(COMMAND)
#	except:
#		return ("An error occured compressing the motion folder.\n" + traceback.format_exc())