#!/usr/bin/python
#
### Info: Inflates a zlib stream.

import zlib

def convert(data, args):

	#d = zlib.decompressobj(16+zlib.MAX_WBITS)
	d = zlib.decompressobj()
	return [d.decompress(data)]
