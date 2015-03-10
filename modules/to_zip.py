#!/usr/bin/python
#
### Info: Zip compresses input data.

import zipfile
from StringIO import StringIO

def convert(data, args):
	
	temp = StringIO()
	temp.write(data)
	dst = StringIO()
	zf = zipfile.ZipFile(dst, mode="w", compression=zipfile.ZIP_DEFLATED)
	zf.writestr("pfm.data", temp.getvalue())
	zf.close()
	return [dst.getvalue()]

