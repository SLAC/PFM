#!/usr/bin/python
#
### Info: Bz2 compresses data.

import bz2

def convert(data, args):

	return [bz2.compress(data)]
