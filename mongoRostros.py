import base64
import os
from pymongo import MongoClient
import gridfs
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

mongodb_password = "pekecito"  # Contraseña de MongoDB Atlas
client = MongoClient(f"mongodb+srv://agentepeke:{mongodb_password}@cerradura.pymvanq.mongodb.net/?retryWrites=true&w=majority&appName=cerradura")
db = client.cerradura
collection = db.face_models

filesPath = os.environ['USERPROFILE'] + '/Documents/proyectoRF'
dataPath = filesPath + '/Data' #Cambia a la ruta donde hayas almacenado Data
peopleList = os.listdir(dataPath)
labels = []
facesData = []
label = 0
fid = ""
for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir
	print('Leyendo las imágenes')
	for fileName in os.listdir(personPath):
		img = personPath+'/'+fileName
        # Lectura de la imagen
        with open(img, "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            decoded = encoded.decode('utf-8')
        # Carga de la imagen en mongoDB
        fs = gridfs.GridFS(collection)
        file_id = fs.put(encoded)
        collection.images.insert_one({"file_id": file_id})

        for item in collection.images.find({"filename": filename}):
            fid = item["file_id"]
            
        if fid != "":
            outputdata = fs.get(fid).read()
            print(outputdata)
	label = label + 1