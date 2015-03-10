#!/usr/bin/python
#
### Info: Inflates a deflate compression stream.

import zlib

def convert(data, args):

	return [zlib.decompress(data, -zlib.MAX_WBITS)]
