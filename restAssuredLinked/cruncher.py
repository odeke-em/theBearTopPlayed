#!/usr/bin/env python3

# Author: Emmanuel Odeke <odeke@ualberta.ca>

import re
import sys

# Local module
import extractor
from dbConn import DbLiason
pParse = DbLiason.produceAndParse

class TheBearHandler(object):
    def __init__(self, baseUrl, *args, **kwargs):
        self.baseUrl = baseUrl
        self.__songHandler = DbLiason.HandlerLiason(baseUrl + '/songHandler')
        self.__artistHandler = DbLiason.HandlerLiason(baseUrl + '/artistHandler')

    @property
    def songHandler(self):
        return self.__songHandler

    @property
    def artistHandler(self):
        return self.__artistHandler

    def extractArtist(self, attrs):
        pass

    def addSong(self, songAttrs, artistAttrs):
        artist, artistURI = artistAttrs
        artistID = self.addArtist(dict(name=artist, uri=artistURI))
        if artistID:
            check = pParse(self.__songHandler.getConn, dict(
                title=songAttrs.get('title', None), artist_id=artistID,
                select='id', playTime=songAttrs.get('playTime', None))
            )

            if not (check and check.get('data', None)):
                songAttrs['artist_id'] = artistID
                cResponse = pParse(self.__songHandler.postConn, songAttrs)
                print(cResponse)
            else:
                print(check)

    def updateSong(self, songAttrs):
        pass

    def deleteSong(self, attrs):
        pass

    def addArtist(self, attrs):
        pResponse = pParse(
            self.__artistHandler.getConn, dict(
                name=attrs.get('name', None), select='id'
            )
        ) 

        if pResponse:
            data = pResponse.get('data', None)
            if data:
                return data[0].get('id', None)

        cResponse = pParse(self.__artistHandler.postConn, attrs)
        if cResponse:
            print(cResponse)
            data  = cResponse.get('data', None)
            if hasattr(data, 'get'):
                return data.get('id', None)
        
    def updateArtst(self, attrs):
        artist = attrs.get('artist', None)

        parsedResponse = pParse(self.__artistHandler, dict(name=artist))
        if parsedResponse:
            data = parsedResponse.get('data', None)
            if data:
                return data[0].get('id', -1)

    def deleteArtist(self, attrs):
        return self.__artistHandler.deleteConn(attrs)

    def getArtist(self, attrs):
        return self.__artistHandler.getConn(attrs)

    def getSong(self, attrs):
        return self.__songHandler.getConn(attrs)

    def checkArtist(self, artistName):
        parsedResponse = pParse(
            self.__artistHandler.getConn, dict(name=artistName)
        )

        if parsedResponse:
            data = parsedResponse.get('data', None)
            if data: return True

        return False

def main():
    restAssuredAccessibleUrl = 'http://127.0.0.1:8000/thebear'

    argc = len(sys.argv)
    if argc > 1:
        restAssuredAccessibleUrl = sys.argv[1]

    print(restAssuredAccessibleUrl)
    # sys.exit(0)
    dbHandler = TheBearHandler(restAssuredAccessibleUrl)

    crawled = extractor.crawl()
    for tup in crawled:
        artist, title, playTime, uri = tup
        artist = re.sub('\s', '_', artist) 
        title = re.sub('\s', '_', title) 
        dbHandler.addSong(
            dict(title=title, playTime=playTime), (artist, uri)
        )

if __name__ == '__main__':
    main()
