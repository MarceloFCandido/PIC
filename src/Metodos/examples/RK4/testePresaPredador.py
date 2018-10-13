#!/usr/bin/python
#!-*- coding: utf8 -*-

# Importando bibliotecas nativas
import matplotlib.pyplot as plt
import numpy as np

# Importando bibliotecas desenvolvidas
from eqDiferencialOrdinaria import eqDiferencialOrdinaria as edo
from rungeKutta import rungeKutta4Ordem as RK4

# Plota o grafico a partir dos vetores criados
def plotar(T, Y):
    # Criando figura
    fig = plt.figure()

    # Adicionando eixos
    fig.add_axes()

    # Criando subplots nos eixos
    # Eixo para coelhos
    ax1 = fig.add_subplot(211)

    # Determinando o conteudo do eixo para coelhos
    plt.autoscale(enable=True, axis='x', tight=True)
    ax1.plot(T, np.transpose(Y[:1:10]))

    # Eixo para lobos
    ax2 = fig.add_subplot(212)

    # Determinando o conteudo do eixo para lobos
    ax2.plot(T, np.transpose(Y[1:2:10]))
    plt.autoscale(enable=True, axis='x', tight=True)

    # Determinando titulos e legendas dos graficos
    ax1.set(title='Teste Presa-Predador', ylabel='Pop. Pulgoes', xlabel='Tempo (t)')
    ax2.set(ylabel='Pop. Joaninhas', xlabel='Tempo (t)')

    # Salvando o grafico em .png
    plt.savefig('Imagens/testePresaPredador.png')

    # Plotando
    plt.show()

class EqPresaPredador(edo):
    # Inicializacao de variaveis sem valor numerico
    k = a = r = b = None

    def setK(self, k):
        self.k = k

    def getK(self):
        return self.k

    def setA(self, a):
        self.a = a

    def getA(self):
        return self.a

    def setR(self, r):
        self.r = r

    def getR(self):
        return self.r

    def setB(self, b):
        self.b = b

    def getB(self):
        return self.b

    def __init__(self, dimension, k, a, r, b):
        edo.__init__(self, dimension)

        self.setK(k)
        self.setA(a)
        self.setR(r)
        self.setB(b)

    def evaluate(self, T, Y):
        # Criacao de vetor para retorno
        dY = np.zeros(2)

        # Equacao para presas
        dY[0] = self.k * Y[0] - self.a * Y[0] * Y[1]

        # Equacao para predadores
        dY[1] = -1 * self.r * Y[1] + self.b * Y[0] * Y[1]

        return dY

def main():
    # Numero de passos
    N = 100000

    # Intervalo maximo para T
    tMax = 100.0

    # Parametros
    k = 2.0
    a = 0.01
    r = 0.5
    b = 0.0001

    # Valores iniciais
    To = 0.0    # Instante inicial
    Co = 2000   # Populacao inicial de presas
    Lo = 35     # Populacao inicial de predadores
    Yo = np.array([Co, Lo])

    # Instanciando sistema de EDO's Lotka-Voltera
    EDO = EqPresaPredador(2, k, a, r, b)

    # chama a funcao para execucao do Runge-Kutta
    T, Y = RK4(EDO, tMax, N, To, Yo)

    # Plotando as equacoes
    plotar(T, Y)

def intro():
    # Apresenta o algoritmo
    print "Esse algoritmo retorna a solucao para o seguinte problema de Lotka-Volterra:\n"
    print "Populacoes de pulgoes e joaninhas descritas pelas equacoes de Lotka-Volterra com\n"
    print "k = 2.0, a = 0.01, r = 0.5, b = 0.0001\n"
    print "Instante t = 0 com 2000 coelhos e 35 lobos."
    print "Fonte: Calculo. v.2. Stewart, James."

    # Faz as inicializacoes do programa pela funcao main
    main()

intro()
exit()
