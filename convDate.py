#!/usr/bin/python
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re
import time

######################################################################
FEB_IDX = 2 #February's index in the Gregorian calendar
PM = 'PM'
AM = 'AM'
S_A_J_N = [9,4,6,11] #Indices of Months with 30 days ie:
                     #  September, April, June, November
######################################################################

def isLeap(year):
  #Input: A year as an integer.
  #Returns: True' iff a year is a leap year

  #No odd numbered year is a leap year
  if (year & 1): return False

  if (not year%400):  return True

  elif (not year%100):  return False

  elif (year%4):  return False

  return True

#Returns the seconds since the epoch
base_seconds = lambda : mdy_date_to_Int("00:00 AM", "01/01/1970")

def get_days_in_month(monthIdx, year):
  #Input:  A month's index, and year, both integers.
  #Output: The number of days in that month.
  #Given a month's index check if it is February, and from 
  #that return the number of days that February has depending
  #on if it is leap year or not.
  #Else check if the month is in SAJN(30 day - months) classification.
  #Else return 31
  if (monthIdx is FEB_IDX):
    if (isLeap(year)):
      return 29
    return 28

  if (monthIdx in S_A_J_N):
    return 30

  return 31

##########################################################################

def concatDate(timeStr, dateStr):
  #Input: timeStr => HH:MM AM/PM form
  #       dateStr => dd/mm/yyyy  form
  hh_mm_apm = re.findall(r'(\d+):(\d+)\s(\w+)', timeStr)[0]  
  m_d_y = re.findall(r'(\d+)/(\d+)/(\d\d\d\d)', dateStr)[0]

  if (len(hh_mm_apm) != 3): return -1 #Failed to get time fields
  if (len(m_d_y) != 3): return -1 #Failed to get time fields

  hh = int(hh_mm_apm[0])
  mm = int(hh_mm_apm[1])
  apm = hh_mm_apm[2] #String: either 'AM' or 'PM'

  #Convert hours to 24 hour clock -> add +12 if PM 
  if (re.search(apm, PM)):
    hh +=  12
  month,day,year = m_d_y
  joinedDate = list(map(lambda s : "{0:0>2}".format(s),[year,month,day,hh,mm]))
  return "".join(joinedDate)


if __name__ == '__main__':
  #Simple visual verification
  concatDate = concatDate('3:23 AM', '6/30/2013')
  print(concatDate)
