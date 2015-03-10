#!/usr/bin/python
#
### Info: Extracts data payloads from all TCP, UDP & ICMP packets in a pcap. No ordering or defrag.

import binascii, dpkt, StringIO

# Defining a fake method for binding to our StringIO buffer object to make dpkt happy
# https://code.google.com/p/dpkt/source/browse/trunk/dpkt/pcap.py
def fileno():
	return 31337

def convert(data, args):
	
	out = ""
	buffer = StringIO.StringIO(data)
	# dpkt wants a name attribute for our file buffer
	buffer.name = "ballz"
	# dpkt wants a fileno method
	buffer.fileno = fileno
	pcap = dpkt.pcap.Reader(buffer)	

	for ts,buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                if eth.type == 2048:
                        ip = eth.data
                        if ip.p == 6:
                                tcp = ip.data
				if (tcp.data != ""):
					out += binascii.hexlify(tcp.data) + "\n"
			if ip.p == 17:
				udp = ip.data
				if (udp.data != ""):
					out += binascii.hexlify(udp.data) + "\n"
			if ip.p == 1:
				icmp = ip.data
				if (icmp.data != ""):
					out += binascii.hexlify(str(icmp.data)) + "\n"

        return [out]
