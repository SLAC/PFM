#!/usr/bin/python
#
### Info: Inflates bz2 compressed data.

import bz2

def convert(data, args):

	return [bz2.decompress(data)]
