#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

<<<<<<< HEAD

import sys, re, subprocess
=======
import sys, re
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
from optparse import OptionParser
from time import sleep, ctime, time

import thebear

RANKS_STORAGE = 'ranks.rk' #File to which retrieved ranks will be written

def cliParser():
  #Input: None
  #Returns: parser for updateDb
  parser = OptionParser()
<<<<<<< HEAD
  parser.add_option('-t','--timeout',dest='timeout',
    help="Set the timeout in minutes between database updates", default=1)
  parser.add_option('-d', '--displayranks', dest='displayranks',
    help="Set whether to print out ranks every after a data collection", 
    default=True,action="store_false")
  args,options = parser.parse_args()
  return args,options

def updateDb(timeout_mins, PRINT_RANKS_BOOL=True):
  #Calls module 'thebear.main' and prints ranks retrieved if 'PRINT_RANKS'
  # is set. Sleeps for a 'timeout_mins' interval, and refreshes
=======
  parser.add_option( '-t','--timeout',dest='timeout',
    help="Set the timeout in minutes between database updates", default=1 )
  parser.add_option( '-d', '--displayranks', dest='displayranks',
    help="Set whether to print out ranks every after a data collection", 
    default=True,action="store_false" )
  args,options = parser.parse_args()
  return args,options

def updateDb( timeout_mins, PRINT_RANKS_BOOL=True ):
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  #Input: timeout_mins -> Unsigned value(float/int) in minutes for which 
  #              script will sleep before refreshing.
  #      PRINT_RANKS_BOOL(Optional) -> Boolean to determine if ranks retrieved
  #                       on every refresh will be written to standard output
<<<<<<< HEAD
  #Returns: None
  assert(hasattr(timeout_mins, '__divmod__')) #Only either a float or int
=======
  #
  #Calls module 'thebear.main' and prints ranks retrieved if 'PRINT_RANKS'
  # is set. Sleeps for a 'timeout_mins' interval, and refreshes
  #
  #Returns: None

  assert( hasattr( timeout_mins, '__divmod__' )) #Only either a float or int
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  updateRunning = True

  while updateRunning:
    try:
      ranksCompiled = thebear.main() #Retrieve the ranks

      if (not ranksCompiled): #Notify user of failed attempt to get ranks
<<<<<<< HEAD
        sys.stderr.write("Failed to retrieve ranks.\n")
=======
        sys.stderr.write("Failed to retrieve ranks.")
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

        sleepBeforeRefresh(timeout_mins) #Sleep and then try again
        continue 

<<<<<<< HEAD
      if (not PRINT_RANKS_BOOL): #Notify user if ranks will not be printed to
                              #standard output
        sys.stderr.write(
           "\033[33m\nSince boolean 'PRINT_RANKS' is set to False, ranks ")
=======
      if ( not PRINT_RANKS_BOOL ): #Notify user if ranks will not be printed to
                              #standard output
        sys.stderr.write( 
           "\033[33m\nSince boolean 'PRINT_RANKS' is set to False, ranks " )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
        sys.stderr.write(
           "will not be printed to the screen after every retrival\n\033[00m")

      #Write the ranks to file
<<<<<<< HEAD
      f = open(RANKS_STORAGE, 'w')
      f.write(ranksCompiled)
=======
      f = open( RANKS_STORAGE, 'w' )
      f.write( ranksCompiled )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
      f.flush()
      f.close()

      #Notify that the ranks have been written to file
<<<<<<< HEAD
      sys.stderr.write("Ranks written to file: '%s'\n"%(RANKS_STORAGE))

      if (PRINT_RANKS_BOOL):
          print(ranksCompiled)
=======
      sys.stderr.write( "Ranks written to file: '%s'\n"%( RANKS_STORAGE ))

      if ( PRINT_RANKS_BOOL ):
          print( ranksCompiled )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

      sleepBeforeRefresh(timeout_mins)

    except KeyboardInterrupt as e:
<<<<<<< HEAD
      #status,output = subprocess.getstatusoutput(wifiManage('unblock'))
      print("Ctrl-C applied. Exiting...")
      updateRunning=False

#Returns arguments for function to kill/turnon wifi for the sleep duration
#Args: 'up' or 'down'
wifiManage = lambda sigValue : 'rfkill %s wifi'%(sigValue)

def sleepBeforeRefresh(timeout_mins,BRUTE_WINDOW_PROTECTION=True):
   #Sleep for the requested minutes
   #Input: 'timeout_mins' -> unsigned value (float/int) in minutes to sleep for
   #Output: None
   assert(hasattr(timeout_mins, '__divmod__')) #Only either a float or int
=======
      print( "Ctrl-C applied. Exiting..." )
      updateRunning=False

def sleepBeforeRefresh(timeout_mins):
   #Sleep for the requested minutes
   #Input: 'timeout_mins' -> unsigned value (float/int) in minutes to sleep for
   #Output: None
   assert( hasattr( timeout_mins, '__divmod__' )) #Only either a float or int
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
   tSleep_secs = timeout_mins*60 #Sleep time converted to seconds

   #Get the current time in seconds since the epoch
   curTimeSecs = time() 

   #Calculate the time for next update, to be displayed to screen
   nextUpdateAt = curTimeSecs + tSleep_secs

   #Convert the next update time to a string in local time
<<<<<<< HEAD
   nextTimeStr  = ctime(nextUpdateAt)

   print("Sleeping for %d seconds. Next update at: %s"%(tSleep_secs ,
        nextTimeStr))
   #First kill the wifi to prevent brute-force attacks
   #WIFI_BLOCKED = False
   #if BRUTE_WINDOW_PROTECTION:
      #status,output = subprocess.getstatusoutput(wifiManage('block'))
      #print("Blocked wifi")
      #WIFI_BLOCKED = (status == 0)
   sleep(tSleep_secs)
   #Turn the wifi back on
   #status,output = subprocess.getstatusoutput(wifiManage('unblock'))
   #WIFI_BLOCKED = ~(status == 0)
   #print("UnBlocked wifi")
   sleep(1)
=======
   nextTimeStr  = ctime( nextUpdateAt )

   print( "Sleeping for %d seconds. Next update at: %s"%( tSleep_secs ,
        nextTimeStr ))

   sleep( tSleep_secs )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

if __name__ == '__main__':
  args,options = cliParser()
  try:
    timeout_value = str(args.timeout)
<<<<<<< HEAD
    if (re.search('^(\d+)$',timeout_value)): secTimeOut = int(timeout_value)
      
    elif (re.search('^(\d+\.\d+)$',timeout_value)): 
=======
    if ( re.search('^(\d+)$',timeout_value)): secTimeOut = int(timeout_value)
      
    elif ( re.search('^(\d+\.\d+)$',timeout_value)): 
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
      secTimeOut = float(timeout_value)
      
    else: raise ValueError("Timeout must be either an integer or float\n")

    PRINT_RANKS_BOOL = bool(args.displayranks)

  except ValueError as e:
    sys.stderr.write(e.__str__())
<<<<<<< HEAD
    #status,output = subprocess.getstatusoutput(wifiManage('unblock'))

  else:
    updateDb(secTimeOut, PRINT_RANKS_BOOL)
=======

  else:
    updateDb( secTimeOut, PRINT_RANKS_BOOL )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
