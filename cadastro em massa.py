import cv2
import numpy as np
import os
import PySimpleGUI as sg
from sklearn.neighbors import KNeighborsClassifier


nomes = []
rostos = []
i = 1
banco_nomes = np.genfromtxt("./data/banco_nomes.csv", delimiter=",", dtype=str)
banco_nomes = banco_nomes.reshape(len(banco_nomes), -1)
banco_rostos = np.genfromtxt("./data/banco_rostos.csv", delimiter=",")
facec = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# print('Shape of Faces matrix --> ', banco_rostos.shape)
# print('Shape of Names matrix --> ', banco_nomes.shape)

steve = r".\fotos\Randoom"
print("Arquivos carregados")
for filename in os.listdir(steve):
    if os.path.isfile(os.path.join(steve, filename)) and filename.lower().endswith((".png", ".jpg")):
        file = os.path.join(steve, filename)
        img = cv2.imread(file)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coord_rosto = facec.detectMultiScale(img_cinza, 1.3, 4)
        for (x, y, w, h) in coord_rosto:
            face = img[y:y + h, x:x + w, :]
            face_r = cv2.resize(face, (50, 50))
            rostos.append(face_r)
            nomes.append("0")
    print (i)
    i += 1
rostos_cad = np.asarray(rostos)
rostos_cad = rostos_cad.reshape(len(rostos), -1)
nomes_cad = np.asarray(nomes)
nomes_cad = nomes_cad.reshape(len(nomes), -1)

banco_rostos = np.concatenate((banco_rostos, rostos_cad), axis=0)
banco_nomes = np.concatenate((banco_nomes, nomes_cad), axis=0)
np.savetxt('data/banco_rostos.csv', banco_rostos, delimiter=",")
np.savetxt('data/banco_nomes.csv', banco_nomes, delimiter=",", fmt="%s")
