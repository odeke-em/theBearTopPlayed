#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import sys
import os
import json
import sqlite3
import re
import time

import mover
import resources

numbersOnlyCompile = re.compile('^(\d+\s?){1,}$')
def getJSON(dbPath):
  if not mover.existantPath(dbPath): return None
  conn = sqlite3.connect(dbPath)
  cur  = conn.cursor()

  cur.execute('select * from songs')

  #Retrieving the table's column names
  tableNames = list(map(lambda tup : tup[0], cur.description))

  #Dictionary to handle and extract dates
  exc = {lambda s : re.search('^(\d+\s?){1,}$',s) : numbersOnlyCompile.findall}

  entriesList = list()

  getIntField = lambda s : re.search('^(\d+\s?){1,}$',s)
  #Doing a query for all elements in the db
  for eachEntry in cur:
    entryDict=dict()
  
    dates = filter( getIntField, eachEntry)

    nonDates = filter(lambda s: not getIntField(s), eachEntry)

    dates = list(dates)[0].split(" ")
    dates = list(filter(lambda s : s, dates))
    entryDict['count'] = len(dates)
    nonDates = list(nonDates)
    nonDates.append(dates)
    #print("tN ",tableNames)
    #print("nD ",nonDates)
    for i in range(len(nonDates)):
      entryDict.setdefault(tableNames[i],nonDates[i])
    if not entryDict:
      continue
    entriesList.append(entryDict)

  return entriesList

def getMonitorData():
  metaData = dict()

  monitorStart = "Invalid"
  monitorEnd = "Invalid"

  try:
    import monitor_start 
  except ImportError:
    sys.stderr.write("Failed to import the module containing monitor dates") 
  else:
    try:
      monitorStart = monitor_start.MONITOR_START_DATE[1]
      monitorEnd = monitor_start.MONITOR_END_DATE[1]
    except AttributeError:
      sys.stderr.write("Invalid dates in module 'monitor_start'")
    except Exception:
      sys.stderr.write("Invalid date formats in moduel 'monitor_start'")
  metaData["monitorStartDate"] = monitorStart 
  metaData["monitorEndDate"] = monitorEnd

  return metaData 

def saveJSON(dbName,destName):
  if not mover.existantPath(dbName): 
    sys.stderr.write(
     "\033[31mThe source database %s does not exist\033[00m\n"%(dbName)
    )
    return None
  if not destName: 
    sys.stderr.write(
     "\033[31mExpecting a path to store the retrieved json\033[00m\n"
    )
    sys.exit(-4)

  metaData = getMonitorData()
  trackInfo = getJSON(dbName)
  with open(destName,"w") as f:
    try:
      outDict = dict()
      outDict["meta"] = metaData
      outDict["data"] = trackInfo 
      f.write(json.dumps(outDict))
    except IOError:
      sys.stderr.write("Failed to write json data to %s"%(destName))
      return None

  return True
 
def archiveLoadedData():
  #Utility to manage archiving and deletion of logged files 
  jsonCreationSuccess = saveJSON(resources.dbPath,resources.JSON_DUMP_PATH)
  archivingStatus = False
  if not jsonCreationSuccess:
    print("Could not create a json file of the played tracks")
    return False

  dirSrc = mover.createSourceDirName()
  #Time to archive the created json, DB and ranks file
  if not mover.makeReportPackage(
    fileMatches=[
      "monitor_start*",resources.dbPath,resources.JSON_DUMP_PATH,
      resources.RANKS_DUMP_PATH],
    baseName=dirSrc,copyOnly=False):
    #Success here
    inodeGetter = mover.getInode
    if inodeGetter('.') != inodeGetter(dirSrc): 
      if mover.canWrite(dirSrc):
        deleteFunc = os.unlink
        if mover.isDir(dirSrc): 
          deleteFunc = mover.delTree
        try: 
          deleteFunc(dirSrc)
        except Exception as e: 
          sys.stderr.write("%s \n"%(e.__str__()))
          sys.stderr.write("Failed to delete %s\n"%(dirSrc))
      else:
       sys.stderr.write("You don't have write permissions for %s\n"%(dirSrc)) 
  return True

if __name__ == '__main__':
  print(archiveLoadedData())
