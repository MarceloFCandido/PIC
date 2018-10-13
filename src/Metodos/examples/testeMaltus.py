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

    # Criando eixo para plotagem
    ax = fig.add_subplot(111)

    # Criando plot
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.plot(T, np.transpose(Y[0:Y.size - 1:2]))

    # Configurando o titulo do grafico e suas legendas
    ax.set(title='Teste Maltus', ylabel='Populacao', xlabel='Tempo (t)')

    # Salvando o grafico em .png
    plt.savefig('Imagens/testeMaltus.png')

    # Mostrando o grafico
    plt.show()

# Definindo a classe Maltus
class EqMaltus(edo):
    def __init__(self, dimension):
        # Passando argumento para o construtor da superclasse
        edo.__init__(self, dimension)

    # Implementando o metodo evaluate (especifico para esse caso)
    def evaluate(self, sliceT, sliceY):
        e = 2.71828182846
        return e ** sliceT

def main():
    print "Esse programa busca plotar o grafico de e^x por meio do metodo de Runge-Kutta da 4a ordem"

    # Numero de passos
    N = 50

    # Intervalo maximo para T
    tMax = 10.0

    # Valores iniciais
    To = 0.0
    Yo = 1.0

    # Instanciando EDO
    EDO = EqMaltus(1)

    # chama a funcao para execucao do Runge-Kutta
    T, Y = RK4(EDO, tMax, N, To, Yo)

    #chama a funcao para plotagem do grafico
    plotar(T, Y)

main()
exit()
