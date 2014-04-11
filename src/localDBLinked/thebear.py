#!/usr/bin/env python
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re, sys, sqlite3

from hashlib import md5

#Local modules
import sitereader
import createDb
import convDate
import resources as rscs

###############################PATTERNS_AND_REGEXS##############################
BEAR_ROCKS_URL="http://www.thebearrocks.com/broadcasthistory.aspx"

dateStampRegex = \
 r'<option selected="selected" value="(\d+/\d+/\d{4})">(\d+/\d+/\d{4})</option>'
timeStampRegex   = r'(\d?:?\d+:\d+\s[AP]?M)'
linkTitleRegex   = r'<a href="(.*)" title="(.*)-(.*)">'

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
  #       dateOfTrack -> dd/mm/yyyy string
  #Returns: 
  #        if successful: 
  #           'artistName', 'songTitle',
  #           'trackHash' -> md5 sum of the song's name,
  #           'secondsString'-> string of seconds since the epoch in reference 
  #                             to the time that the song was reported played
  #        else: None 
  artist = songTitle = timeStamp = None
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

    trackHash = md5(bytes(songTitle, *rscs.byteEncodingArgs)).hexdigest()

    return artist, songTitle, trackHash, str(dateInt), songUrl

def main():
  #Input: None
  #Description: Makes a request to theBearRocks url and parses the data, creating
  #ranks that are returned.
  #Returns:  Data from theBearRocks url or None if retrieval failed
  data = sitereader.site_opener(
    BEAR_ROCKS_URL, stderr=sys.stderr, errorVerbosity=True)

  if not data:
    sys.stderr.write("\n\t\033[31mFailed to retrieve data from %s. "%(
                  BEAR_ROCKS_URL))
    sys.stderr.write("Check the url or the script's regular expressions\n")
    sys.stderr.write("may have also changed\033[00m\n")

    return None

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
  dateInTag,dateDisplayed = dateStampFindall[0]

  #The date displayed in the tag as the selected date must match that displayed
  #else the data is corrupted
  assert(dateInTag == dateDisplayed)
  sys.stderr.write(
   "Timestamp from url of data retrieved: %s\n"%(dateDisplayed))
  data = data.split('\n')

  fullTrs = []

  while data:
    line = data.pop(0)
    if (trStartCompile.search(line)):
      fullTr = []
   
      while data and (not trEndCompile.search(line)):
        line = data.pop(0)
        fullTr += [line]
      fullTrs += [fullTr]

  sys.stderr.write("\nConnecting to storage Database %s ....\n"%(rscs.dbPath))
  conn,cursor = createDb.getConCursor(rscs.dbPath)

  if not (conn and cursor):
    sys.stderr.write("Connection to the database unsuccessful\n")
    return None

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

  return compiledRanks

if __name__ == '__main__':
  main()
