#!/usr/bin/python
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import re

##############################################################
FEB_IDX = 2
PM = 'PM'
AM = 'AM'
S_A_J_N = [ 4, 6, 10, 11 ]
BASE_YEAR = 1970
##############################################################

relativeyear = lambda year : abs( year - BASE_YEAR ) 
def isLeap( year ):
  #No odd numbered year is not a leap year
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
  if ( monthIdx is FEB_IDX ):
    print( year )
    if ( isLeap( year )):
      return 29
    return 28

  if ( monthIdx in S_A_J_N ):
    return 30

  return 31
##############################################################
def mdy_date_to_Int( dateStr, timeStr ):
  hh_mm_apm = re.findall( r'(\d+):(\d+)\s(\w+)', dateStr )[0]
  m_d_y = re.findall( r'(\d+)/(\d+)/(\d\d\d\d)', timeStr )[0]

  month = int( m_d_y[0] )
  day   = int( m_d_y[1] )
  year  = int( m_d_y[2] )
  nDays_in_year = 365 

  if ( isLeap( year )):
    nDays_in_year = 366

  nDays_in_month = get_days_in_month( month, year )

  nDays = day + ( relativeyear( year )*nDays_in_year ) + nDays_in_month 
  nDays *= 24

  hh = int( hh_mm_apm[0] )
  mm = int( hh_mm_apm[1] )*60
  apm = hh_mm_apm[2]

  hh += nDays

  if ( re.search( apm, PM )):
    hh +=  12

  hh *= 60*60

  seconds = hh+mm
  return seconds
    
if __name__ == '__main__':
  print( mdy_date_to_Int( '12:29 PM', '5/13/2013' ))
