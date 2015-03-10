#!/usr/bin/python
#
### Info: Quick byte frequency analysis of input. Also performs a Shannon entropy check - the closer to 1.0 the more random the data (possibly indicating encryption).

import math,os,sys

def convert(data, args):
	
	i = -1
	count = 1	
	out = ""
	ent = 0.0
        table = [0] * 256
        for c in data:
        	table[ord(c)] += 1    		
	
	for c in table:
		if c > 0:
			freq = float(c) / len(data)
			ent = ent + freq * math.log(freq, 2) 
		i += 1
		if count == 5:
			out += '%02X = %d' % (i, c) + "\n"
			count = 0
		else:
			out += '%02X = %d' % (i, c) + "\t\t"
        	count += 1

	ent = -ent    	
	out = "Entropy: " + str(ent/8) + "\n" + out

        return [out]