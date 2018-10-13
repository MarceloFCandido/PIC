"""
    Arquivo: classesRT.py
    Reune as classes utilizadas no tracamento de raios, definindo os elementos
    que compoem o meio onde os raios serao tracados, definindo tambem os
    proprios raios.
"""

from eqDiferencialOrdinaria import eqDiferencialOrdinaria as EDO
import numpy as np

class ray(EDO):
    """
        Herda: EDO
        Define, a partir da teoria matematica, o que e um raio, armazenando
        em arrays os seus pontos e direcoes ao longo do tempo.
    """
    def __init__(self, dimension, XP, time = 0.):
        """
            Definicao de construtor
            Recebe:         dimension - numero de EDOs que definem o raio (4)
                            XP - array de posicoes/direcoes ao longo do tempo
                            time - array que guarda o tempo de transito do raio
        """
        super(ray, self).__init__(dimension)
        self.XP            = XP
        self.time          = np.array([0.])

    def evaluate(self, Y, v):
        """
            Definicao de funcao
            Avalia as quatro equacoes que definem o raio usando os pontos e
            direcoes passadas em Y e o modelo de velocidade definido em v.
            Recebe:         Y - ultimos valores calculados pelo RK4 para a
                                posicao e a direcao do raio em questao
                            v - objeto velocidade que, quando chamado (utilizan-
                                do a funcao __call__) retorna a velocidade no
                                ponto (x, y) passado por parametro
            Retorna:        retorno - array contendo os valores calculados pelas
                                      equacoes do raio
        """
        retorno = np.zeros(4) # Array que servira de retorno
        Vxy     = v(Y[0], Y[1], "0")
        iVxy    = 1. / Vxy
        dVx     = v(Y[0], Y[1], "1x")
        dVy     = v(Y[0], Y[1], "1y")

        retorno[0] = Vxy * Vxy * Y[2] #  dx/dt
        retorno[1] = Vxy * Vxy * Y[3] #  dy/dt
        retorno[2] = iVxy * dVx       # dPx/dt
        retorno[3] = iVxy * dVy       # dPy/dt

        return retorno

class source(object):
    """
        Herda: object
        Define a fonte de raios, que os cria de acordo com os parametros que re-
        cebeu.
    """
    def __init__(self, posY, angMin, angMax, nRays, initialVelocity):
        """
            Definicao de um construtor
            Recebe:         posY - Posicao de onde partirao os raios
                            angMin - Inicio do intervalo que sera iluminado
                                     pelos raios
                            angMax - Fim desse intervalo
                            nRays - Numero de raios a serem tracados
                            initialVelocity - velocidade no ponto de partida dos
                                              raios
        """
        self.posY            = posY
        self.angMin          = angMin
        self.angMax          = angMax
        self.nRays           = nRays
        self.initialVelocity = initialVelocity
        self.genRays()

    def genRays(self):
        """
            Procedimento que cria os raios de acordo com os parametros da fonte.
        """
        # Determinando 'passo angular'
        h = (self.angMax - self.angMin) / (self.nRays - 1)

        # Criando lista vazia
        self.rays = []

        for i in range(0, self.nRays):
            # Determinando angulo do raio
            ang = self.angMin + i * h
            # Criando vetor posicao-direcao do raio
            Y = np.zeros((4, 2))
            Y[:, 0] = np.nan    # Para permitir o anexamento no metodo 'go'
            Y[0, 1] = Y[1, 1] = 0. # Posicao inicial
            Y[2, 1] = np.sin(ang) / self.initialVelocity # Direcao inicial
            Y[3, 1] = np.cos(ang) / self.initialVelocity

            # Criando raio auxiliar
            Aux = ray(4, Y)

            # Colocando raio na lista
            self.rays.append(Aux)

class velocity(object):
    """
        Herda: object
        Define a velocidade como uma funcao quadratica com coeficientes a, b e c
        bem como as derivadas dessa funcao
    """
    def __init__(self, type, a = 0., b = 0., c = 1.):
        """
            Definicao de um construtor
            Recebe:         type - tipo de velocidade (neste trabalho foi defi-
                                   nido apenas o modelo quadratico de veloci-
                                   dade, entretanto, essa variavel permite que
                                   mais modelos sejam implementados)
                            a, b, c - coeficientes da funcao quadratica que
                                      define a velocidade
        """
        self.type = type
        self.a    = a
        self.b    = b
        self.c    = c

    def getGradientVelocity(self, x, y, derv = "0"):
        """
            Funcao que retorna a velocidade (ou uma de suas derivadas) em um da-
            do ponto (x, y)
            Recebe          x - coordenada x do ponto em que se deseja calcular
                                a velocidade
                            y - coordenada y do mesmo ponto
                            derv - a derivada desejada
            Retorna         a velocidade no ponto (x, y) ou a derivada desejada
                            da funcao
        """

        return {
            "0"  : self.a * x + self.b * y + self.c,
            "1x" : self.a,
            "1y" : self.b
        }.get(derv, "0")

    def __call__(self, x, y, derv = "0"):
        """
            Uma funcao call para uma classe permite que um objeto desta
            seja chamado como uma funcao. No caso de um objeto velocity ser
            chamado, ele retornara a velocidade v_type(x, y), sendo type o tipo
            de velocidade a ser retornada e derv a derivada da velocidade
        """
        return {
            '0' : self.getGradientVelocity(x, y, derv)
        }.get(self.type, '0')

class interface(object):
    """
        Herda: object
        Responsavel por permitir a interpretacao de uma interface como uma reta,
        na sua forma parametrica, ou seja, com um vetor diretor e um ponto por
        onde ela passa. Alem disso, sao definidos os seus pontos extremos (pon-
        tos laterais).
    """

    def __init__(self, diretor, lateralPoints):
        """
            Definicao de construtor
            Recebe:         diretor - vetor diretor da interface
                            lateralPoints - pontos extremos da interface
        """
        self.vDiretor = diretor
        self.vNormal  = np.array([-diretor[1], diretor[0]])
        self.a        = diretor[1] / diretor[0]
        self.b        = lateralPoints[0]
        self.lP       = lateralPoints

    def __call__(self, x):
        """
            Funcao que possibilita que, ao se chamar um objeto da classe inter-
            face, passando-se um valor na coordenada x para ele, se obtenha o
            valor y correspondente, como em uma reta.
            Recebe:         x - coordenada nas abscissas
            Retorna:        y - valor correspondente a x nas ordenadas
        """
        return self.a * x + self.b

class layer(object):
    """
        Herda: object
        Define como e interpretada uma camada. A camada e interpretada como
        possuindo uma interface superior e uma interface inferior. Entre ambas
        as interfaces, ha uma parcela do meio que possui uma determinada velo-
        cidade.
    """
    def __init__(self, mediumsDimension, lateralPoints, velocity):
        """
            Definicao de construtor
            Recebe:         mediumsDimension - dimensao do meio
                            lateralPoints - pontos extremos da interface supe-
                                            rior
                            velocity - modelo de velocidade para a camada
        """
        self.mediumsDimension = mediumsDimension
        self.lateralPoints    = lateralPoints
        self.velocity         = velocity
        self.makeDirector()
        self.supInt = interface(self.director, lateralPoints)

    def makeDirector(self):
        """
            Metodo responsavel por criar um vetor diretor para a camada (e,
            consequentemente, para sua interface superior)
        """
        # Criando vetor paralelo a interface
        self.director = np.array([self.mediumsDimension[0],
                        self.lateralPoints[1] - self.lateralPoints[0]])
        # Calculando a norma do vetor
        directorNorm = np.linalg.norm(self.director)
        # Normalizando o vetor
        self.director /= directorNorm

    def setInfInt(self, Int):
        """
            Metodo responsavel por setar a interface inferior da camada
        """
        self.infInt = Int

class medium(object):
    """
        Herda: object
        Define o meio por meio dos seus principais elementos
    """
    def __init__(self, dimension, s0, layers):
        """
            Definicao de construtor
            Recebe:         dimension - dimensoes do meio
                            s0 - fonte que dispara raios no meio
                            layers - camadas (e, consequentemente, interfaces do
                                     meio)
        """
        self.dimension  = dimension
        self.s0         = s0
        self.layers     = layers
