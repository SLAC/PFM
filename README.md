# PFM

PFM is a data manipulation tool for security analysts and incident responders. A core capability is the ability to "chain" data manipulation modules to speed analyst workflow and improve local data handling procedures (eg. not using
random online website to process base64-encoded data). PFM is designed to be easily extensible via python scripts for integration of current tools or to create new modules as needed. PFM is based on, but does not share code with, a similar tool in use by the US DoD.

To do:
<br>	JSON-based API
<br>	Unicode support?
<br>	Install script
<br>	CLI wrapper
<br>	Unittest support
<br>	PEP 8 styling
<br>	Documentation

External dependencies
<br>	pfm.py:
	<br>	easy_install requests
	<br>from_bplist.py:
	<br>	easy_install biplist
	<br>	https://github.com/hay/xml2json

Install steps:
<br>	Install external dependencies (see above)
<br>	Copy pfm directory to /var/www/ 
<br>	Configure web server to execute python scripts at /var/www/pfm
<br>	Ensure data directory and files can be read & written to by web server

Recommended:
<br>	Lockdown data directory files (.htaccess or similar) 
<br>	Enable SSL on web server to avoid triggering IDS/WAF/etc
<br>	Setup access control via web server; you really don't want this publicly accessible
