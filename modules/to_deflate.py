#!/usr/bin/python
#
### Info: Creates a deflate compression stream.

import zlib

def convert(data, args):

	d = zlib.compressobj(6, zlib.DEFLATED, -zlib.MAX_WBITS)
	return [d.compress(data) + d.flush()]
