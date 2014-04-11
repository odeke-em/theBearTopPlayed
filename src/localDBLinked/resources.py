#!/usr/bin/env python

import sys

pyVersion = sys.hexversion/(1<<24)
urlRequester = None

if pyVersion > 2:
  import urllib.request
  from urllib.error import URLError
  urlRequester = urllib.request
  byteEncodingArgs = ('utf-8',)
else:
  import urllib2
  from urllib2 import URLError as URLError
  urlRequester = urllib2
  byteEncodingArgs = ()

UBUNTU_UAGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:13.0) ' +\
                'Gecko/20100101 Firefox/13.0'

dbPath = "./dbs/songDatabase.db" 
JSON_DUMP_PATH= "./reports/ranks.json"
RANKS_DUMP_PATH = "./reports/ranks.rk"
RANKS_TAR_BASE_PATH = "./reports/rankBack"
