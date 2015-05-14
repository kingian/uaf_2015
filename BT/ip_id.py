import commands

def get_ip_address():
	intf = 'eth0'
	intf_ip = commands.getoutput("ip address show dev " + intf).split()
	intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
	return intf_ip