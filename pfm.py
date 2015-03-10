#!/usr/bin/python
#
# pfm.py - main script
# Pure Funky Magic (PFM) v0.1 
# by Mario R. De Tore, SLAC National Accelerator Laboratory
#
# PFM is a data manipulation tool for security analysts and incident responders.
# A core capability is the ability to "chain" data manipulation modules to speed
# analyst workflow and improve local data handling procedures (eg. not using
# random online website to process base64-encoded data). PFM is designed to be
# easily extensible via python scripts for integration of current tools or to 
# create new scripts as needed. PFM is a complete rewrite of a similar tool in 
# use by the US DoD.
#
# To do:
# 	JSON-based API
# 	Unicode support?
#	Install script
#	CLI wrapper
# 	Unittest support
#	PEP 8 styling
#	Documentation
#
# Directory structure:
#	Top-level (pfm.py, pfm.js, pfm.css)
#		modules (from_*py, to_*py, do_*py)
#		data (logs & other data, you probably don't want this globally viewable)
#
# External dependencies
#	pfm.py:
#		easy_install requests
#	from_bplist.py:
#		easy_install biplist
#		https://github.com/hay/xml2json
#
# Install steps:
#	Install external dependencies (see above)
#	Copy pfm directory to /var/www/ 
#	Configure web server to execute python scripts at /var/www/pfm
#	Ensure data directory and files can be read & written to by web server
# Recommended:
#	Lockdown data directory files (.htaccess or similar) 
#	Enable SSL on web server to avoid triggering IDS/WAF/etc
#	Setup access control via web server; you really don't want this publicly accessible

import base64
import cgi
import glob
import hashlib
import json
import os
import re
import requests
import sys
import time

sys.path.append("modules")

# Local data directory for usage log & storing data
datadir = "data/"
# https://github.com/seejohnrun/haste-server
hastebin_server = "https://haste.yourdomain.com/"

# HTML special character escaping - anything going back to the browser should be 
# filtered with this to counter XSS and other things. User should send output to 
# file if they want truly unfiltered results.
def escape(text):
	if text:
		# Replace non-printables with "." 
		text = re.sub('[^\s!-~]', '.', text)
		# HTML-escape text
		return (text
			.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
			.replace("'", "&#39;").replace('"', "&quot;")
			)
            
# Builds select options and extracts converter info & required args
def opts(header):
	options = ""
	cinfo = ""
	oargs = ""
	adata = ""
	for item in sorted(glob.glob("modules/" + header + "*.py")):
		option = item[8:-3]
		optionv = item[8:-3]
		for line in open(item):
			if "### Info:" in line:
				cinfo += option + ": " + line.replace("### Info: ", "") + "<br>"
			if "### Required args:" in line:
				optionv += ": " + line.replace("### Required args: ","").rstrip()
				option += " *"
				cinfo += "<i>- required arg(s): " + line.replace("### Required args: ","").rstrip() + "</i><br>"
			if "### Optional args:" in line:
				cinfo += "<i>- optional arg(s): " + line.replace("### Optional args: ","").rstrip() + "</i><br>"
		options += "<option value=\"" + optionv + "\">" + option + "</option>"
	return [options, cinfo]

# The workhorse 
def do_the_things(data,chain):
	# Loop through the converters
	converted = []
	info = ""
	for item in chain:
		slice_arg = ""
		aflag = False
		bflag = False
		astop = ""
		bstop = ""
		# Check to see if args were included; if so put them in a list (assumes 
		# the args are separated with spaces from the converter name and each 
		# other)
		module_name = item.split().pop(0)
		args = item.split()[1:]
		# Check for and remove splicing arg 
		slice_idx = [i for i, item in enumerate(args) if ":" in item]	
		try:
			for slice in slice_idx:
				slice_arg = args[slice]
				slicel = slice_arg.split(":")
				sstart = slicel[0]
				if sstart:
					# Filter out args that aren't slicing related. "--" prepended
					# to an arg prevents it being evaluated as a slice argument.
					if (sstart[0] != "a" or sstart[0] != "b" or sstart[:1] == "--"):
						slice_idx.remove(slice)	
					if sstart[0] == "b":
						bstart = sstart[1:]
						bflag = True
						if bstart != "":
							bstart = int(bstart,0)
						else:
							bstart = 0 
						if slicel[1]:
							bstop = int(slicel[1],0)
					if sstart[0] == "a":
						aflag = True
						astart = sstart[1:]
						if astart != "":
							astart = int(astart,0)
						else:
							astart = 0
						if slicel[1]:
							astop = int(slicel[1],0)

			args = [v for i, v in enumerate(args) if i not in slice_idx]
			
		except:
			info = info + " \n\n<b style=\"color:red\">" + module_name + ":<br>" + str(sys.exc_info()[1]) + "</b>"
			return [data, info]
		# Import the converter script
		mod = __import__(module_name, fromlist=[''])
    	# Call the convert function from the imported module
		try:
			# If the data slice option before processing is set:
			if (bflag):
				if bstop:
					data = data[bstart:bstop]
				else:
					data = data[bstart:]
			converted = mod.convert(data,args)
			data = converted[0]
			# If the data slice option after processing is set:
			if (aflag):
				if astop:
					data = data[astart:astop]
				else:
					data = data[astart:]
			if len(converted) == 2:
				if converted[1] != "":
					info += module_name + ": " + converted[1] + "\n"
		except:
			info = info + " \n\n<b style=\"color:red\">" + module_name + ": " + str(sys.exc_info()[1]) + "</b>"
			return [data, info]
	# Log the activity
	user_agent = os.environ["HTTP_USER_AGENT"]
	ip = os.environ["REMOTE_ADDR"]
	ctime = str(int(time.time()))
	achain = ', '.join(chain)
	entry = ctime + "   " + ip + "   " + achain + "   " + user_agent + "\n"
	f = open(datadir + "log.txt","a+")
	f.write(entry)
	f.close
	return [data,info]

# Load the values passed from HTTP
form = cgi.FieldStorage()

# Below var order is important for the template formatting
from_options = ""
to_options = ""
do_options = ""
original_old = ""
info = ""
converted = []
converter_info = ""

# Load the dropdown options for the various groups of converters. Assumes that converter 
# scripts are in the modules subdirectory off of where ever this script resides.
# Need to write a function for this.

_from = opts("from")
from_options += _from[0]
converter_info += _from[1] + "<br>"
	
_to = opts("to")
to_options += _to[0]
converter_info += _to[1] + "<br>"

_do = opts("do")
do_options += _do[0]
converter_info += _do[1] + "<br>"

# Load the converter chain
coflag = False
chain_options = ""
if form.getvalue("getchain"):
	chain_opts = []
	f = open(datadir + "savechain.txt","r")
	for line in f:
		if form.getvalue("getchain") in line:
			for opt in base64.b64decode(line.split(",")[1]).split(","):
				chain_opts.append(base64.b64decode(opt))
	
	for opt in chain_opts:
		# Need to add code here to pull in option values from above
		chain_options += "<option value=\"" + opt +"\">" + opt + "</option>"
		coflag = True
				
	f.close()

if not coflag:
	chain_options = '''
						<option value="0" >Choose</option>
						<option value="0" >from</option>
						<option value="0" >left</option>
	'''

# Handle savechain GET requests

if form.getvalue("savechain"):
	# You need to make sure your webserver has permission to write to this directory/file
	savechain = form.getvalue("savechain")
	f = open(datadir + "savechain.txt","a+")
	m = hashlib.md5()
	m.update(savechain)
	md5 = m.hexdigest()
	logged = False
	
	for line in f:
		if savechain in line:
			logged = True
	if not logged:	
		f.write(md5 + "," + savechain + "\n")
		f.close()

	print "Content-type: text/html"
	print
	print "?getchain=" + md5

	exit()

# The orignal that goes back to the browser needs to be escaped
if form.getvalue("original"):
	original_old = escape(form.getvalue("original"))

# We need some input data and a converter selection to move forward
if ((form.getvalue("inputFile") or form.getvalue("original")) and form.getvalue("chain")):
	# This is the raw input data
	if (form.getvalue("inputFile")):
		data = form.getvalue("inputFile")
	else:
		data = form.getvalue("original")
	# This is the converter chain
	chain = form.getvalue("chain")
	# Was "chain" passed as a list or a single item (string)? Do some 
	# normalization so chain is passed on later as a list, even if its a single 
	# item
	if isinstance(chain, str):
		chain = [chain] # Poof, its a single item list now
	# Repopulating the converter selections
	chain_options = ""
	for option in chain:
		chain_options += "<option value=\"" + option + "\" >" + option + "</option>"

	# This is where the magic happens 
	converted = do_the_things(data,chain)
	info = converted[1]

else:
	converted.append(form.getvalue("original"))

# The webpage template
content = '''
	<head>

		<title>Pure Funky Magic!</title>

		<link rel="stylesheet" type="text/css" href="pfm.css"/>
		<script src="pfm.js"></script>
		<meta name="robots" content="noindex,nofollow"/>

	</head>

	<body onload="toggleText(); theTime(%s);">
	<div id="blanket" style="display:none"></div>
	<form method="POST" onsubmit="selectAll();" enctype="multipart/form-data">
		<div id="key" tabindex="1">
		<div id="minimize" onclick="toggleHeader();">-</div>
		<table>
			<tr id="row1">
				<div id="header" onclick="toggleHeader();">
				PFM
				</div>
			</tr>
			<tr id="row2">
				<td>
				<div class="styled-select" id="lcol">
					<select id="selectFrom" onchange="AddToChain('From');">
						<option value="">FROM</option>%s
					</select>
					<br>
							<select id="selectTo" onchange="AddToChain('To');">
						<option value="">TO</option>%s
							</select>
							<br>
					<select id="selectDo" onchange="AddToChain('Do');">
						<option value="">DO</option>%s
					</select>
					<br>
					Args:<br>
					<input type="text" size=7 id="args" onchange="updateChainArgs();">
				</div>
				</td>
				<td>
				<div id="ccol" class="styled-select-chain">
					<select name="chain" size="7" id="chain" ondblclick="remove_from_chain();" onChange="updateArgsBox();">%s</select>
				</div>
				</td>
				<td>
				<div id="rcol">
					<div onclick="moveUp();" title="move up">&#x2191</div>
					<div onclick="moveDown();" title="move down">&#x2193</div>
					<div onclick="remove_from_chain();" title="remove item">-</div>
					<div onclick="clearChain()" title="clear chain">*</div>
					<div onclick="saveChain()"><img src="save.png" alt="save chain" title="save chain" height="16" width="16"></div>
				</div>
				</td>
			</tr>
			<tr id="row3">
				<td colspan="3">
				<div class="styled-select" id="footer">
					Target:<select name="selectOutput" id="selectOutput">
						<option value="web">webpage</option>
						<option value="file">file</option>
						<option value="hastebin">hastebin</option>
						<option value="raw">raw</option>
					</select>
					<input type="submit" class="button" value="Do the thing(s)">
				</div>
				</td>
			</tr>
		</table>
		<div id="alertDiv" style="display:none" tabindex="0">%s</div>
		</div>

		<div id="input">
			<label>Input:</label>
			<button type="button" id="btnInputHide" onclick="hideInput();">Hide input</button>
			<button type="button" id="btnInputShow" style="display: none" onclick="showInput();">Show input</button>
			<input type="file" name="inputFile" id="btnInputFile" size="50" onchange="document.getElementById('original').value = ''; document.getElementById('original').disabled = true;">
			<button type="button" id="btnInputClear" onclick="clearInput();">Clear input</button>
			<textarea name="original" id="original" spellcheck="false">%s</textarea>
		</div>
			
		<div id="popUpDiv" style="display:none" tabindex="0">		
			<br>
			<input type="text" size=7 id="popupargs">
			<button type="button" id="btnPopupArgs" onclick="closePopup();">Ok</button>
		</div>
		<div id="output" style="display: none;">
			<div id="info" style="display: none;">
			</div>
			<label>Output:</label><button type="button" onclick="moveToInput();">Move to input</button>
			<section contextmenu="mymenu">
        	<textarea name="converted" id="converted" spellcheck="false">%s</textarea>
        	<menu type="context" id="mymenu">
				<menuitem label="Copy selection to input" onclick="copySelected();" icon="copy.png"></menuitem>
			</menu>
        	</section>
        </div>
	</form>
	Module descriptions<br>
	<b>Note:</b> Slicing is now enabled to trim data before and/or after processing by a
	specific module. This feature is based on the Python slicing notation preceded by an
	"a" or "b" to allow you to slice data before ("b") you send data to a PFM module or
	after ("a") it has been processed. For example, adding "b0:128 a64:-32" as module
	arguments will cause PFM to only send the first 128 bytes of data to a module and
	return only the 64th through whatever byte is 32 bytes from the end of the processed
	data for that module. Similarly, "b18: a:256" will suppress the first 18 bytes of
	data to the module and return the first 256 bytes of processed data. Stepping and
	other advanced slicing features are not supported however. The script checks for
	arguments beginning with an "a" or "b" that contain a colon and treats them as
	slicing arguments. To override this for a specific argument (like a zip password
	that happens to match that pattern) prepend it with "--".
	<br><br>
	<div id="converter_info">
	%s
	</div>
	</body>
'''

if (form.getvalue("selectOutput") == "file"):
	# Send the headers
	print "Content-type: application/octet-stream"
	print 'Content-disposition: attachment; filename="PFM_out_' + str(int(time.time())) + '"'
	print
	sys.stdout.write(converted[0])
	
elif (form.getvalue("selectOutput") == "hastebin"):
	# POST the results to hastebin
	r = requests.post(hastebin_server + "documents", verify=False, data=converted[0])
	url = hastebin_server + json.loads(r.text)['key']	

	print "Location: " + url
	print
	
elif (form.getvalue("selectOutput") == "raw"):
	# Write raw output to the browser. User is on their own safety-wise.
	print "Content-type: text"
	print
	print converted[0]

else:
	thetime = int(time.time() * 1000)
	# Send the headers - second print statement is very important!
	print "Content-type: text/html"
	print
	print "<html>"
	# Pull in and populate the template
	body = content % (thetime, from_options, to_options, do_options, chain_options, info, original_old, escape(converted[0]), converter_info)
	# If you change the below review all the code - lots of dependencies on this.
	print body.replace(">None<","><") 	
	# FIN
	print "</html>"
