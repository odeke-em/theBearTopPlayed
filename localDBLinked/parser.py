#!/usr/bin/python3

from optparse import OptionParser

def cliParser():
  #Input: None
  #Returns: parser for updateDb
  parser = OptionParser()

  parser.add_option('-t','--timeout',dest='timeout',
  help="Set the timeout in minutes between database updates", default=1)

  parser.add_option('-d', '--displayranks', dest='displayranks',
  help="Set whether to print out ranks every after a data collection",
  default=True,action="store_false")

  args,options = parser.parse_args()

  return args,options
