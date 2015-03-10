#!/usr/bin/python
#
### Info: Expands a zip file.
### Optional args: Zip archive password 

import zipfile
from StringIO import StringIO

def convert(data, args):

	temp = StringIO()
	temp.write(data)
	zf = zipfile.ZipFile(temp, "r")
	if args:
		zf.setpassword(args[0])
	data = ""
	for file in zf.namelist():
		data += zf.read(file) 

        return [data]
