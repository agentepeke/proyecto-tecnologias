import cv2
import os
import numpy as np
from pymongo import MongoClient
import pickle

# Conexión a la base de datos en la nube
mongodb_password = "pekecito"  # Contraseña de MongoDB Atlas
client = MongoClient(f"mongodb+srv://agentepeke:{mongodb_password}@cerradura.pymvanq.mongodb.net/?retryWrites=true&w=majority&appName=cerradura")
db = client.cerradura
collection = db.face_models

dataPath = 'C:/Users/agent/Documents/proyectoRF/Data'
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