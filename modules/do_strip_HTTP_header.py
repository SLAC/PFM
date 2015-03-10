#!/usr/bin/python
#
### Info: Strips the HTTP header from a dumped TCP stream.

def convert(data, args):
	info = ""
	if data[:4] == "HTTP" or data[:4] == "http":
		if ("Transfer-Encoding: chunked" in data):
			info += 'HTTP <a href="http://en.wikipedia.org/wiki/Chunked_transfer_encoding" target=_new>chunking</a> detected'
		return [data[data.find("\x0d\x0a\x0d\x0a") + 4:],info]
	else:
		info += "Valid HTTP header not detected."
		return [data,info]
