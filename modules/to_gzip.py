#!/usr/bin/python
#
### Info: Creates a gzip stream.

import zlib

def convert(data, args):

	d = zlib.compressobj(6, zlib.DEFLATED, 16+zlib.MAX_WBITS)
	return [d.compress(data) + d.flush()]

