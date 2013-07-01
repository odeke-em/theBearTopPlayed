#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

RANKS_STORAGE = 'ranks.rk'
import sys, subprocess
from optparse import OptionParser
from time import sleep, ctime, time

import thebear

def cliParser():
  parser = OptionParser()
  parser.add_option( '-t','--timeout',dest='timeout',
    help="Set the timeout in minutes between database updates", default=1 )
  parser.add_option( '-d', '--displayranks', dest='displayranks',
    help="Set whether to print out ranks every after a data collection", 
    default=True,action="store_false" )
  args,options = parser.parse_args()
  return args,options

def updateDb( timeout_mins, PRINT_RANKS=True ):
  assert( hasattr( timeout_mins, '__divmod__' )) #Either a float or int
  updateRunning = True
  tSleep_secs = timeout_mins*60
  while updateRunning:
    try:
      ranksCompiled = thebear.main()
      if ( not PRINT_RANKS ):
        sys.stderr.write( "\033[31m\nSince boolean 'PRINT_RANKS' is set to False, ranks " )
        sys.stderr.write("will not be printed to the screen after every retrival\n\033[00m")
      f = open( RANKS_STORAGE, 'w' )
      f.write( ranksCompiled )
      f.flush()
      f.close()
      sys.stderr.write( "Ranks written to file: '%s'\n"%( RANKS_STORAGE ))
    except KeyboardInterrupt as e:
      print( "Exiting....." )
      updateRunning=False
    else:
      if ( PRINT_RANKS ):
          print( ranksCompiled )
      curTimeSecs = time()
      nextUpdateAt = curTimeSecs + tSleep_secs
      nextTimeStr  = ctime( nextUpdateAt )
      print( "Sleeping for %d seconds next update at: %s"%( tSleep_secs ,
        nextTimeStr ))
      sleep( tSleep_secs )
  
if __name__ == '__main__':
  args,options = cliParser()
  try:
    secTimeout  = int( args.timeout )
    PRINT_RANKS = bool( args.displayranks )
  except ValueError as e:
    print( "Timeout must be an integer" )
  updateDb( secTimeout, PRINT_RANKS )
