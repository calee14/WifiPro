from scapy.all import Ether, ARP, srp, sniff, conf

def get_mac(ip):
	"""
	Returns the MAC address of 'ip', if it is unable to find it
	for some reason, throws 'IndexError'
	"""
	p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
	result = srp(p, timeout=3, verbose=False)[0]
	return result[0][1].hwsrc

def process(packet):
	# if the packet is an ARP packet
	if packet.haslayer(ARP):
		# if it is an ARP reponse (ARP reply)
		if packet[ARP].op == 2:
			try:
				# get the real MAC address of the sender
				real_mac = get_mac(packet[ARP].psrc)
				# get the MAC address from the packet sent to us
				response_mac = packet[ARP].hwsrc
				# if they're different, difinetely there is an attack
				if real_mac != resonse_mac:
					print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
			except IndexError:
				# unable to find the real mac
				# maybe a fake IP or firewall is blocking packets
				pass

sniff(store=False, prn=process)