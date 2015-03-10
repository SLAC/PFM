#!/usr/bin/python
#
### Info: Performs an XOR against the input using a supplied key.
### Required args: A single or multi-byte XOR key in plain hex (no spaces, no leading 0x) is required.

from binascii import unhexlify
from itertools import izip, cycle

def convert(data, args):
	
	xored = ''

	if len(args) == 1:
		key = unhexlify(args[0])
		xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))

        return [xored]
