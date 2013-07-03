#!/usr/bin/python
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re

######################################################################
FEB_IDX = 2 #February's index in the Gregorian calendar
PM = 'PM'
AM = 'AM'
S_A_J_N = [ 4, 6, 10, 11 ] #Indices to Months with 30 days
                           #September, April, June, November-SAJN
BASE_YEAR = 1970
######################################################################

#Input: Unsigned value of the year
#Returns: the unsigned result of the subtraction of the input from 
#           the base year
relativeyear = lambda year : abs( year - BASE_YEAR ) 

def isLeap( year ):
  #Input: An year as an integer
  #Returns 'True' iff a year is a leap year
  
  #No odd numbered year is a leap year
  if ( year & 1 ):
    return False

  if ( not year%400 ):
    return True 

  elif ( not year%100 ):
    return False

  elif ( year%4 ):
    return False

  return True

def get_days_in_month( monthIdx, year ):
  #Input:  A month's index, and year, both integers.
  #Output: The number of days in that month.
  #Given a month's index check if it is February, and from 
  #that return the number of days that February has depending
  #on if it is leap year or not.
  #Else check if the month is in SAJN(30 day - months) classification.
  #Else return 31
  if ( monthIdx is FEB_IDX ):
    if ( isLeap( year )):
      return 29
    return 28

  if ( monthIdx in S_A_J_N ):
    return 30

  return 31
##########################################################################
def mdy_date_to_Int( dateStr, timeStr ):
  #Input: timeStr => HH:MM AM/PM form
  #       dateStr => dd/mm/yyyy  form
  #Returns: Unsigned equivalent after converting the date and time to
  #         seconds. 
  #         **if retrieval/conversion fails, return '-1', else output
  #          should be unsigned
  hh_mm_apm = re.findall( r'(\d+):(\d+)\s(\w+)', timeStr )[0]
  m_d_y = re.findall( r'(\d+)/(\d+)/(\d\d\d\d)', dateStr )[0]
  
  if (len(hh_mm_apm) != 3): return -1 #Failed to get time fields
  if (len(m_d_y) != 3): return -1 #Failed to get time fields
  
  month = int( m_d_y[0] )
  day   = int( m_d_y[1] )
  year  = int( m_d_y[2] )
  

  if ( isLeap( year )): nDays_in_year = 366
    
  else: nDays_in_year = 365 

  nDays_in_month = get_days_in_month( month, year )

  nDays = day + (relativeyear( year )*nDays_in_year) + nDays_in_month 
  nDays *= 24 #Convert those days to hours

  hh = int( hh_mm_apm[0] )
  mm = int( hh_mm_apm[1] )*60 #Minutes converted to seconds
  apm = hh_mm_apm[2]

  hh += nDays

  if ( re.search( apm, PM )): #Add 12 hours if time of the day is PM
    hh +=  12

  hh *= 60*60  #Hours converted to seconds

  seconds = hh+mm
  return seconds
    
if __name__ == '__main__':
<<<<<<< HEAD
  converted_value = mdy_date_to_Int( '12:29 PM', '5/13/2013' )
  assert(converted_value == 1359937740)

=======
  #Simple visual verification
  converted_value = mdy_date_to_Int( '12:29 PM', '5/13/2013' )
  assert(isinstance(converted_value,int))
  assert(converted_value >= 0) #Making sure we've got an unsigned result
  assert(converted_value == 1359937740) #Value determined by following
                                        #algorithm and hand-calculation 
>>>>>>> 364bd914e23aaf065a18790838a1eaca875f3ae6
