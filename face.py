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
			
def destartDe(strpid):
	if(scheduler!=None):
		scheduler.remove_job(strpid)
	stoperofdet.set("stop")
	print(stoperofdet)
def printd(event=None):
	global tableoftab
	global arra
	print("nhvn")
	for i in range(1,4):
		arra.append([str(i*10+1),str((i+1)*10+i+1)])							
		try:
			hourint,minint=map(int,tableoftab[i][1].get().split(":"))
		except:
			break
		date = parse(time.ctime())
		print(date)
		diff=(minint*60+hourint*3600)-((date.minute*60+date.hour*3600+date.second))
		scheduler.add_job(startDetectorfaculty, 'interval', seconds=diff,id=arra[i-1][0],args=(arra[i-1][0],))
		hourout,minout=map(int,tableoftab[i][2].get().split(":"))
		diff=(minout*60+hourout*3600)-((date.minute*60+date.hour*3600+date.second))
		scheduler.add_job(destartDe, 'interval', seconds=diff,id=arra[i-1][1],args=(arra[i-1][1],))
	scheduler.start()
def Shortner(FullName):
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
	select_q="SELECT * FROM `map`"
	cursor.execute(select_q)
	number=0
	for (a,b) in cursor:
		number=b
	number=str(hex(int(number,16)+1))[2:]
	number='0'*(4-len(number))+number
	add_stuednt = "INSERT INTO map (Name, Short) VALUES (%s, %s)"
	data_student = (FullName,number)
	cursor.execute(add_stuednt, data_student)
	cnx.commit()
	cursor.close()
	cnx.close()
	return number
def startGen(event=None):
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
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('Classifiers/face.xml')
    i=0
    offset=50
    name=nameVar.get()
    sId=studentoId.get()
    listofclass=classNames.get().split(",")
    print(name,classNames)
    for kl in listofclass:
        insert_q="INSERT INTO facclass VALUES (%s, %s)"
        cursor.execute(insert_q,(name,kl))
        create="CREATE TABLE `attend`.`"+name+"_"+kl+"` ( `ID` VARCHAR(20) NOT NULL  ) ENGINE = InnoDB;"
        cursor.execute(create)
    cnx.commit()
    cursor.close()
    cnx.close()
    while(True):
        ret,im =cam.read()
        if(not ret):
            continue
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            i=i+1
            cv2.imwrite("dataSet/face-"+str(name) + "#" + str(sId) +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
            cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
            cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
            cv2.waitKey(100)
        if(i>33):
            cam.release()
            cv2.destroyAllWindows()
            break
def startGens(event=None):
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('Classifiers/face.xml')
    i=0
    offset=50
    name=nameVar.get()
    clasa=classNames.get()
    sId=studentoId.get()
    print(sId)
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
    cursor.execute("INSERT INTO stuclass (Name,Class) VALUES ('"+name+"','"+clasa+"')")
    cnx.commit()
    cursor.close()
    cnx.close()
    #print(name)
    while(True):
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            i=i+1
            xyzim=gray[y-offset:y+h+offset,x-offset:x+w+offset]
            cv2.equalizeHist(xyzim)
            cv2.imwrite("dataSetS/face-"+str(name) + "#" + str(sId) +'.'+ str(i) + ".jpg", xyzim)
            cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
            cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
            cv2.waitKey(100)
        if(i>50):
            cam.release()
            cv2.destroyAllWindows()
            break			
def get_images_and_labels(path):
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
	image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # images will contains face images
	images = []
    # labels will contains the label that is assigned to the image
	labels = []
	getN=None
	firstTime=True
	inoofima=0
	for image_path in image_paths:
        # Read the image and convert to grayscale
		image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
		image = np.array(image_pil, 'uint8')
        # Get the label of the image
		FullName , getN = os.path.split(image_path)[1].split(".")[0].replace("face-", "").upper().split("#")
		# Detect the face in the image
		if(firstTime):
			firstTime=False
			cursor.execute("INSERT INTO `map`  VALUES ('"+FullName+"','"+getN+"')")
			cnx.commit()
			cursor.close()
			cnx.close()
		print("GetN",getN)
		if(inoofima==51):
			inoofima=0
		number=int(''.join(str(ord(c)) for c in getN.upper()),10)
		cascadePath = "Classifiers/face.xml"
		faceCascade = cv2.CascadeClassifier(cascadePath);
		faces = faceCascade.detectMultiScale(image)
		inoofima+=1
		# If face is detected, append the face to images and the label to labels
		for (x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			labels.append(number)
			#cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
			cv2.waitKey(10)
    # return the images list and labels list
	return images, labels


def startTrain(event=None):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataSet'
    images, labels = get_images_and_labels(path)
    cv2.imshow('test',images[0])
    cv2.waitKey(1)
    recognizer.train(images, np.array(labels))
    recognizer.write('trainer/trainer.yml')
    cv2.destroyAllWindows()

def startTrains(event=None):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataSets'
    images, labels = get_images_and_labels(path)
    cv2.imshow('test',images[0])
    cv2.waitKey(1)
    recognizer.train(images, np.array(labels))
    recognizer.write('trainer/trainers.yml')
    cv2.destroyAllWindows()	
def startDetector(event=None):
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
		print(nooframes)
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
				if(name!=""):
					fnG.set(name)
					startDetectors()
		if(b==True):
			break
def CSV(event=None):
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
	tabname=nameVar.get()+"_"+classNames.get()
	selectcol="show columns from attend."+tabname
	cursor.execute(selectcol)
	soham=""
	for x in cursor:
		soham+=x[0]+","
	soham+='\n'
	select_csv="SELECT * FROM `"+tabname+"`"
	cursor.execute(select_csv)
	for x in cursor:
		for okokok in x:
			if(okokok!=None):soham+=okokok+','
			else:soham+=","
		soham+='\n'
	cursor.close()
	cnx.commit()
	cnx.close()
	fileName=nameVar.get()+' '+datetime.now().ctime()+'.csv'
	fileName=fileName.replace(":","")
	fileName=fileName.replace(" ","")
	#print(fileName)
	myFile = open(""+fileName+"", 'w')
	myFile.write(soham)
	myFile.close()
	os.system('start '+''+fileName+'')
def startDetectors(event=None):
	cnx = mysql.connector.connect(user='root',password="",host="localhost")
	cursor = cnx.cursor()
	DB_NAME = 'attend'
	date = parse(time.ctime())
	try:
		cnx.database = DB_NAME
	except mysql.connector.Error as err:
		if(err.errno == errorcode.ER_BAD_DB_ERROR):
			create_database(cursor)
			cnx.database = DB_NAME
		else:print(err);
	cursor.execute("SELECT * FROM `facclass` WHERE Name=\""+fnG.get()+"\"")
	clasthin=''
	for (ab,ck) in cursor:
		clasthin=ck
	thistime=time.ctime()
	cursor.execute("ALTER TABLE `"+fnG.get()+"_"+clasthin+"` ADD `"+thistime+"` VARCHAR(20) ")
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer/trainers.yml')
	cascadePath = "Classifiers/face.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath);
	path = 'dataSets'
	cam = cv2.VideoCapture(0)
	fn='attendance'
	b=False
	arrayofar={}
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(im,"detector",1, 1, 0, 1, 1)
    #font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font
	while(True):
		ret, im =cam.read()
		if(not ret):
			#print("c")
			continue		
		gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
		for (x,y,w,h) in faces:
			nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
			if conf > 50 :
				name=""
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
				select_q="SELECT * FROM `stuclass` WHERE Name=\""+name+"\""
				cursor.execute(select_q)
				if( name not in arrayofar.keys()):
					arrayofar.update({name:0})
				classno=None
				for (a,b) in cursor:
					classno=b
				if(classno!=None):
					try:
						update_q="UPDATE `"+fnG.get()+"_"+str(classno)+"` SET `"+thistime+"`='P' WHERE ID=\""+number+"\""
						select_q="SELECT * FROM `"+fnG.get()+"_"+str(classno)+"` WHERE ID=\""+number+"\""
						cursor.execute(select_q)
						cfsel=0
						for spofkopsd in cursor:
							cfsel+=1
						if(cfsel==0):
							print(fnG.get()+"_"+str(classno))
							add_stuednt = "INSERT INTO "+fnG.get()+"_"+str(classno)+" (ID, `"+thistime+"`) VALUES (%s, %s)"
							data_student = (number, 'P')
							cursor.execute(add_stuednt, data_student)
							print("excuted")
						else:
							cursor.execute(update_q)
						arrayofar.update({name:1})
					except mysql.connector.errors.ProgrammingError:
						arrayofar.update({name:0})
			else:
				cv2.rectangle(im,(x-50,y-50),(x+w+20,y+h+20),(255,255,255),1)
				name="unknown"
    		#cv2.putText(im,str(nbr_predicted), (x,y+h),font, 255,(225,0,0))		#Draw the text
			cv2.putText(im, "Student : "+name, (x-50,y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2,cv2.LINE_8,False)
			cv2.imshow('im',im)
			print(name)	
			if(cv2.waitKey(1)==ord('q')):
				cv2.destroyAllWindows()
				cam.release()
				cursor.close()
				cnx.commit()
				cnx.close()
				print("cnx closed")
				b=True
				break
		if(stoperofdet.get()=="stop"):
			cv2.destroyAllWindows()
			cam.release()
			cursor.close()
			cnx.commit()
			cnx.close()
			print("cnx closed")
			stoperofdet.set("")
			b=True
			break
		if(b==True):
			break
	noone=0
	nozero=0
	print(arrayofar)
	for b in arrayofar.values():
		if(b==0):
			nozero+=1
		else:
			noone+=1
	filename="log "+datetime.now().strftime("%d %b %Y")+".txt"
	filename=filename.replace(":","")
	filename=filename.replace(" ","")
	
	logfile=open(filename,"w")
	logfile.write(str(noone)+" Accpted\n"+str(nozero)+" Rejected\n"+"total students detected "+str(noone+nozero))
	logfile.close()
	print(filename)
	os.system('start '+''+filename+'')
def getData1(event=None):
	print("getData1")
def getData2(event=None):
	print("getData2")
	global nameVar1,nameVar2,optFrame,root1,root
	
	if(nameVar1.get()=="a" and nameVar2.get()=="a"):
		print("x")
		root1.destroy()
		root=Tk()

		btn = StringVar()
		globalId=StringVar()
		
#full()
#globalBol=BooleanVar()
#root.geometry("390x300+300+350")
#root.resizable(width=False, height=False)
		def full(event=None):
			state = True
			root.attributes("-fullscreen", state)
	#state = not state
    #screen()        	
		#full()
		optFrame=LabelFrame(root,text="Options",font=("times new roman",23),fg="black",padx=40,pady=20)
		def close_window(event=None):
			global root
	
			root.destroy()
		optFrame.pack(side=LEFT,fill=BOTH, expand=YES)

#----------making optFrame----------


##who are you
#whoLF=LabelFrame(optFrame, text="Who are you?",bg="#cd5c5c",fg="grey",padx=617, pady=65,font=("times new roman", 18))
#whoLF.grid(row=0, column=0, sticky=W)
#facRadio=Radiobutton(whoLF, text="Faculty",bg="grey",font=("times new roman", 17),fg="grey", value="fac",variable=btn,indicatoron=0)
#facRadio.grid(row=0, column=1, sticky=W)
#stuRadio=Radiobutton(whoLF, text="Student",bg="grey",font=("times new roman", 17),fg="grey", value="stu",variable=btn,indicatoron=0)
#stuRadio.grid(row=0, column=2, sticky=W)
#separator = (height=2, bd=1, relief=SUNKEN)
#separator.pack(fill=X, padx=5, pady=5)

		#changes
		info=LabelFrame(optFrame, text="Personal details",fg="black",font=("times new roman", 18))
		info.grid(row=1, column=0, sticky=W)
		def getData(event=None):
			name=nameVa.get()
			clas=className.get()
			id=studentId.get()
			global nameVar,classNames,studentoId
			nameVar.set(name)
			classNames.set(clas)
			studentoId.set(id)
		
		
		
		
		
		Label(info,text="Name:",font=("times new roman", 17),fg="black").grid(row=0,column=0,padx=0)
		nameVa=StringVar()
		className=StringVar()
		studentId=StringVar()
		nameEntry = Entry(info, textvariable=nameVa,font=("times new roman",17))
		nameEntry.grid(row=0,column=1,padx=20,ipady=2)
		getDataButton = Button(info, text="Submit",bg="grey",font=("times new roman", 17),fg="white")
		getDataButton.grid(row=1,padx=20,pady=10,column=1)
		getDataButton.bind("<Button-1>", getData)
		Label(info,text="birth date:",font=("times new roman", 17),fg="black").grid(row=0,column=2,padx=0)
		classEntry = Entry(info, textvariable=className,font=("times new roman",17))
		classEntry.grid(row=0,column=3,padx=10,ipady=2)
		Label(info,text="Email Id:",font=("times new roman", 17),fg="black").grid(row=0,column=4,padx=0)
		idEntry = Entry(info, textvariable=studentId,font=("times new roman",17))
		idEntry.grid(row=0,column=5,padx=10,ipady=2)
		#changend
#One Button for all things

		recg=LabelFrame(optFrame, text="Recognize",fg="black",padx=245,pady=5,font=("times new roman", 18))
		recg.grid(row=3,column=0,sticky=W)
		Label(recg,text="Registration:",font=("times new roman", 17),fg="black").grid(row=1,column=0,sticky=W)
#Label(recg,text="Registration :",padx=5,bg="grey",font=("times new roman", 17),fg="white").grid(row=1,column=0,sticky=W)
		genButtonf = Button(recg, text="Admin",bg="grey",font=("times new roman", 17),fg="white")
		genButtonf.grid(row=1,column=1,sticky=W, padx=20)
		genButtonf.bind("<Button-1>", startGen)
		genButtons = Button(recg, text="guest",bg="grey",font=("times new roman", 17),fg="white")
		genButtons.grid(row=1,column=2,sticky=W)
		genButtons.bind("<Button-1>", startGens)

		Label(recg,text="Training:",font=("times new roman", 17),fg="black").grid(row=2,column=0,sticky=W)
		trainButtonf = Button(recg, text="Admin Trainer",bg="grey",font=("times new roman", 17),fg="white")
		trainButtonf.grid(row=2,column=1,sticky=W,padx=20)
		trainButtonf.bind("<Button-1>", startTrain)
		trainButtons = Button(recg, text="guest Trainer",bg="grey",font=("times new roman", 17),fg="white")
		trainButtons.grid(row=2,column=2,sticky=W,pady=10)
		trainButtons.bind("<Button-1>", startTrains)

		Label(recg,text="Recognizer:",font=("times new roman", 17),fg="black").grid(row=3,column=0,sticky=W)
		recgButton = Button(recg, text="Start",bg="grey",font=("times new roman", 17),fg="white")
		recgButton.grid(row=3,column=1,sticky=W,padx=20)
		recgButton.bind("<Button-1>", lambda e : startDetectorfaculty(None))
		def close_window(event=None):
			global root
			root.destroy()
##To Get Out Of The Program
		Kill=LabelFrame(optFrame, text="Close and Excel file Generation",fg="black",padx=365, pady=10,font=("times new roman", 18))
		Kill.grid(row=4, column=0, sticky=W)
		button = Button(Kill, text="   EXIT   ",bg="grey",font=("times new roman", 17),fg="white")
		button.grid(row=4,column=1,sticky=W)
		button.bind("<Button-1>", close_window)
		button = Button(Kill, text="   CSV   ",bg="grey",font=("times new roman", 17),fg="white")
		button.grid(row=4,column=2,sticky=W,padx=20)
		button.bind("<Button-1>", CSV)
#trainButton.bind("<Button-1>", Kill Me)

		# table=LabelFrame(optFrame, text="Time Table",fg="grey",padx="133",pady="10",font=("times new roman",15))
		# table.grid(row=0,column=0,sticky=W)
		# Label(table,text="Starting Time",bg="grey",font=("times new roman", 17),fg="white").grid(row=0,column=1)
		# Label(table,text="Ending Time",bg="grey",font=("times new roman", 17),fg="white").grid(row=0,column=2)
		# Label(table,text="Faculty",bg="grey",font=("times new roman", 17),fg="white").grid(row=0,column=3)
		# Label(table,text="Subject",bg="grey",font=("times new roman", 17),fg="white").grid(row=0,column=4)
		# Label(table,text="Slot 1",bg="grey",font=("times new roman", 17),fg="white").grid(row=1,column=0)
		# Label(table,text="Slot 2",bg="grey",font=("times new roman", 17),fg="white").grid(row=2,column=0)
		# Label(table,text="Slot 3",bg="grey",font=("times new roman", 17),fg="white").grid(row=3,column=0)
		# for i in range(1,4): #Rows
		# 	tableoftab.append([])
		# 	if(i==1):
		# 		tableoftab.append([])
		# 	for j in range(1,5): #Columns
		# 		if(j==1):
		# 			tableoftab[i].append("")
		# 		uj = Entry(table, text="")
		# 		tableoftab[i].append(uj)
		# 		uj.grid(row=i, column=j)
		# button = Button(table, text="Submit",bg="grey",font=("times new roman", 17),fg="white")
		# button.grid(row=6,column=2,pady="15")
		# button.bind("<Button-1>", printd)
		mainloop()
root1=Tk()
root1.title("ADMIN PANEL")
def close_windown(event=None):
	global root1
	
	root1.destroy()
fnG=StringVar()
classNames=StringVar()
nameVar = StringVar()
studentoId = StringVar()
stoperofdet=StringVar()
stoperofdet.set("")
adminFrame=LabelFrame(root1,text="Admin Login",font=("times new roman",23),fg="black")
adminFrame.pack(side=BOTTOM,fill=BOTH,expand=YES)
Label(adminFrame,text="USERNAME:",font=("times new roman", 17),fg="black").grid(row=0,column=0,sticky=W,padx=15)
nameVar1 = StringVar()
nameEntry1 = Entry(adminFrame, textvariable=nameVar1,font=("times new roman",17))
nameEntry1.grid(row=0,column=1,padx=20,ipady=2)
#getDataButton = Button(info, text="Submit",bg="grey",font=("times new roman", 17),fg="grey")
#getDataButton.grid(row=1,padx=20,pady=20,column=1,sticky=W)
#getDataButton.bind("<Button-1>", getData1)
Label(adminFrame,text="PASSWORD:",font=("times new roman", 17),fg="black").grid(row=3,column=0,sticky=W,padx=15,pady=10)
nameVar2 = StringVar()
nameEntry2 = Entry(adminFrame, textvariable=nameVar2,font=("times new roman",17))
nameEntry2.grid(row=3,column=1,padx=35,ipady=2,pady=10)
getDataButton1 = Button(adminFrame, text="Submit",bg="grey",font=("times new roman", 17),fg="white")
getDataButton1.grid(row=4,padx=20,pady=20,column=1,sticky=W)
getDataButton1.bind("<Button-1>", getData2)
Label(adminFrame,text="Recognizer:",font=("times new roman", 17),fg="black").grid(row=0,column=2,sticky=W)
recgButton = Button(adminFrame, text="Start",bg="grey",font=("times new roman", 17),fg="white")
recgButton.grid(row=0,column=3,sticky=E,padx=10,pady=9)
recgButton.bind("<Button-1>", lambda e : startDetectorfaculty(None))
button2 = Button(adminFrame, text="   EXIT   ",bg="grey",font=("times new roman", 17),fg="white")
button2.grid(row=4,column=2,sticky=W)
button2.bind("<Button-1>", close_windown)

mainloop()
