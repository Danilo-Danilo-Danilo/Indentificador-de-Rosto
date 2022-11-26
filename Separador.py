import cv2
import numpy as np
import os
import PySimpleGUI as sg
from sklearn.neighbors import KNeighborsClassifier


nomes = []
rostos = []
# Importando banco de dados
# Para fazer: check se eles existem
banco_nomes = np.genfromtxt("./data/banco_nomes.csv", delimiter=",", dtype=str)
banco_rostos = np.genfromtxt("./data/banco_rostos.csv", delimiter=",")
# Carrega detector de rosto
facec = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# Define o classificador knn e coloca os bancos de dados nele
knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn.fit(banco_rostos, banco_nomes)
# Para fazer: interface com opção de escolher as pastas
directory = r"./fotos/teste"
pasta = r"./fotos/resultado/"

# Se pasta de resultado não existe cria uma pasta para colocar fotos classificadas
if not os.path.exists(pasta):
    os.mkdir(pasta)
# Pega cada arquivo da pasta selecionada e confere se é imagem
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith((".png", ".jpg")):
        # classif vai ser parte do nome do arquivo, vai possuir todas as classes identificadas na foto
        classif = ""
        # pessoas é todas as classes identificadas na foto
        pessoas = []
        # abre a foto e detecta todos os rostos
        file = os.path.join(directory, filename)
        img = cv2.imread(file)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coord_rosto = facec.detectMultiScale(img_cinza, 1.3, 4)
        # para cada rosto dá uma classificação e adiciona a classe no array de pessoas
        for (x, y, w, h) in coord_rosto:
            face = img[y:y + h, x:x + w, :]
            face_r = cv2.resize(face, (50, 50)).flatten().reshape(1, -1)
            text = knn.predict(face_r)
            nome = text[0]
            # checa se pessoa caiu no grupo dos não cadastrados
            if nome == "0":
                nome = "N cadastrado"
            classif = (classif + "(" + nome + ") ")
            pessoas.append(nome)
        # se não detectou nenhuma pessoa salva como uma classe sem rosto
        if len(pessoas) < 1:
            classif = "Sem rosto"
            pessoas.append("Sem rosto")
        new_name = classif + "-" + filename
        # para fazer: barra de progessão
        # para cada pessoa detectada checa se já existe uma pasta com aquele nome
        # se não cria a pasta
        # e salva foto com nome de todas as classes e depois o nome original
        for i in pessoas:
            new_dir = os.path.join(pasta, i)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            new_file = os.path.join(new_dir, new_name)
            cv2.imwrite(new_file, img)




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








