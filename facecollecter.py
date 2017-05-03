# -*- coding: utf-8 -*-
"""
Spyder Editor
face collecter
"""

import httplib  
import urllib  
import re  
import os 
from urllib2 import urlopen
from urllib import quote
import cv2
import dlib
import time
import shutil
import threading

DETECTOR = dlib.get_frontal_face_detector() #Face detector

colloctnames = ["人民的名义", "神盾局特工"，"西部世界"]

class Collecter_Thread(threading.Thread):
    def __init__(self,collectername):
        super(Collecter_Thread,self).__init__()
        self.arg = collectername
        
        self.collecter = ImgCollecter()
    
    def run(self):
        self.collecter.init_collecter_name(self.arg)    
        self.collecter.request() 
        
    
class ImgCollecter():
    def __init__(self):
        self.CollecterOBJName = None
        self.walker = 20
        self.index = 1
        self.Savepath="./ImgDownload"
        self.faceindex = 1 
    def init_collecter_name(self,name):
        self.CollecterOBJName = quote(name)
    def request(self):  
            if os.path.exists(self.Savepath):
                pass
            else:
                os.mkdir(self.Savepath)
            try:  
                while 1:  
                    conn = httplib.HTTPConnection('image.baidu.com')  
                    request_url ='/search/flip?tn=baiduimage&ie=utf-8&word='+self.CollecterOBJName+'&pn='+str(self.walker)+'&gsm=3c'
                    url = "http://image.baidu.com"+ request_url                                                                                          
#                    print "[url]:",url                                                                                      
                    conn.request('GET',request_url)  
                    r= conn.getresponse()  
                    print r.status  
                    if r.status == 200:  
                        html =self.getHtml(url)

                        self.downLoad(self.getImg(html),self.Savepath)         
                    self.walker += 60 
#                    print "walker is ",self.walker
            except Exception,e:  
                print e  
            finally:  
                conn.close()  
                
    def getHtml(self,url):
        page=urllib.urlopen(url)
        html=page.read()
        return html
    
    def getImg(self,html):
        reg=r'"objURL":"(.*?)"'   
        imgre=re.compile(reg)
        print imgre
        imglist=re.findall(imgre,html)
        l=len(imglist)
        print l
        return imglist
    
    def downLoad(self,urls,path):
        for url in urls:
            print("[Downloading]:",len(urls), url)
            try:
                fp = urlopen(url,timeout = 60)
                if os.path.exists(path+"/trash"):
                        pass
                else:
                    os.mkdir(path+"/trash")
                    
                if os.path.exists("faces"):
                        pass
                else:
                    os.mkdir("faces")
                data = fp.read()
#                facesname = os.path.join("./faces",str(self.faceindex)+".jpg")
#                trashname = os.path.join(path+"/trash",str(self.CollecterOBJName)+'_'+str(self.index) + ".jpg")
                filename = os.path.join(path, str(self.CollecterOBJName)+"_"+str(self.index) + ".jpg")
                self.index  = self.index + 1
                f = open(filename , 'w+b')
                f.write(data)
                time.sleep(10)
                image = cv2.imread(filename)
                faces = DETECTOR(image, 1)
#                print faces
#                removeimg = 1
                for k,d in enumerate(faces):
#                   removeimg = 0
                   x = d.left()
                   y = d.top()
                   w = d.width()
                   h = d.height()
                   face = image[y:y+h,x:x+w]
                   cv2.imshow("img",face)
                   cv2.waitKey(5) 
                   facesname = os.path.join("./faces",str(self.CollecterOBJName)+'_'+str(self.faceindex)+".jpg")
                   cv2.imwrite(facesname,face)
                   self.faceindex = 1 + self.faceindex
#                if removeimg:
#                    shutil.move(filename,)
                
            except:
                print "[error!!]request next picture!!"
                

if  __name__ == '__main__':  
    for item in colloctnames:
        CLTthread = Collecter_Thread(item) 
        CLTthread.start()
