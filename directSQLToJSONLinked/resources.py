#!/usr/bin/env python

import os
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

def delegateFileWriting(path, data, isBinary=False):
  if not path:
    return -1
  elif not os.path.exists(path):
    dirPath = os.path.dirname(path)
    if not os.path.exists(dirPath):
        try:
            os.mkdir(dirPath)
        except Exception: # TODO: Actual verbosity
            return -1
        else:
            sys.stderr.write('\033[42mSuccessfully created directory: %s\033[00m\n'%(dirPath))
    elif not os.access(dirPath, os.W_OK):
        sys.stderr.write('No write access to directory: %s\n'%(dirPath))
        return -1

  # Now good to go
  wBytes = 0
  with open(path, 'wb' if isBinary else 'w') as f:
    wBytes = f.write(data)

  return wBytes
