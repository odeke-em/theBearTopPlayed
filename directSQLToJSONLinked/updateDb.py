#!/usr/bin/env python
# Author: Emmanuel Odeke <odeke@ualberta.ca>

import os, sys, re, subprocess
from time import sleep, ctime, time

import thebear
import resources
from parser import cliParser

RANKS_STORAGE = resources.RANKS_DUMP_PATH

def supportsRfKill():
  return os.uname()[0] in ['Linux']

def updateDb(timeout_mins, PRINT_RANKS_BOOL=True):
  # Calls module 'thebear.main' and prints ranks retrieved if 'PRINT_RANKS'
  #  is set. Sleeps for a 'timeout_mins' interval, and refreshes
  # Input: timeout_mins -> Unsigned value(float/int) in minutes for which 
  #               script will sleep before refreshing.
  #       PRINT_RANKS_BOOL(Optional) -> Boolean to determine if ranks retrieved
  #                       on every refresh will be written to standard output
  # Returns: None
  assert(hasattr(timeout_mins, '__divmod__')) #Only either a float or int
  updateRunning = True
  iterationCount = 0

  while updateRunning:
    try:
      ranksCompiled = thebear.main() # Retrieve the ranks

      if not ranksCompiled:
        sys.stderr.write("Failed to retrieve ranks.\n")

        sleepBeforeRefresh(timeout_mins)
        continue

      if not PRINT_RANKS_BOOL:
        sys.stderr.write(
           "\033[33m\nSince boolean 'PRINT_RANKS' is set to False, ranks "+\
           "will not be printed to the screen after every retrival\n\033[00m"
        )

      res = resources.delegateFileWriting(RANKS_STORAGE, ranksCompiled)

      iterationCount += 1
      sys.stderr.write("IterationCount: %d\n"%(iterationCount))

      if res >= 1:
        sys.stderr.write("\033[92mRanks written to file: '%s'\033[00m\n"%(RANKS_STORAGE))
      else:
        sys.stderr.write("\033[91mFailed to write ranks to file: '%s'\033[00m\n"%(RANKS_STORAGE))

      if (PRINT_RANKS_BOOL):
          print(ranksCompiled)
      sleepBeforeRefresh(timeout_mins)

    except KeyboardInterrupt as e:
      # status,output = subprocess.getstatusoutput(wifiManage('unblock'))
      print("Ctrl-C applied. Exiting...")
      updateRunning=False
  # return iterationCount

# Returns arguments for function to kill/turnon wifi for the sleep duration
# Args: 'up' or 'down'
wifiManage = lambda sigValue : 'rfkill %s wifi'%(sigValue)

def sleepBeforeRefresh(timeout_mins,BRUTE_WINDOW_PROTECTION=True):
   # Sleep for the requested minutes
   # Input: 'timeout_mins' -> unsigned value [float, int] in minutes to sleep for
   # Output: None
   assert(hasattr(timeout_mins, '__divmod__')) #Only either a float or int
   tSleep_secs = timeout_mins * 60 #Sleep time converted to seconds

   # Get the current time in seconds since the epoch
   curTimeSecs = time()

   # Calculate the time for next update, to be displayed to screen
   nextUpdateAt = curTimeSecs + tSleep_secs

   # Convert the next update time to a string in local time
   nextTimeStr  = ctime(nextUpdateAt)

   print("Sleeping for %d seconds. Next update at: %s"%(tSleep_secs ,
        nextTimeStr))
   '''
   # Kill the wifi to prevent brute-force attacks once the system is idle and exposed
   # Only Linux based solution
   WIFI_BLOCKED = False
   if BRUTE_WINDOW_PROTECTION and supportsRfKill():
      status,output = subprocess.getstatusoutput(wifiManage('block'))
      print("Blocked wifi")
      WIFI_BLOCKED = (status == 0)

   sleep(tSleep_secs)
   Turn the wifi back on
   status,output = subprocess.getstatusoutput(wifiManage('unblock'))
   WIFI_BLOCKED = ~(status == 0)
   print("UnBlocked wifi")
   '''
   sleep(tSleep_secs)

if __name__ == '__main__':
  args,options = cliParser()
  try:
    timeout_value = str(args.timeout)

    if (re.search('^(\d+)(\.\d+)?$',timeout_value)):
      secTimeOut = float(timeout_value)

    else: raise ValueError("Timeout must be an integer or a simple float\n")

    PRINT_RANKS_BOOL = bool(args.displayranks)

  except ValueError as e:
    sys.stderr.write(e.__str__())
    # status,output = subprocess.getstatusoutput(wifiManage('unblock'))

  else:
    updateDb(secTimeOut, PRINT_RANKS_BOOL)
