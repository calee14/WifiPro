## WifiPro

- These scripts, that will hopefully one day be in an app, are tools for performing network hacks on other devices. Some of those scripts are for running arp spoof attacks and dns spoof attacks. There is also a sniffing script. These scripts, however, require the arp spoof attack to be running so that the packets can be intercepted. 

```
# enables packet forwarding or else the device is blocked
# form receiving packets from the gateway
sysctl -w net.inet.ip.forwarding=1
```

## Usage

```
# run the arp spoof script
sudo python wifipro.py
# run any attack 
sudo python sniff.py
sudo python dns_spoof
```

## Requirements 

- Better used with Linux. Although with some finessing and some luck one should be able to get it working on MacOS and Windows.