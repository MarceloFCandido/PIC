#!/usr/bin/python2.7
#!-*- coding: utf8 -*-

import numpy as np
import matplotlib.pyplot as plt

print "Qual voce deseja plotar:\n 1 - C/ reflexao \n 2 - C/ fronteiras abertas?"
caminhoEscolhido = input()
camh = 'open'
if (caminhoEscolhido == 1):
    camh = 'reflect'
elif (caminhoEscolhido == 2):
    camh = 'open'
else:
    print 'Opcao inexistente'
    exit()

# Carregando arrays a partir de arquivos
X = np.load('../data/outputs/{caminho}/X.npy'.format(caminho=camh))
Y = np.load('../data/outputs/{caminho}/Y.npy'.format(caminho=camh))
V = np.load('../data/outputs/{caminho}/V.npy'.format(caminho=camh))
params = np.load('../data/configs/params.npy')
markers = np.load('../data/configs/markers.npy')

# Criando figura
fig = plt.figure()

# Adicionando eixos
fig.add_axes()

# Criando eixo para plotagem
ax = fig.add_subplot(111)

# Formando base para o plot (?)
[Y, X] = np.meshgrid(Y,X)

# Buscando o maior valor de U para fixar o eixo em z
M = max(abs(V.min()), abs(V.max()))

# Criando plot
plot = ax.contourf(X, Y, V, 20, cmap=plt.cm.seismic, vmin=-M, vmax=M)

# Desenhando a barra de cores
plt.colorbar(plot)

# Definindo limites para o plot
plt.xlim(0., params[0])
plt.ylim(params[1], 0.) # para inverter o eixo y

# Plotando as Camadas
for i in range(0, markers.size / 2):
    ax.plot((0., params[0]), (markers[i][0], markers[i][1]), '-k')

# Configurando o titulo do grafico e suas legendas
ax.set(title='Velocidades', ylabel='Y', xlabel='X')

# Definindo caminho da plotagem
caminho = '../data/images/Velocidades.png'

# Salvando a imagem
plt.savefig(caminho)
