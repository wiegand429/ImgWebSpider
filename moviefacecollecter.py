#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:55:02 2017

colloct faces from movie
@author:wiegand 
"""


import cv2
import dlib
import threading
import emotion_micro
import time
import os

DETECTOR = dlib.get_frontal_face_detector() #Face detector
MOVIELIST = ["agent.mp4"]
MOVIEFACE = "./movieface"
#
#@filename:movie path
#@return:frame
class faceCatcher:
    def __init__(self,filename):
        self.movie = None
        self.faceindex = 0
        self.index = 0
        self.movieName = filename
#        print self.movieName
        if os.path.exists(MOVIEFACE):
            pass
        else:
            os.mkdir(MOVIEFACE)
        self.filepath = MOVIEFACE+'/'+self.movieName.split('.')[0]
        if os.path.exists(self.filepath):
            pass
        else:
            os.mkdir(self.filepath)
        for dirname in emotion_micro.EMOTIONS:
            if os.path.exists(self.filepath+'/'+dirname):
                pass
            else:
                os.mkdir(self.filepath+'/'+dirname)
            
    def openMovie(self):
        if self.movieName:
            self.movie = cv2.VideoCapture(self.movieName)
    def faceSave(self):
        while 1:
            if self.movie:
                    ret,image = self.movie.read()
                    if ret:
#                        cv2.resize()
#                        print image.shape()
#                        print image.shape[0],image.shape[1]
#                        cv2.imshow("img",image)
#                        cv2.waitKey(2)
                        faces = DETECTOR(image, 0)
        #                print faces
        #                removeimg = 1
                        for k,d in enumerate(faces):
        #                   removeimg = 0
                           x = d.left()
                           y = d.top()
                           w = d.width()
                           h = d.height()
                           face = image[y:y+h,x:x+w]
#                           cv2.imshow("img",face)
#                           cv2.waitKey(3) 
                           print face.shape[1],face.shape[0]
                           filename = os.path.join('./trash', str(self.movieName.split(".")[0])+"_"+str(self.index) + ".jpg")
                           cv2.imwrite(filename,face)
                           time.sleep(2)
                           emotion = emotion_micro.getemotion(filename)
                           if emotion != "error" and emotion != None:
                               facesname = os.path.join(self.filepath,emotion,emotion+'_'+str(self.faceindex)+".jpg")
                               print facesname
                               cv2.imwrite(facesname,face)
                               self.faceindex = 1 + self.faceindex
                        self.index = self.index + 1
        #                if removeimg:
        #                    shutil.move(filename,)
                    else:
                        print "read frame error"
                
    def close(self):
        if self.movie:
            self.movie.release()
        

if __name__ == "__main__":
    
    moviecap = faceCatcher(MOVIELIST[0])
    moviecap.openMovie()
    moviecap.faceSave()
    moviecap.close()

#        
