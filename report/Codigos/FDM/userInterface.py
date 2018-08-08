#!/usr/bin/python2.7
#!-*- coding: utf8 -*-

'''
    Arquivo: userInterface.py
    Responsavel por receber as configuracoes do meio e da onda por parte do
    usuario e codifica-las em arrays binarios para que os demais scripts
    as recebam
'''

import numpy as np

print "Seja bem-vindo ao Wave Plotter 2000!"

# Informacoes para a criacao da onda e do meio
print "Insira o tamanho em x: "
Lx = input()

print "Insira o tamanho em y: "
Ly = input()

print "Insira o tempo maximo de animacao: "
tMax = input()

print "Insira o numero de pontos em x: "
Mx = input()

print "Insira o numero de pontos em y: "
Ny = input()

print "Insira o alpha: "
alpha = input()

print "Insira o omega: "
w = input()

print "Insira a Amplitude da onda: "
A = input()

print "Insira em a posicao em x do pico do pulso da onda: "
Xp = input()

print "Insira em a posicao em y do pico do pulso da onda: "
Yp = input()

print "Insira o tempo de pico do pulso da fonte: "
Tp = input()

print "Insira o numero de camadas que voce deseja: "
NL = input()

# Criando listas vazias para velocidades e interfaces
interfaces = np.zeros(NL, dtype=(float, 2))
velocidades = np.zeros(NL, dtype=(float, 3))
for i in range(NL - 1):
    print "Digite os coeficientes de velocidade da camada %d separados por virgula: ", i
    velocidades[i, :] = input()
    print "Digite os coeficientes da interface %d separados por virgula: ", i
    interfaces[i + 1, :] = input()
print "Digite os coeficientes de velocidade da camada %d separados por virgula: ", NL
velocidades[-1, :] = input()

# Criando um array com todos os valores recebidos
a = np.array([Lx, Ly, tMax, Mx, Ny, w, A, Xp, Yp, Tp, interfaces, velocidades])

# Salvando dados em um arquivo
np.save('data', a)
