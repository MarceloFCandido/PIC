#!/usr/bin/python2.7
#!-*- coding: utf8 -*-

'''
    Arquivo: snapshoter.py
    Responsavel por recolher os dados produzidos por calculator.py e criar as
    imagens que representam os dados numericos da simulacao de progapacao de
    onda
'''

import numpy as np
import matplotlib.pyplot as plt

# Carregando arrays a partir de arquivos
X = np.load('data/X.npy')
Y = np.load('data/Y.npy')
U = np.load('data/U.npy')

print "Quantos snapshots voce deseja?"
N = input()

# Definindo passo
h = U.shape[2] / N

counter = 0

# Criando figura
fig = plt.figure()

# Adicionando eixos
fig.add_axes()

# Criando eixo para plotagem
ax = fig.add_subplot(111)

# Formando base para o plot (?)
[Y, X] = np.meshgrid(Y, X)

# TODO: Trocar isso por entradas do introdutor
markers = np.array([(0., 0.), (1.5, 1.9), (3., 2.3), (4., 3.8), (6.5, 8.)], dtype=(float, 2))

# Invertendo o eixo y
plt.gca().invert_yaxis()

# Cria as imagens de N em N quadros
for i in range(h, U.shape[2], h):

    # Buscando o maior valor de U para fixar o eixo em z
    M = max(abs(U.min()), abs(U.max()))

    # Criando plot
    ax.contourf(X, Y, U[:,:,i], 20, cmap=plt.cm.seismic, vmin=-M, vmax=M )

    # Plotando as Camadas
    for i in range(0, markers.size / 2):
        # TODO: Trocar o 15. por uma variavel passada pelo introdutor
        ax.plot((0., 15.), (markers[i][0], markers[i][1]), '-k')

    # Configurando o titulo do grafico e suas legendas
    ax.set(title='Onda em 2D', ylabel='Y', xlabel='X')

    # Definindo titulo da plotagem
    titulo = "Teste 0%d - MDF - 1D" % counter

    # Definindo caminho da plotagem
    caminho = 'images/Teste0%d.png' % counter

    # Incrementando o contador
    counter += 1

    # Salvando a imagem
    plt.savefig(caminho)
