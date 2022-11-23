import cv2
import numpy as np
import os
import PySimpleGUI as sg


def get_coords(coord_rosto, j):
    x = coord_rosto[j][0]
    y = coord_rosto[j][1]
    w = coord_rosto[j][2]
    h = coord_rosto[j][3]

    return x, y, w, h


def atualizar(img, j, coord_rosto):
    if len(coord_rosto) > 0:
        x, y, w, h = get_coords(coord_rosto, j)
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    propor = 260 / img.shape[0]
    altura = int(img.shape[0] * propor)
    largura = int(img.shape[1] * propor)
    dim = (largura, altura)
    img_resize = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    imgbytes = cv2.imencode(".png", img_resize)[1].tobytes()

    return imgbytes


def recortar_rosto(img, coord_rosto, j):
    x, y, w, h = get_coords(coord_rosto, j)
    rosto = img[y:y + h, x:x + w, :]
    resized_faces = cv2.resize(rosto, (50, 50))
    resized_bytes = cv2.imencode(".png", resized_faces)[1].tobytes()
    return resized_bytes, resized_faces


def remover_elemento(btn, miniaturas, vb, data_rostos):
    if miniaturas[btn] != vb:
        miniaturas[btn] = vb
        if btn < len(data_rostos):
            data_rostos.pop(btn)
        if btn < 10:
            for m in range(btn, 9):
                miniaturas[m] = miniaturas[m + 1]
        miniaturas[9] = vb

    return miniaturas


# Definindo imagens vazias para as telas no inicio

vazio = cv2.imread(r'.\data\empty.png')
vazio_bytes = cv2.imencode(".png", vazio)[1].tobytes()
# Importando Haarcascade para detecção de faces

facec = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
# Criando Arrays para o banco de dados
data_rostos = []
data_nomes = []
array_rostos = []
filename = None
coord_rosto = None
miniaturas = []
mini = 0
for i in range(10):
    miniaturas.append(vazio_bytes)
# Primeira coluna com espaço para a pasta e lista de arquivos

file_list_column = [
    [
        sg.Text("Pasta:"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
    ],
]
# Segunda coluna com o visualizador de imagens, miniaturas de rosto e botões para cadastro

image_viewer_column = [
    [sg.Text("Nome:"),
     sg.In(size=(25, 1), enable_events=True, key="-STRING-")],
    [sg.Text("Escolha uma imagem da lista ao lado:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Push(), sg.Image(filename=r'.\data\main_empty.png', key="-IMAGE-"), sg.Push()],
    [sg.Button('<-', enable_events=True, key="-ANT-"), sg.Push(),
     sg.Button('Selecionar', enable_events=True, key="-SELECT-"), sg.Push(),
     sg.Button('->', enable_events=True, key="-PROX-")],
    [sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_0-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_1-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_2-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_3-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_4-"), ],
    [sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_5-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_6-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_7-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_8-"),
     sg.Button(image_data=vazio_bytes, enable_events=True, key="-A_9-"),
     sg.Button("Cadastrar", enable_events=True, key="-CADASTRA-"),
     ]
]
# Layout com as duas colunas e um separador entre elas

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Cadastrar Rosto", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Se um endereço está no campo de pasta ele tenta listar os arquivos na pasta
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        # Exibe os files que terminam somente em png e jpg
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".png", ".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # Se um arquivo é escolhido
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            j = 0
            # Abre imagem converte em grayscale e tenta detectar rosto
            img_og = cv2.imread(filename)
            img = img_og.copy()
            img_cinza = cv2.cvtColor(img_og, cv2.COLOR_BGR2GRAY)
            coord_rosto = facec.detectMultiScale(img_cinza, 1.3, 4)
            # Faz conversão e redimensiona imagem para caber melhor na tela
            window["-IMAGE-"].update(data=atualizar(img, j, coord_rosto))
        except:
            pass
    if event == "-ANT-":
        if len(coord_rosto) > 0:
            img = img_og.copy()
            j -= 1
            if j < 0:
                j += len(coord_rosto)
            window["-IMAGE-"].update(data=atualizar(img, j, coord_rosto))

    if event == "-PROX-":
        if len(coord_rosto) > 0:
            img = img_og.copy()
            j += 1
            if j == len(coord_rosto):
                j = 0
            window["-IMAGE-"].update(data=atualizar(img, j, coord_rosto))

    if event == "-SELECT-":
        repetido = True
        if coord_rosto is not None:
            if len(coord_rosto) == 0:
                sg.popup('Rosto não detectado.', title="Aviso")
            elif mini > 9:
                sg.popup('Banco cheio, apague um rosto ou cadastre para liberar espaço.', title="Aviso")
            elif miniaturas[mini] == vazio_bytes:
                for rosto in miniaturas:
                    if rosto == recortar_rosto(img_og, coord_rosto, j)[0]:
                        sg.popup('Rosto já selecionado.', title="Aviso")
                        repetido = False
                minis = str(mini)
                if repetido:
                    miniaturas[mini] = recortar_rosto(img_og, coord_rosto, j)[0]
                    data_rostos.append(recortar_rosto(img_og, coord_rosto, j)[1])
                    window["-A_" + minis + "-"].update(image_data=miniaturas[mini])
                    mini += 1
    for k in range(10):
        ks = str(k)
        if event == "-A_" + ks + "-":
            if miniaturas[k] != vazio_bytes:
                mini -= 1
                miniaturas = remover_elemento(k, miniaturas, vazio_bytes, data_rostos)
                for i in range(k, 10):
                    st = str(i)
                    window["-A_" + st + "-"].update(image_data=miniaturas[i])


window.close()

"""for file in os.listdir(fotos):
    f = os.path.join(fotos, file)
    if os.path.isfile(f):
        img = cv2.imread(f)
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coord_rosto = facec.detectMultiScale(img_cinza, 1.3, 4)

        for (x, y, w, h) in coord_rosto:
            rostos = img[y:y + h, x:x + w, :]
            resized_faces = cv2.resize(rostos, (50, 50))
            data_rostos.append(resized_faces)
            cv2.imshow('image', rostos)
            cv2.threshold()
            nome = input('Quem é essa pessoa?:')
            data_nomes.append(nome)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            i += 1

data_rostos = np.asarray(data_rostos)
data_rostos = data_rostos.reshape(i, -1)
data_nomes = np.asarray(data_nomes)
data_nomes = data_nomes.reshape(i, -1)
print(data_nomes)
np.savetxt('data/data_rostos.csv', data_rostos, delimiter=",")
np.savetxt('data/data_nomes.csv', data_nomes, delimiter=",", fmt="%s")

fotos = np.loadtxt('data/data_rostos.csv', delimiter= ",")
print(fotos)
nomes = np.loadtxt('data/data_nomes.csv', delimiter= ",", dtype= str)
print(nomes) """
