#!/usr/bin/python2.7
#!-*- coding: utf8 -*-

import numpy as np

print "Seja bem-vindo ao Wave Plotter 2000!"

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

# Salvando dados em um arquivo
np.save('data', a)
