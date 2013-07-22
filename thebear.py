#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re, sys, sqlite3

from hashlib import md5

#Local modules
import sitereader
import createDb
import convDate 
<<<<<<< HEAD
import resources
=======

#Path for database
dbPath = "songDatabase.db" 
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

###############################PATTERNS_AND_REGEXS##############################
BEAR_ROCKS_URL="http://www.thebearrocks.com/broadcasthistory.aspx"

dateStampRegex = \
 r'<option selected="selected" value="(\d+/\d+/\d{4})">(\d+/\d+/\d{4})</option>'
timeStampRegex   = r'(\d?:?\d+:\d+\s[AP]?M)'
linkTitleRegex   = r'<a href="(.*)" title="(.*)-(.*)">'

<<<<<<< HEAD
timeStampCompile = re.compile(timeStampRegex)
linkTitleCompile = re.compile(linkTitleRegex)
dateStampCompile = re.compile(dateStampRegex)

trStartCompile = re.compile(r'<tr class=\'.*\'>')
trEndCompile = re.compile(r'</tr>')

#Selection Date should be changed in submission to match the target selection
selectionDateRegex = r'<option (value||selected)="(\d+/){3}">'
selectDateCompile = re.compile(selectionDateRegex)
###############################################################################

def ripTrackInfo(tdList, dateOfTrack):
  #Input: tdList -> A list of xml-lines with potential song info
=======
timeStampCompile = re.compile( timeStampRegex )
linkTitleCompile = re.compile( linkTitleRegex )
dateStampCompile = re.compile( dateStampRegex )

trStartCompile = re.compile( r'<tr class=\'.*\'>' )
trEndCompile = re.compile( r'</tr>' )

#Selection Date should be changed in submission to match the target selection
selectionDateRegex = r'<option (value||selected)="(\d+/){3}">'
selectDateCompile = re.compile( selectionDateRegex )
###############################################################################

def ripTrackInfo( tdList, dateOfTrack ):
  #Input: tdList ->#List containing the data affixed between <td> html tags
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  #       dateOfTrack -> dd/mm/yyyy string
  #Returns: 
  #        if successful: 
  #           'artistName', 'songTitle',
<<<<<<< HEAD
  #           'trackHash' -> md5 sum of the song's name,
=======
  #           'trackHash' -> md5 sum of the song's title,
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  #           'secondsString'-> string of seconds since the epoch in reference 
  #                             to the time that the song was reported played
  #        else: None 
  artist = songTitle = timeStamp = None
<<<<<<< HEAD
  while tdList:
    line = tdList.pop(0)

    #Remove/Replace the special xml symbols
    line = re.sub('&quot;|&#39;', '',line)
    line = re.sub('&amp;', '&',line)

    timeStampSearch = timeStampCompile.search(line)
    linkTitleSearch = linkTitleCompile.search(line)

    if timeStampSearch:
      timeStamp = timeStampSearch.groups(1)[0]

    if linkTitleSearch:
      songUrl, songTitle, artist = linkTitleSearch.groups(1)

  if (artist and songTitle and timeStamp):
    dateInt = convDate.concatDate(timeStamp, dateOfTrack)

    trackHash = md5(bytes(songTitle, 'utf-8')).hexdigest()

    return artist, songTitle, trackHash, str(dateInt), songUrl

def main():
  #Input: None
  #Description: Makes a request to theBearRocks url and parses the data, creating
  #ranks that are returned.
  #Returns:  Data from theBearRocks url or None if retrieval failed
  data = sitereader.site_opener(
    BEAR_ROCKS_URL, stderr=sys.stderr, errorVerbosity=True)
=======
  while tdList: 
    line = tdList.pop(0)

    #Remove/Replace the special xml symbols
    line = re.sub('&quot;|&#39', '',line )
    line = re.sub('&amp;', '&',line )

    timeStampSearch = timeStampCompile.search( line )
    linkTitleSearch = linkTitleCompile.search( line )

    if timeStampSearch:
      timeStamp = timeStampSearch.groups( 1 )[0]

    if linkTitleSearch:
      songUrl, songTitle, artist = linkTitleSearch.groups( 1 )

  if ( artist and songTitle and timeStamp ):
    convertedSeconds = convDate.mdy_date_to_Int( timeStamp, dateOfTrack )

    if ( convertedSeconds == -1 ): #Corrupted date here
      return None

    trackHash = md5( bytes( songTitle, 'utf-8' )).hexdigest()

    return artist, songTitle, trackHash, str( convertedSeconds )

def main():
  #Input: None
  #Description: Makes a request to theBearRocks url and parses the data, 
  #creating ranks that are returned as a string.
  
  #Returns:  Data from theBearRocks url or None if retrieval failed
  data = sitereader.site_opener( 
    BEAR_ROCKS_URL, stderr=sys.stderr, errorVerbosity=True )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  
  if not data: 
    sys.stderr.write("\n\t\033[31mFailed to retrieve data from %s. "%(
                  BEAR_ROCKS_URL))
    sys.stderr.write("Check the url or the script's regular expressions\n")
    sys.stderr.write("may have also changed\033[00m\n")

    return None

<<<<<<< HEAD
  sys.stderr.write(
   "\033[32mNote: \n\tStep by step info is printed to standard error ")
  sys.stderr.write(
   "and cannot be redirected to a file. \n\tRanks produced however, ")
  sys.stderr.write("can be redirected to file: ranks.rk\033[00m\n\n")
  sys.stderr.write("Retrieving data from %s\n"%(BEAR_ROCKS_URL))
  sys.stderr.write("Data retrieved from the web....\n")

  #Taking out all tabs and carriage returns
  data = re.sub('[\t\r]', '', data) 

  dateStampFindall = dateStampCompile.findall(data)
=======
  sys.stderr.write( 
   "\033[32mNote: \n\tStep by step info is printed to standard error " )
  sys.stderr.write( 
   "and cannot be redirected to a file. \n\tRanks produced however, " )
  sys.stderr.write( "can be redirected to file: ranks.rk\033[00m\n\n" )
  sys.stderr.write( "Retrieving data from %s\n"%( BEAR_ROCKS_URL ))
  sys.stderr.write( "Data retrieved from the web....\n" )

  #Taking out all tabs and carriage returns
  data = re.sub( '[\t\r]', '', data ) 

  dateStampFindall = dateStampCompile.findall( data )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
  dateInTag,dateDisplayed = dateStampFindall[0]

  #The date displayed in the tag as the selected date must match that displayed
  #else the data is corrupted
<<<<<<< HEAD
  assert(dateInTag == dateDisplayed)
  sys.stderr.write(
   "Timestamp from url of data retrieved: %s\n"%(dateDisplayed))
  data = data.split('\n')
=======
  assert( dateInTag == dateDisplayed )

  sys.stderr.write( 
   "Timestamp from url of data retrieved: %s\n"%( dateDisplayed ))
  data = data.split( '\n' )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

  fullTrs = []
  
  while data:
    line = data.pop(0)
<<<<<<< HEAD
    if (trStartCompile.search(line)):
      fullTr = []
      while data and (not trEndCompile.search(line)):
=======
    if ( trStartCompile.search( line )):
      fullTr = []
      while data and ( not trEndCompile.search( line )):
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90
        line = data.pop(0)
        fullTr += [ line ]
      fullTrs += [ fullTr ]

<<<<<<< HEAD
  sys.stderr.write("\nConnecting to storage Database %s ....\n"%(resources.dbPath))
  conn,cursor = createDb.getConCursor(resources.dbPath)
  sys.stderr.write("Connection to the database successful\n")

  sys.stderr.write(
  "\nParsing and extracting data to retrieve artist, songtitle and playTimes\n"   )
  for tr in fullTrs:
    songParams = ripTrackInfo(tr, dateDisplayed)
    if not songParams:
        continue;  

    createDb.addEntry('songs', songParams, cursor)
  try:
    conn.commit() #Save changes
  except sqlite3.OperationalError as e:
    sys.stderr.write(
     "Failed to  commit changes to the database. Exiting...\n")
    sys.exit(-2)
  else:
    sys.stderr.write("Changes committed to the database\n\n")
  #rankQuery = input("Would you like to see the ranks for the data retrieved? (y/n) ")
  #if re.search('[yY]+', rankQuery):
  #  print(rankTracks(cursor))
  compiledRanks = createDb.rankTracks(cursor)
  conn.close()
  sys.stderr.write("\nBye...\n")
=======
  sys.stderr.write( "\nConnecting to storage Database %s ....\n"%( dbPath ))
  conn,cursor = createDb.getConCursor( dbPath )
  sys.stderr.write( "Connection to the database successful\n" )

  sys.stderr.write( 
  "\nParsing and extracting data to retrieve artist, songtitle and playTimes\n"   )
  for tr in fullTrs:
    songParams = ripTrackInfo( tr, dateDisplayed )
    if not songParams:
        continue;  

    #'songs' is the name of the source table in the database
    createDb.addEntry( 'songs', songParams, cursor )
  try:
    conn.commit() #Save changes
  except sqlite3.OperationalError as e:
    sys.stderr.write( 
     "Failed to  commit changes to the database. Exiting...\n" )
    sys.exit( -2 )
  else:
    sys.stderr.write( "Changes committed to the database\n\n" )
  #printRanksQuery = input( "Would you like to see the ranks for the data retrieved? (y/n) " )
  #if re.search( '[yY]+', printRanksQuery ):
  #  print( rankTracks( cursor ))

  compiledRanks = createDb.rankTracks( cursor )

  conn.close() #Close our database
  sys.stderr.write( "\nBye...\n" )
>>>>>>> d726d7deb3a82fd599172344699dbe98561a6e90

  return compiledRanks

if __name__ == '__main__':
  main()
