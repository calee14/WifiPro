from scapy.all import *
arp_frame = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst="10.1.9.135")
resp, unas = srp(arp_frame)

for s,r in resp:
	print(r[Ether].src)