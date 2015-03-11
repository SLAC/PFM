# PFM

PFM is a data manipulation tool for security analysts and incident responders. A core capability is the ability to "chain" data manipulation modules to speed analyst workflow and improve local data handling procedures (eg. not using
random online website to process base64-encoded data). PFM is designed to be easily extensible via python scripts for integration of current tools or to create new modules as needed. PFM is based on, but does not share code with, a similar tool in use by the US DoD.

To do:
	JSON-based API
	Unicode support?
	Install script
	CLI wrapper
	Unittest support
	PEP 8 styling
	Documentation

Directory structure:
	Top-level (pfm.py, pfm.js, pfm.css)
		modules (from_*py, to_*py, do_*py)
		data (logs & other data, you probably don't want this globally viewable)

External dependencies
	pfm.py:
		easy_install requests
	from_bplist.py:
		easy_install biplist
		https://github.com/hay/xml2json

Install steps:
	Install external dependencies (see above)
	Copy pfm directory to /var/www/ 
	Configure web server to execute python scripts at /var/www/pfm
	Ensure data directory and files can be read & written to by web server
Recommended:
	Lockdown data directory files (.htaccess or similar) 
	Enable SSL on web server to avoid triggering IDS/WAF/etc
	Setup access control via web server; you really don't want this publicly accessible
