#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re, sys

from hashlib import md5

from sitereader import *
from createDb import *
import convDate 
###############################PATTERNS_AND_REGEXS#############################
BEAR_ROCKS_URL="http://www.thebearrocks.com/broadcasthistory.aspx"
dateStampRegex  = r'<option selected="selected" value="(\d+/\d+/\d\d\d\d)">(\d+/\d+/\d\d\d\d)</option>'
timeStampRegex   = r'(\d?:?\d+:\d+\s[AP]?M)'
linkTitleRegex   = r'<a href="(.*)" title="(.*)-(.*)">'

timeStampCompile = re.compile( timeStampRegex )
linkTitleCompile = re.compile( linkTitleRegex )
dateStampCompile = re.compile( dateStampRegex )

trStartCompile = re.compile( r'<tr class=\'.*\'>' )
trEndCompile = re.compile( r'</tr>' )

#Selection Date should be changed in submission to match the target selection
selectionDateRegex = r'<option (value||selected)="(\d+/\d+/\d+)">'
selectDateCompile = re.compile( selectionDateRegex )
###############################################################################
def ripTrackInfo( tdList, dateOfTrack ):
  artist = songTitle = timeStamp = None
  while tdList:
    line = tdList.pop(0)
    line = line.replace( '&quot;', '' )
    line = line.replace( '&amp;', '&' )
    line = line.replace( '&#39;', '' )

    timeStampSearch = timeStampCompile.search( line )
    linkTitleSearch = linkTitleCompile.search( line )
    if timeStampSearch:
      timeStamp = timeStampSearch.groups( 1 )[0]
    if linkTitleSearch:
      songUrl, songTitle, artist = linkTitleSearch.groups( 1 )
  if ( artist and songTitle and timeStamp ):
    dateInt = convDate.mdy_date_to_Int( timeStamp, dateOfTrack )
    #songObj = SongObj( artist, songTitle, entryTime=timeStamp )
    trackHash = md5( bytes( songTitle, 'utf-8' )).hexdigest()
    return artist, songTitle, trackHash, str( dateInt )

def main():
  sys.stderr.write( "\033[32mNote: \n\tStep by step info is printed to standard error " )
  sys.stderr.write( "and cannot be redirected to a file. \n\tRanks produced however, " )
  sys.stderr.write( "can be redirected to file: ranks.rk\033[00m\n\n" )
  sys.stderr.write( "Retrieving data from %s\n"%( BEAR_ROCKS_URL ))
  dbPath = "songDatabase.db" 
  data = site_opener( BEAR_ROCKS_URL, sys.stderr, True )
  sys.stderr.write( "Data retrieved from the web....\n" )
  
  data = re.sub( '[\t\r]', '', data )

  dateStampFindall = dateStampCompile.findall( data )
  dateInTag,dateDisplayed = dateStampFindall[0]

  #The date displayed in the tag as the selected date must match that displayed, else the data is corrupted
  assert( dateInTag == dateDisplayed )
  sys.stderr.write( "Timestamp from url of data retrieved: %s\n"%( dateDisplayed ))
  data = data.split( '\n' )
  songObjs = []
  fullTrs = []
  #sys.stderr.write( createTable( 'songs', cur )) # == TABLE_CREATED  
  
  while data:
    line = data.pop(0)
    if ( trStartCompile.search( line )):
      fullTr = []
      while data and ( not trEndCompile.search( line )):
        line = data.pop(0)
        fullTr += [ line ]
      fullTrs += [ fullTr ]

  sys.stderr.write( "\nConnecting to storage Database %s ....\n"%( dbPath ))
  conn,cursor = getConCursor( dbPath )
  sys.stderr.write( "Connection to the database successful\n" )

  sys.stderr.write( "\nParsing and extracting data to retrieve artist, songtitle and playTimes\n" )
  for tr in fullTrs:
    songParams = ripTrackInfo( tr, dateDisplayed )
    if not songParams:
        continue;  

    addEntry( 'songs', songParams, cursor )
  try:
    conn.commit() #Save changes
  except OperationalError as e:
    sys.stderr.write( "Failed to  commit changes to the database. Exiting...\n" )
    sys.exit( -2 )
  else:
    sys.stderr.write( "Changes committed to the database\n\n" )
  #rankQuery = input( "Would you like to see the ranks for the data retrieved? (y/n) " )
  #if re.search( '[yY]+', rankQuery ):
  #  print( rankTracks( cursor ))
  compiledRanks = rankTracks( cursor )
  conn.close()
  sys.stderr.write( "\nBye...\n" )
  return compiledRanks

if __name__ == '__main__':
  main()
