#!/usr/bin/python
#
### Info: URL encodes input (including spaces).

import urllib

def convert(data, args):

        return [urllib.quote_plus(data)]
