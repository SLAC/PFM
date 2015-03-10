#!/usr/bin/python
#
### Info: Converts unix epoch timestamp to human formatted time (GMT).

import time

def convert(data, args):
   
	return [time.strftime('%Y-%m-%d %H:%M:%S GMT', time.gmtime(int(data)))]
