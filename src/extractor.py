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
timeStampRegex     = r'(\d?:?\d+:\d+\s[AP]?M)'
linkTitleRegex     = r'<a href="(.*)"\s+title="\s*(.*)\s*-\s*(.*)\s*">'

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
    #             dateOfTrack -> dd/mm/yyyy string
    #Returns: 
    #                if successful: 
    #                     'artistName', 'songTitle',
    #                     'secondsString'-> string of seconds since the epoch in reference 
    #                                       to the time that the song was reported played
    #                else: None 
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

        return artist, songTitle, dateInt, songUrl

def crawl():
    data = sitereader.site_opener(
        BEAR_ROCKS_URL, stderr=sys.stderr, errorVerbosity=True
    )

    if not data:
        sys.stderr.write(
            "\n\t\033[31mFailed to retrieve data from %s. "%(BEAR_ROCKS_URL)
        )
        sys.stderr.write("Check the url or the script's regular expressions\n")
        return None

    #Taking out all tabs and carriage returns
    data = re.sub('[\t\r]', '', data)

    dateStampFindall = dateStampCompile.findall(data)
    dateInTag,dateDisplayed = dateStampFindall[0]

    #The date displayed in the tag as the selected date must match that displayed
    #else the data is corrupted
    assert(dateInTag == dateDisplayed)
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

    params = []
    for tr in fullTrs:
        songParams = ripTrackInfo(tr, dateDisplayed)
        if songParams:
            params.append(songParams)

    return params

def main():
    crawl()

if __name__ == '__main__':
    main()
