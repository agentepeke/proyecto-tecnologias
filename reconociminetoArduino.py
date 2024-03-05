import cv2
import os
import serial
import time

# Inicializa la comunicación serial con Arduino
arduino = serial.Serial('COM5', 9600)  # Reemplaza 'COMX' con el puerto serial correcto
time.sleep(2)  # Espera a que Arduino inicialice

dataPath = 'C:/Users/agent/Documents/proyectoRF/Data'
imagePaths = os.listdir(dataPath)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modeloLBPHFaceU.xml')

cap = cv2.VideoCapture(0)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

exit_flag = False  # Bandera para controlar la salida del bucle principal

def exit_program():
    global exit_flag
    exit_flag = True

while not exit_flag:
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        if result[1] < 70:
            cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # Envía mensaje a Arduino para encender el LED
            arduino.write(b'1')  # Envía '1' para encender el LED
        else:
            cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Envía mensaje a Arduino para apagar el LED
            arduino.write(b'0')  # Envía '0' para apagar el LED

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:  # Si se presiona la tecla 'ESC'
        exit_program()

cap.release()
cv2.destroyAllWindows()