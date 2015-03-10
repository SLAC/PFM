#!/usr/bin/python
#
### Info: Converts a binary plist to XML (default) or JSON format.
### Optional args: "json" for JSON format.
#
# Requires https://github.com/hay/xml2json

from biplist import readPlistFromString, writePlistToString
from xml2json import xml2json

def convert(data, args):
	class holder():
		pass
	placeholder = holder()
	placeholder.pretty = True 	

	if len(args) == 1:  	
		if (args[0] == "json" or args[0] == "JSON"):
			# xml2json() converts newlines and tabs in strings to "\n" & "\t".
			# Stripping them out of XML before conversion to JSON. 
			rawxml = writePlistToString(readPlistFromString(data),binary=False)
			rawxml = rawxml.replace("\t","")
			rawxml = rawxml.replace("\n","")
			
			return [xml2json(rawxml,placeholder)]			
	else:
		return [writePlistToString(readPlistFromString(data),binary=False)]
