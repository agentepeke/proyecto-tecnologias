import base64
import cv2
import os
import imutils
import numpy as np

from conexionMongo import get_client

personName = 'FernandoQ'
filesPath = os.environ['USERPROFILE'] + '/Documents/proyectoRF'
dataPath = filesPath + '/Data' #Cambia a la ruta donde hayas almacenado Data #Cambia a la ruta donde hayas almacenado Data
personPath = dataPath + '/' + personName

client = get_client()
db = client.cerradura
collection = db.face_frames

if not os.path.exists(personPath):
	print('Carpeta creada: ',personPath)
	os.makedirs(personPath)

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture(filesPath + "/" + personName + ".mp4")

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 0

while True:

	ret, frame = cap.read()
	if ret == False: break
	frame =  imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		rostro = auxFrame[y:y+h,x:x+w]
		rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
		# cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
		ret, buffer = cv2.imencode('.jpg', rostro)
		datos_imagen = buffer.tobytes()
		print(datos_imagen)
		model_entry = {
        "model_type": personName + str(count),
        "model_path": datos_imagen
		}
		collection.insert_one(model_entry)
		# nparr = np.frombuffer(datos_imagen, np.uint8)
		# imagen_recuperada = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		# cv2.imshow('imagen',imagen_recuperada)
		count = count + 1
	cv2.imshow('frame',frame)

	k =  cv2.waitKey(1)
	if k == 27 or count >= 300:
		break
print('Si llego aqui')
cap.release()
cv2.destroyAllWindows()