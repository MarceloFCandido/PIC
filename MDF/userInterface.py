#!/usr/bin/python2.7
#!-*- coding: utf8 -*-

import numpy as np

print "Seja bem-vindo ao plotter de ondas via MDF"

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

# Criando um array com todos os valores recebidos
a = np.array([Lx, Ly, tMax, Mx, Ny, w, A, Xp, Yp, Tp])

print "Digite o numero de interfaces/velocidades (interfaces + 1): "
N = input()

vl = np.zeros(N + 1, dtype=(float, 3))
it = np.zeros(N, dtype=(float, 2))
print "ATENCAO! As proximas entradas devem ser separadas por virgula \',\'."
for i in range(N):
    print "Digite os coeficientes da funcao de velocidade da camada ", i + 1, \
    ":"
    vl[i] = input()
    print "Digite os coeficientes da reta que descreve a interface ", i + 1, \
    ":"
    it[i] = input()
print "Digite os coeficientes da funcao de velocidade da camada ", N, \
":"
vl[N] = input()

# Salvando configuracoes da onda e do meio em arquivos
np.save('waveConfigs.npy', a)
np.save('velocities.npy', vl)
np.save('interfaces.npy', it)
