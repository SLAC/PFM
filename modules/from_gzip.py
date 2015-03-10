#!/usr/bin/python
#
### Info: Inflates a gzip stream.

import zlib

def convert(data, args):

	d = zlib.decompressobj(16+zlib.MAX_WBITS)
	return [d.decompress(data)]
