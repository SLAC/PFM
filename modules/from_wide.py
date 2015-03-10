#!/usr/bin/python
#
### Info: Converts two-byte wide characters (UTF-16 unicode) to one-byte characters. 

def convert(data, args):

        return [str(data.decode('utf-16'))]
