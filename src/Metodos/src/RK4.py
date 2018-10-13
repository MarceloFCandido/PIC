#!-*- coding: utf8 -*-

import numpy as np

def rungeKutta4Ordem(EDO, tMax, N, To, Yo, paramRK = 0):
    '''
        Definicao do metodo de Runge-Kutta de 4 ordem
        Recebe:         EDO     - objeto da classe EqDiferencialOrdinaria
                        tMax    - tempo maximo que a resolucao pode alcancar
                        N       - numero maximo de passos que a resolucao pode 
                                  dar
                        To      - instante inicial para a resolucao
                        Yo      - valores das EDO's a serem resolvidas no 
                                  instante inicial
                        paramRK - array com parametros para o metodo
        Retorna:
                        T - array com os instantes de tempo pelos quais o metodo 
                            passa
                        Y - array com os valores das EDO's para cada instante de
                            tempo
    '''
    # Variavel para indexacao dos vetores
    i = 0

    # Recebe o numero de equacoes a serem resolvidas pelo metodo
    numEq = EDO.getDimension()

    # Criando vetores de tempo e imagem
    T = np.zeros(N + 1)
    Y = np.zeros((numEq, N + 1))

    # Criacao de vetores de constantes
    K1 = np.zeros((numEq, 1))
    K2 = np.zeros((numEq, 1))
    K3 = np.zeros((numEq, 1))
    K4 = np.zeros((numEq, 1))

    # Preenchimento inicial dos vetores
    T[0] = To
    Y[0:numEq, 0] = Yo

    # Determinando o passo
    h = tMax / N

    for i in range(0, N):
        # Constantes do metodo de Runge-Kutta
        K1 = EDO.evaluateFx(T[i], Y[0:numEq, i])
        K2 = EDO.evaluateFx(T[i] + 0.5 * h, Y[0:numEq, i] + 0.5 * h * K1)
        K3 = EDO.evaluateFx(T[i] + 0.5 * h, Y[0:numEq, i] + 0.5 * h * K2)
        K4 = EDO.evaluateFx(T[i] + h, Y[0:numEq, i] + h * K3)

        # Prepara o proximo Y
        Y[0:numEq, i + 1] = (Y[0:numEq, i] + (h / 6.0) * (K1 + 2.0 * (K2 + K3) + K4))

        # Prepara o proximo tempo
        T[i + 1] = T[i] + h

    return (T, Y)
