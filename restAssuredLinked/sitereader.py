#!/usr/bin/env python3
'''
  Author: Emmanuel Odeke <odeke@ualberta.ca>
   Module to retrieve data from url, using a customized user agent.
   Logs to standard error stream(if defined) any errors encountered.
'''

import re
import resources as rscs #  Local module

def site_opener(url, stderr,errorVerbosity, user_agent=rscs.UBUNTU_UAGENT):
  # Input: url->string, stderr -> file stream to log errors, 
  #        errorVerbosity ->Boolean to determine if
  #         any errors and excepts can be logged to standard error
  # Output: Logs to stderr errors if boolean 'errorVerbosity' is set
  # Returns: Retrieved data retrieved  or None on failure
  # Make sure that the stream passed in as the standard error, can be written to
  #  and flushed else throw an exception
  if (not (hasattr(stderr,'write') and hasattr(stderr,'flush'))): 
    raise Exception("The standard error stream needs to have methods 'write'"+\
                    " and 'flush' defined")

  try:
    # Building our modified url opener to enable the use of a fake user-agent
    modified_opener   = rscs.urlRequester.build_opener()
    user_agent_tuple = ('user-agent', user_agent)
    modified_opener.addheaders = [user_agent_tuple]

    data = modified_opener.open(url) # Use the modified url opener to open url
  except Exception as e:
    print(e)
    if (errorVerbosity): # Log the error to std
      # Possibly corrupted url or no internet connectionerr
      if (isinstance(e, rscs.URLError)): 
        errMsg = "Unknown service %s or check your Internet connection"%(url)
      else:
        errMsg = "While opening url '%s' error: %s encountered"%(url, e.__str__())

      stderr.write("\033[31m%s\033[00m\n"%(errMsg))
      stderr.flush()
    return None

  try:
    outdata = data.read()
    # Try decoding the data
    decoded_data = outdata.decode() if rscs.pyVersion > 3 else outdata.decode('utf-8')
  except Exception as e:
    # Manage error later# 
    if (errorVerbosity):
      stderr.write("Decoding error: errorBelow: %s\n"%(e.__str__()))
      stderr.flush()
    return None
  else: return decoded_data
