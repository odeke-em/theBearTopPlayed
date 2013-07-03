#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>


import sys, re
from optparse import OptionParser
from time import sleep, ctime, time

import thebear

RANKS_STORAGE = 'ranks.rk' #File to which retrieved ranks will be written

def cliParser():
  #Input: None
  #Returns: parser for updateDb
  parser = OptionParser()
  parser.add_option( '-t','--timeout',dest='timeout',
    help="Set the timeout in minutes between database updates", default=1 )
  parser.add_option( '-d', '--displayranks', dest='displayranks',
    help="Set whether to print out ranks every after a data collection", 
    default=True,action="store_false" )
  args,options = parser.parse_args()
  return args,options

def updateDb( timeout_mins, PRINT_RANKS_BOOL=True ):
  #Calls module 'thebear.main' and prints ranks retrieved if 'PRINT_RANKS'
  # is set. Sleeps for a 'timeout_mins' interval, and refreshes
  #Input: timeout_mins -> Unsigned value(float/int) in minutes for which 
  #              script will sleep before refreshing.
  #      PRINT_RANKS_BOOL(Optional) -> Boolean to determine if ranks retrieved
  #                       on every refresh will be written to standard output
  #Returns: None
  assert( hasattr( timeout_mins, '__divmod__' )) #Only either a float or int
  updateRunning = True

  while updateRunning:
    try:
      ranksCompiled = thebear.main() #Retrieve the ranks

      if (not ranksCompiled): #Notify user of failed attempt to get ranks
        sys.stderr.write("Failed to retrieve ranks.")

        sleepBeforeRefresh(timeout_mins) #Sleep and then try again
        continue 

      if ( not PRINT_RANKS_BOOL ): #Notify user if ranks will not be printed to
                              #standard output
        sys.stderr.write( 
           "\033[33m\nSince boolean 'PRINT_RANKS' is set to False, ranks " )
        sys.stderr.write(
           "will not be printed to the screen after every retrival\n\033[00m")

      #Write the ranks to file
      f = open( RANKS_STORAGE, 'w' )
      f.write( ranksCompiled )
      f.flush()
      f.close()

      #Notify that the ranks have been written to file
      sys.stderr.write( "Ranks written to file: '%s'\n"%( RANKS_STORAGE ))

      if ( PRINT_RANKS_BOOL ):
          print( ranksCompiled )

      sleepBeforeRefresh(timeout_mins)

    except KeyboardInterrupt as e:
      print( "Ctrl-C applied. Exiting..." )
      updateRunning=False

def sleepBeforeRefresh(timeout_mins):
   #Sleep for the requested minutes
   #Input: 'timeout_mins' -> unsigned value (float/int) in minutes to sleep for
   #Output: None
   assert( hasattr( timeout_mins, '__divmod__' )) #Only either a float or int
   tSleep_secs = timeout_mins*60 #Sleep time converted to seconds

   #Get the current time in seconds since the epoch
   curTimeSecs = time() 

   #Calculate the time for next update, to be displayed to screen
   nextUpdateAt = curTimeSecs + tSleep_secs

   #Convert the next update time to a string in local time
   nextTimeStr  = ctime( nextUpdateAt )

   print( "Sleeping for %d seconds. Next update at: %s"%( tSleep_secs ,
        nextTimeStr ))

   sleep( tSleep_secs )

if __name__ == '__main__':
  args,options = cliParser()
  try:
    timeout_value = str(args.timeout)
    if ( re.search('^(\d+)$',timeout_value)): secTimeOut = int(timeout_value)
      
    elif ( re.search('^(\d+\.\d+)$',timeout_value)): 
      secTimeOut = float(timeout_value)
      
    else: raise ValueError("Timeout must be either an integer or float\n")

    PRINT_RANKS_BOOL = bool(args.displayranks)

  except ValueError as e:
    sys.stderr.write(e.__str__())

  else:
    updateDb( secTimeOut, PRINT_RANKS_BOOL )
