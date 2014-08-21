#!/usr/bin/env python3
# Author: Emmanuel Odeke <odeke@ualberta.ca>
import re
import sys

# Local module
import extractor
from resty import restDriver

def crunch(address='http://127.0.0.1', port='8000'):
    connector = restDriver.RestDriver(address, port)
    connector.registerLiason('Song', '/thebear/songHandler')
    connector.registerLiason('Artist', '/thebear/artistHandler')

    crawled = extractor.crawl()
    for tup in crawled:
        artistName, title, playTime, artistURI = tup
        artistName = re.sub('\s', '_', artistName.strip(' ')) 
        title = re.sub('\s', '_', title.strip(' '))

        # Unicode is tripping out comparisons, and for starters we shall be using 'uri' as unique attr 
        artistNameInfo = connector.getArtists(uri=artistURI)
        readInfo = artistNameInfo.get('value', {}).get('data', None)

        if not (readInfo and len(readInfo) >= 1):
            readInfo = connector.newArtist(name=artistName, uri=artistURI)
            if not (isinstance(readInfo, dict) and readInfo.get('status_code', 400) == 200):
                print('Failed to create new artist. Data back', readInfo)
                continue
           
            readInfo = readInfo.get('value', {}).get('data', None)
            print('created Artist', readInfo)
        else:
            readInfo = readInfo[0] # Head element

        songContent = {'title': title, 'artist_id': readInfo.get('id', -1), 'playTime': playTime}
        queriedInfo = connector.getSongs(**songContent)
        readSongInfo = queriedInfo.get('data', None)
        if not (readSongInfo and len(readSongInfo) >= 1):
            print('Freshly creating', songContent, connector.newSong(**songContent))
        else:
            print('Already registered', songContent)

def main():
    args, options = restDriver.cliParser()
    crunch(args.ip, args.port)

if __name__ == '__main__':
    main()
