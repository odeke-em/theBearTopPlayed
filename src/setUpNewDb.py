#!/usr/bin/python3

#Author: Emmanuel Odeke <odeke@ualberta.ca>

import sqlite3
import os
from stat import S_ISDIR, S_ISREG, S_ISFIFO

import dbDesign #Local module

pathExists = lambda path: path and os.path.exists(path)
isDir = lambda path : pathExists(path) and S_ISDIR(statDict(path).st_mode)
isReg = lambda path : pathExists(path) and S_ISREG(statDict(path).st_mode)

canRead   = lambda path : pathExists(path) and os.access(path, os.R_OK)
canWrite  = lambda path : pathExists(path) and os.access(path, os.W_OK)
canDelete = lambda path : canWrite(path)

def statDict(path):
  if pathExists(path):
    return os.stat(path)

def generateDB(dbName):
  if not dbName:
    raise Exception("Expecting a non-NULL database name")
    exit(-1)

  if pathExists(dbName):
    if not isReg(dbName):
      raise Exception("Only regular files are allowed to be databases")
      exit(-2)

    if not canDelete(dbName):
      raise Exception("You need have delete permissions to file %s"%(dbName))
      exit(-3)

    else:
      #Time to delete that file
      os.unlink(dbName)

  connection = sqlite3.connect(dbName)

  try:
    for commandString in dbDesign.creationTablesTuple:
      connection.execute(commandString)

    connection.commit()
  except sqlite3.OperationalError as e:
    print(e)
    return False
  except Exception as e:
    print(e)
    return False
  else:
    return True

def main():
  generateDB('songDatabase.db')

if __name__ == '__main__':
  main()
