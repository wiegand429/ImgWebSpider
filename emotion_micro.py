#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#"""
#Created on Fri May  5 14:58:04 2017
#
#@author:wiegand 
#"""
#
import httplib, urllib, base64



EMOTIONS = ["anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"]

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'key',
}

def getemotion(imgpath,key = None):
    data3 = {"anger":0,"contempt":0,"disgust":0,"fear":0,"happiness":0,"neutral":0,"sadness":0,"surprise":0}
    dlist = []
    if ".jpg" in imgpath:
        fp = open(imgpath, "rb")  
        fp.seek(0, 0)  
        d = []  
        d = fp.read()
        params = urllib.urlencode({})
        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, d, headers)
            response = conn.getresponse()
#            print response
            data = response.read()
            print "len of :",len(data)
            if len(data) > 200:
                data2 = data.split('}')[1].split('{')[1].split(',')
                for index in xrange(len(data2)):
                    fvalue = float(data2[index].split(':')[1])
                    data3[EMOTIONS[index]] = fvalue
                    dlist.append(fvalue)
                
                conn.close()
                return EMOTIONS[dlist.index(max(dlist))]
            else:
                return "error"
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return None
        
if __name__ == "__main__":
    a = getemotion('agent_4.jpg')
    print a

