from tkinter import *
from tkinter import ttk
import cv2
import os
import numpy as np
from PIL import Image
from threading import Thread
import mysql.connector
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.parser import parse
tableoftab=[]
scheduler=BackgroundScheduler()
arra=[]
def startDetectorfaculty(strpid):
	if(strpid!=None):
		if(scheduler!=None):
			scheduler.remove_job(strpid)
	cnx = mysql.connector.connect(user='root',password="",host="localhost")
	cursor = cnx.cursor()
	DB_NAME = 'attend'


	try:
		cnx.database = DB_NAME
	except mysql.connector.Error as err:
		if(err.errno == errorcode.ER_BAD_DB_ERROR):
			create_database(cursor)
			cnx.database = DB_NAME
		else:print(err);

	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer/trainer.yml')
	cascadePath = "Classifiers/face.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath);
	path = 'dataSet'
	cam = cv2.VideoCapture(0)
	b=False
	nooframes=100
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(im,"detector",1, 1, 0, 1, 1)
    #font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font
	while(True):
		ret, im =cam.read()
		gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
		nooframes-=1
		name=""
		for (x,y,w,h) in faces:
			nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
			cv2.rectangle(im,(x-50,y-50),(x+w+20,y+h+20),(255,255,255),1)
			nbr_predicted=str(nbr_predicted)
			a=[]
			for i in range(0,len(nbr_predicted),2):
				a.append(int(nbr_predicted[i:i+2]))
			number=''.join(chr(i) for i in a)
			#print(number)
			cursor.execute("SELECT * FROM `map` WHERE Short=\""+number+"\"")
			listofout=[]
			for (a,b) in cursor:
				listofout.append(a)
			try:
				name=str(listofout.pop())
			except:
				name=""
			cv2.putText(im, "Faculty : "+ name, (x-50,y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2,cv2.LINE_8,False)
			cv2.namedWindow("im", cv2.WND_PROP_FULLSCREEN)
			cv2.setWindowProperty("im",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
			cv2.imshow('im',im)
			if(cv2.waitKey(1)==ord('y')):
				fnG.set(name)
				print(name)
				cv2.destroyAllWindows()
				cam.release()
				startDetectors()
				b=True
				break
			if(cv2.waitKey(1)==ord('q')):
				cv2.destroyAllWindows()
				
				b=True
				break
		if(nooframes==0):
				cv2.destroyAllWindows()
				cam.release()
				cursor.close()
				cnx.commit()
				cnx.close()
				b=True
				#if(name!=""):
				fnG.set(name)
				print(name)
				startDetectors()
		if(b==True):
			break