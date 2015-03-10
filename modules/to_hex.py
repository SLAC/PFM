#!/usr/bin/python
#
### Info: Provides a hexdump of the input.
### Optional args: "stream" will convert to hex stream

import hexdump
import binascii

def convert(data,args):

	if len(args) == 1:
		if args[0] == "stream":
			return [binascii.hexlify(data)]	

        return [hexdump.hexdump(data,result='return')]
