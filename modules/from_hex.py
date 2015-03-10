#!/usr/bin/env python
#
### Info: Converts a hex dump to raw data. Supported formats include xxd, Wireshark, hexdump and plain hex with no spacing.

import re
from binascii import unhexlify

def convert(data,args):
	
	cinfo = ""
	converted = ''
	raw_hex = re.compile('^([0-9a-fA-F][0-9a-fA-F]+)$')
	tcpdump_hex = re.compile('^0x([0-9a-fA-F][0-9a-fA-F]){2}:\s+[0-9a-fA-F][0-9a-fA-F]')
	wireshark_hex = re.compile('^([0-9a-fA-F][0-9a-fA-F]){4}:?\s+[0-9a-fA-F][0-9a-fA-F]\s+')
	wireshark_hex2 = re.compile('^([0-9a-fA-F][0-9a-fA-F]){2}:?\s+[0-9a-fA-F][0-9a-fA-F]\s+')
	xxd_hex = re.compile('^[0-9a-fA-F]{7}:\s+[0-9a-fA-F][0-9a-fA-F]')
	hexdump_hex = re.compile('^[0-9a-fA-F]{7}\s+[0-9a-fA-F][0-9a-fA-F]')
	spaced_hex = re.compile('^(([0-9a-fA-F][0-9a-fA-F]\s+)+)$')

        for line in data.splitlines():
                line = line.lstrip()

                if raw_hex.match(line):
                        converted += unhexlify(line)
            	elif tcpdump_hex.search(line):
            			converted += unhexlify(line[9:48].replace(" ", ""))
                elif wireshark_hex.search(line):
                        converted += unhexlify(line[10:58].replace(" ", ""))
                elif wireshark_hex2.search(line):
                        converted += unhexlify(line[7:54].replace(" ", ""))
                elif xxd_hex.search(line):
                        converted += unhexlify(line[9:48].replace(" ", ""))
                elif hexdump_hex.search(line):
                        converted += unhexlify(line[8:55].replace(" ", ""))
                else:
			line = line + " "
			if spaced_hex.match(line):
                        	converted += unhexlify(line.replace(" ", ""))
	
	return [converted, cinfo]
