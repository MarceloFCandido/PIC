#!/usr/bin/python
#!-*- coding: utf8 -*-

# Importando bibliotecas nativas
import matplotlib.pyplot as plt
import numpy as np

# Importando bibliotecas desenvolvidas
from bibliotecaEDOs.eqDiferencialOrdinaria import eqDiferencialOrdinaria as edo
from bibliotecaMetodos.rungeKutta import rungeKutta4Ordem as RK4

# Plota o grafico a partir dos vetores criados
def plotar(T, Y):
    # Criando figura
    fig = plt.figure()

    # Adicionando eixos
    fig.add_axes()

    # Criando subplots nos eixos
    # Eixo para velocidade
    ax1 = fig.add_subplot(211)

    # Determinando o conteudo do eixo para velocidade
    plt.autoscale(enable=True, axis='x', tight=True)
    ax1.plot(T, np.transpose(Y[:1]))

    # Eixo para posicao
    ax2 = fig.add_subplot(212)

    # Determinando o conteudo do eixo para posicao
    ax2.plot(T, np.transpose(Y[1:2]))
    plt.autoscale(enable=True, axis='x', tight=True)

    # Configurando titulo do grafico e legendas dos eixos
    ax1.set(title='Teste Massa-Mola Homogeneo', ylabel='Velocidade', xlabel='Tempo (t)')
    ax2.set(ylabel='Posicao', xlabel='Tempo (t)')

    # Salvando a imagem do grafico
    plt.savefig("Imagens/testeMassaMola.png")

    # Plotando
    plt.show()

class EqMassaMola(edo):
    m = gamma = k = None

    def setM(self, m):
        self.m = m

    def getM(self):
        return self.m

    def setGamma(self, gamma):
        self.gamma = gamma

    def getGamma(self):
        return self.gamma

    def setK(self, k):
        self.k = k

    def getK(self):
        return self.k

    def __init__(self, dimension, m, gamma, k):
        # Inserindo dimensao do sistema
        edo.__init__(self, dimension)

        # Inserindo parametros
        self.setM(m)
        self.setGamma(gamma)
        self.setK(k)

    def evaluate(self, sliceT, sliceY):
        # Criacao de vetor para retorno
        valores = np.zeros(2)

        # Equacao para velocidade
        valores[0] = sliceY[1]

        # Equacao para posicao
        valores[1] = ((-self.gamma * sliceY[1] - self.k * sliceY[0]) / self.m)

        return valores

def main():
    # Numero de passos
    N = 10000

    # Define o intervalo maximo em t
    tMax = 50.0

    # Coeficientes da EDO
    m = 1.0       # Massa
    gamma = 0.125 # Coeficiente de amortecimento
    k = 1.0       # Constante elastica (da mola)

    # Valores iniciais
    To = 0.0  # Instante inicial
    Vo = 0.0  # Velocidade inicial
    Po = 2.0  # Posicao inicial
    Yo = np.array([Vo, Po])

    EDO = EqMassaMola(2, m, gamma, k)

    # chama a funcao para execucao do Runge-Kutta
    T, Y = RK4(EDO, tMax, N, To, Yo)

    # Plota os vetores
    plotar(T, Y)

def intro():
    # Apresenta o algoritmo
    print "Resolve a seguinte EDO"
    print "s'' + 0.125s' + s = 0"

    # Faz as inicializacoes do programa pela funcao main
    main()

intro()
exit()
