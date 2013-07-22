#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import sys, re

from os import stat, path
from time import ctime, time
from sqlite3 import connect, OperationalError

import mover
import resources
import createJSON

###################################CONSTANTS###################################
TABLE_ALREADY_EXISTS = 0xf
TABLE_CREATED = (~TABLE_ALREADY_EXISTS)

#Retrieving the current module's file name
current_file_search = re.search('.*/(\w+\.py)$',__file__)
if current_file_search:
  current_file_name = current_file_search.groups(1)[0]
else: #Hard coded value here
  current_file_name = 'createDb.py'
###############################################################################

def create_monitor_time_src(endPeriodSecs=604800):#1 week of monitoring
  #This creates the file from which the first database creation date is stored
  #This date is essential to keep tracking of when track-monitoring began
  curTimeSecs = time()
  endTimeSecs = curTimeSecs+endPeriodSecs

  if (curTimeSecs >= endTimeSecs):
    sys.stderr.write(
    "\033[31mTime to end monitoring has to be greater than 0\033[00m\n")
    sys.exit(-2)

  MONITOR_START_SOURCE = "monitor_start.py"
  sDate = open(MONITOR_START_SOURCE,'w')
  sDate.write('#This file was auto-generated by %s\n'%(current_file_name))
  sDate.write(
    'MONITOR_START_DATE = (%s,"%s")\n'%(curTimeSecs,ctime(curTimeSecs))
  )
  sDate.write('MONITOR_END_DATE = (%s,"%s")\n'%(endTimeSecs,ctime(endTimeSecs)))
  sDate.flush()
  sDate.close()

def checkTableName(tableName):
  #Given a table name, check if it is single word else throw an Exception

  #Table name should be a single word consisting only of characters and/or 
  #numbers
  if (re.search('[^\w\d]',tableName) or (not tableName)):
   raise Exception("Invalid table name or potential injection detected")
   
def getConCursor(dbPath):
  #Create the storage database if none existant, and log 
  #the start date of monitoring
  if (not path.exists(dbPath)):
    create_monitor_time_src(20) #Kick off period monitoring
    f = open(dbPath, "w")
    f.close()

  conn = connect(dbPath) 
  cur  = conn.cursor()
  #Creates the custom function that will be used to query the songsTable name
  #It takes in one parameter

  #Querying if the table exists
  cur.execute(
    "select name from sqlite_master where type='table' and name='songs'")
  tableNameQuery = cur.fetchone()

  if (not tableNameQuery):#Create the table if it doesn't exist
   if (createTable('songs', conn) == TABLE_ALREADY_EXISTS):
     #Potential conflict/error detected here, handle
     sys.stderr.write("Could not create the SQL table, but it was reported")
     sys.stderr.write(" as already created\n")
     sys.exit(-2)
     
  return conn, cur

def createTable(tableName, connection):
  #Input: tableName ->String for the table name to be created
  #        connection object
  #Returns: status to signify if the table was created or if it existed already

  #Check if we were given a valid tableName which should consist only of letters
  #and/or numbers: Else an Exception is thrown
  
  checkTableName(tableName)

  try:
    CREATE_TABLE_CMD = \
     "CREATE TABLE %s(artist text,title text,trackHash text,url text,playTimes text)"%(
      tableName)
    connection.execute(CREATE_TABLE_CMD)
     
    connection.commit() #Commit to memory, the newly made change

  except OperationalError as e:
    return TABLE_ALREADY_EXISTS

  else:
    return TABLE_CREATED

def lookupQuery(title, artist, cursor):
  #Input: Query parameters: title,artist. Cursor object
  #Returns: A tuple of playTimes matching the search parameters
  cursor.execute(
    "SELECT playTimes FROM songs where title=? AND artist=?",(title, artist,)
 )

  results = cursor.fetchone()
  return results

def addEntry(tableName, entry, cursor):
  #Input: 'entry'->Four field tuple of form:
  #          (ArtistName,SongTitle,TrackHash,newPlayTime)
  #       cursor object of the database
  #Queries the database by songTitle and ArtistName for a tuple of previous
  #logged playtimes, and appends the newtime into the joined field 
  #Returns: None
  artist,title,trackHash,newPlayTime,trackUrl = entry
  queryPlayTimes = lookupQuery(title, artist, cursor)

  uniqTimes = dict()

  if (queryPlayTimes): 
    queryPlayTimesString = queryPlayTimes[0]
    newPlayTime = str(newPlayTime)
    foundStatus = newPlayTime in queryPlayTimesString
    if (foundStatus): return

    #Append the new play time to the previously logged times
    strPlayTimes = "%s %s"%(queryPlayTimesString,newPlayTime) 

    cursor.execute(#Update the DB
     'UPDATE songs set playTimes=? where artist=? AND trackHash=? AND url=?', 
     (strPlayTimes, artist, trackHash,trackUrl)
   )

  else: #First time seeing the track
     cursor.execute('INSERT INTO songs VALUES(?,?,?,?,?)', 
           (artist,title, trackHash,trackUrl,newPlayTime)
    ) 

def rankTracks(cursor):
  #Input: cursor to the source database
  #Returns: A report on the ranks of the tracks played in the form of a string
  UNIMPORTED_MONITOR = True
  while UNIMPORTED_MONITOR: #Try to load the module containing the monitor dates
    try:
      import monitor_start
    except ImportError as e:
      create_monitor_time_src()
    except Exception:
      sys.stderr.write("Fatal error: ")
      sys.stderr.write(e.msg)
      sys.exit(-10)
    else:
      UNIMPORTED_MONITOR = False

  monitorEndDate = monitor_start.MONITOR_END_DATE
  monitorStartDate = monitor_start.MONITOR_START_DATE
  curTimeSecs = time()
  if (monitorEndDate[0] <= curTimeSecs):
    #Time to make a backUp and a report
    #Create a json of that data
    archiveStatus = createJSON.archiveLoadedData()
    sys.stderr.write("Archive status %s"%(archiveStatus))
    return None

  ranks = dict()
  ranksStr = ''

  for row in cursor.execute('SELECT * FROM songs'):
    artist,title,trackHash,playTimes,url = row
    timesPlayedList = re.findall(r'(\d+)', playTimes)

    nPlayTimes      = len(timesPlayedList)
    timesPlayedList.insert(0, nPlayTimes)

    #Create a key mapping (number_of_plays,plays) => (title,artist)
    ranks[ tuple(timesPlayedList) ] = (title, artist)

  #Ranks sorted in ascending order
  rankKeys = sorted(list(ranks.keys()), reverse=True)
  
  if not rankKeys: return None

  if (len(monitorStartDate)) != 2:
    sys.stderr.write("Corrupted monitor start date format")
    sys.exit(-3)

  

  nLine =  ('*'*80).center(100, ' ')
  ranksStr += 'TopPlayed Tracks by the BearRocks.com'.center(100, ' ' )+'\n'
  ranksStr +=  ('as last updated at: %s. Monitored from %s'%(ctime(), 
   monitorStartDate[1])).center(100, ' ') + '\n'

  ranksStr +=  nLine +'\n'
  ranksStr +=  '{h:<4} {pos:>5}  {t:<40}  {a:<40}{pTs:<25}\n'.format(
      h='#', pos='Rank', pTs='PlayCounts',t='Title',a='Artist')

  realPos      = 1 #Popularity/Rank of each entry relative to other entries
  runningIndex = 1 #Ascending order index of entries, starting at '1'
  lastNPlays   = 0

  for eachKey in rankKeys:
    title,artist = ranks[eachKey]
    nPlayCounts,pTimes = eachKey[0],eachKey[1:]

    if (lastNPlays != nPlayCounts):
      realPos = runningIndex

    ranksStr += '{seqPos:<5} {pos:<5} {t:<40} {a:<40} {pTs}\n'.format(
	seqPos=runningIndex, pos=realPos, pTs=nPlayCounts,t=title,a=artist)
      
    runningIndex += 1
    lastNPlays = nPlayCounts

  return ranksStr

def main():
  dbPath = resources.dbPath
  conn,cursor = getConCursor(dbPath)
  print(rankTracks(cursor))

if __name__ == '__main__':
  main()
