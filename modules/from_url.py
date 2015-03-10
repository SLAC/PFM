#!/usr/bin/python
#
### Info: URL decodes the input (including encoded spaces).

import urllib

def convert(data, args):

        return [urllib.unquote_plus(data)]
