from urllib.parse import quote_plus
import cv2
import os
import numpy as np
from pymongo import MongoClient
import pickle
from dotenv import load_dotenv

from conexionMongo import get_client

# Conexión a la base de datos en la nube
 # Contraseña de MongoDB Atlas
client = get_client()
db = client.cerradura
collection = db.face_models

filesPath = os.environ['USERPROFILE'] + '/Documents/proyectoRF'
dataPath = filesPath + '/Data' #Cambia a la ruta donde hayas almacenado Data
peopleList = os.listdir(dataPath)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = os.path.join(dataPath, nameDir)

    for fileName in os.listdir(personPath):
        labels.append(label)
        facesData.append(cv2.imread(os.path.join(personPath, fileName), 0))

    label += 1

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))
print("Modelo entrenado.")

# Guardar el modelo en archivos temporales
model_files = []
for i in range(0, len(facesData), 1000):  # Dividir el modelo en partes de 1000 elementos
    face_recognizer.train(facesData[i:i+1000], np.array(labels[i:i+1000]))
    model_file = f'modeloLBPHFaceejemplo_{i}.xml'
    face_recognizer.save(model_file)
    model_files.append(model_file)

# Almacenar los archivos del modelo en la base de datos
for model_file in model_files:
    model_entry = {
        "model_type": "LBPH",
        "model_path": model_file  # Almacenar solo la ruta del archivo en la base de datos
    }
    collection.insert_one(model_entry)
    print(f"Modelo almacenado en la base de datos: {model_file}")