#!/usr/bin/env python3

import os
import json
import collections
import urllib.request, urllib

class DbConn:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def __urlRequest(self, method, isGet=False, **getData):
        fmtdData = json.dumps(getData)
        reqUrl = None

        if not isGet:
            reqUrl = self.baseUrl
        else:
            reqUrl = self.baseUrl + '/?' + '&'.join([
                '{k}={v}'.format(k=k, v=v) for k, v in getData.items()
            ])
        req = urllib.request.Request(reqUrl)
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda : method.upper()
        dataOut = dict()
        try:
            uR = urllib.request.urlopen(req, bytes(fmtdData, encoding='utf-8'))
        except Exception as e:
            print(e)
            dataOut['reason'] = e
        else:
            dataOut['value'] = uR.read()
        return dataOut

    def get(self, data):
        return self.__urlRequest('get', isGet=True, **data)

    def put(self, data):
        return self.__urlRequest('put', **data)

    def post(self, data):
        return self.__urlRequest('post', **data)

    def delete(self, data):
        return self.__urlRequest('delete', **data)

class HandlerLiason(object):
    def __init__(self, baseUrl, *args, **kwargs):
        self.handler = DbConn(baseUrl)

    def postConn(self, data):
        return self.handler.post(data)

    def deleteConn(self, data):
        return self.handler.delete(data)

    def putConn(self, data):
        return self.handler.put(data)

    def getConn(self, data):
        return self.handler.get(data)

def produceAndParse(func, dataIn):
  dbCheck = func(dataIn)
  if hasattr(dbCheck, 'reason'):
    return dbCheck
  else:
    response = dbCheck.get('value', None)
    if response:
      try:
        return json.loads(response.decode())
      except Exception as e:
        return dict(reason = e)
