#!-*- coding: utf8 -*-

from abc import ABCMeta, abstractmethod

class eqDiferencialOrdinaria(object):
    '''
        Herda: object
        Define uma equacao diferencial ordinaria ou um sistema de equacoes desse
        tipo (dependendo do valor da variavel dimension)
    '''
    def __init__(self, dimension, k = 0, a = 0, r = 0, b = 0):
        '''
            Definicao de construtor
            Recebe:         dimension - Numero de EDOs envolvidos no sistema
                            k, a, r, b - constantes para o caso do sistema de
                                         EDOs ser do tipo Lotka-Volterra, ou
                                         algo parecido
        '''
        self.dimension = dimension
        self.k         = k
        self.a         = a
        self.r         = r
        self.b         = b

    @abstractmethod
    def evaluate(Y, v):
        '''
            Funcao que, usando os valores das EDOs contidas em Y, calcula as
            proximos valores das EDOs utilizando as formulas das mesmas. v e
            utilizada na realizacao dos calculos.
            Retorna:        Y - Valores das EDOs
                            v - objeto velocity usado nos calculos
            Retorna:        array com os proximos valores das EDOs
        '''
        pass
