#!/usr/bin/python3

#Author: Emmanuel Odeke <odeke@ualberta.ca>

import os, re, sys, shutil, glob
from stat import S_ISDIR, S_ISREG
from datetime import datetime
'''
try:
  import monitor_start
except ImportError as e:
  sys.stderr.write(
    "Failed to import file containing monitoring start date\n"
  )
  sys.exit(-1)
'''
###########################CONSTANTS HERE################################
TAR_SUFFIX = "tar"
BASE_DIR_NAME = "rankBack"
#########################################################################
existantPath = lambda path: path and os.path.exists(path)

canRead  = lambda path : existantPath(path) and os.access(path, os.R_OK)
canWrite = lambda path : existantPath(path) and os.access(path, os.W_OK)
canExecute = lambda path : existantPath(path) and os.access(path, os.X_OK)

canRW = lambda path : canRead(path) and canWrite(path)
canRX = lambda path : canRead(path) and canExecute(path)
canRWX = lambda path: canRead(path) and canWrite(path) and canExecute(path)

createDir = lambda path : (not existantPath(path)) and os.mkdir(path)
statDict  = lambda path : os.stat(path)

isDir = lambda path: existantPath(path) and S_ISDIR(statDict(path).st_mode)
isReg = lambda path: existantPath(path) and S_ISREG(statDict(path).st_mode)

def getIntDate():
  #Returns YYYYMMDD as an integer
  timeNow = datetime.now()
  dateStr = "{y:0>4}{m:0>2}{d:0>2}".format(
    y=timeNow.year,m=timeNow.month,d=timeNow.day
  )

  return int(dateStr)

#Returns the base_suffix with the creation date suffixed
createSourceDirName = lambda baseName=BASE_DIR_NAME:"%s%s"%(baseName,getIntDate())

#Delete tree
delTree = lambda path : existantPath(path) and shutil.rmtree(path)

def getInode(path):
  if not existantPath(path): return -1
  return statDict(path).st_ino

def existantPaths(args):
  #Returns True iff all the paths in the args are existant paths
  if not hasattr(args, '__iter__'): return False
  
  allValidPathsBool = True
  for eachPath in args:
    if not existantPath(eachPath):
      allValidPathsBool = False

  return allValidPathsBool
  
def moveFile(src, dest, COPY_ONLY=True):
  if not existantPath(src): 
    return None

  if COPY_ONLY:
    return shutil.copy(src, dest)
  else:
    return shutil.move(src, dest)

def cpFile(src, dest):
  #Only copying non-directories here
  if not existantPath(src): return None
  print("Src ",src, " Dest ",dest)
  return shutil.copy(src, dest)

def cpDir(src, dest):
  if not (existantPath(src) and dest): return None
  
  #Cannot allow to copy a source to itself
  if existantPath(dest) and not (getInode(src) == getInode(dest)): 
    return None

  return shutil.copy2(src, dest)

def makeArchive(base_name, fmt=TAR_SUFFIX, root_dir=None, **kwargs):
  if not (base_name and fmt and existantPath(root_dir)): return None

  return shutil.make_archive(base_name,fmt,root_dir)

def globPaths(targetPathSuffices):
  if not hasattr(targetPathSuffices, '__setitem__'): return None

  matchedPaths = []
  for targSuffix in targetPathSuffices:
    matchedPaths += glob.glob(targSuffix)
  return matchedPaths

def copyMatchesToDir(suffixList, dest,COPY_ONLY=True):
  if not existantPath(dest): 
    createDir(dest)

  targetMatches = globPaths(suffixList)
  if not targetMatches:
    print("No file matches for suffices ",suffixList)
    return None
  #print("Target matches ",targetMatches)
  rejectedPaths = []
  for eachMatch in targetMatches:
    moveFile(eachMatch, dest, COPY_ONLY)
  #print(list(rejectedPaths))
  return rejectedPaths

def main():
  print(
    makeReportPackage(fileMatches=['*db','*rk','*json'])
  )

def makeReportPackage(fileMatches=[],baseName=None,copyOnly=True):
  if not (fileMatches): 
    print("No files to archive")
    return None

  dirSource = baseName
  if not baseName: 
    dirSource = createSourceDirName()

  if not dirSource: return None
 
  rejectedPaths = copyMatchesToDir(fileMatches, dirSource, copyOnly)

  #Time to make the archive
  archResult = makeArchive(dirSource, TAR_SUFFIX, root_dir=dirSource)
  if not archResult:
    print("Failed to create archive from directory %s",dirSource)
    return -1
  print("Created archive %s"%(archResult))
  return 0

if __name__ == '__main__':
  main()
