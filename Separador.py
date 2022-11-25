import cv2
import numpy as np
import os
import PySimpleGUI as sg
from sklearn.neighbors import KNeighborsClassifier


nomes = []
rostos = []

banco_nomes = np.genfromtxt("./data/banco_nomes.csv", delimiter=",", dtype=str)
banco_rostos = np.genfromtxt("./data/banco_rostos.csv", delimiter=",")
facec = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
i = 0
print('Shape of Faces matrix --> ', banco_rostos.shape)
print(banco_nomes.shape)
knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn.fit(banco_rostos, banco_nomes)
steve = r".\dataset\rainn_teste"

for i in range(86):
    teste = os.path.join(steve, os.listdir(steve)[i])
    imagem_teste = cv2.imread(teste)
    img_cinza = cv2.cvtColor(imagem_teste, cv2.COLOR_BGR2GRAY)
    coord_rosto = facec.detectMultiScale(img_cinza, 1.3, 4)
    for (x, y, w, h) in coord_rosto:
        face = imagem_teste[y:y + h, x:x + w, :]
        face_r = cv2.resize(face, (50, 50)).flatten().reshape(1,-1)
        text = knn.predict(face_r)
        print(text)
        nomes.append(text)

print(nomes.count("Dwight"))
print(len(nomes))

"""rostos_cad = np.asarray(rostos)
rostos_cad = rostos_cad.reshape(len(rostos), -1)
nomes_cad = np.asarray(nomes)
nomes_cad = nomes_cad.reshape(len(nomes), -1)

banco_rostos = np.concatenate((banco_rostos, rostos_cad), axis=0)
banco_nomes = np.concatenate((banco_nomes, nomes_cad), axis=0)
np.savetxt('data/banco_rostos.csv', banco_rostos, delimiter=",")
np.savetxt('data/banco_nomes.csv', banco_nomes, delimiter=",", fmt="%s")"""




# Define KNN functions


# def distance(x1, x2):
#     d = np.sqrt(((x1 - x2) ** 2).sum())
#     return d


# def knn(xt, X_train=faces, y_train=labels, k=5):
#     vals = []

#     for ix in range(len(labels)):
#         d = distance(X_train[ix], xt)
#         vals.append([d, y_train[ix]])

#     sorted_labels = sorted(vals, key=lambda z: z[0])
#     neighbours = np.asarray(sorted_labels)[:k, -1]

#     freq = np.unique(neighbours, return_counts=True)

#     # freq[0] is list of names and freq[1] is list of counts
#     return freq[0][freq[1].argmax()]





"""directory = r"./fotos"
pasta = r"./fotos/resultado"
if not os.path.exists(pasta):
    os.mkdir(pasta)

for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith((".png", ".jpg")):
        file = os.path.join(directory, filename)
        img = cv2.imread(file)
        new_file = os.path.join(pasta, filename)
        cv2.imwrite(new_file, img)"""


