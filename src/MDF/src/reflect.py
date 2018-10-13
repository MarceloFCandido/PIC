import numpy as np

'''
Arquivo: reflect.py

Esse programa le o arquivo data.npy que estive na mesma pasta que ele e resolve
a equacao da onda em um meio bidimensional nao-homogeneo
(com condicoes de contorno refletoras) para os parametros
passados pelo arquivo data.npy pelo metodo de diferencas finitas

Apos resolver a equacao, o arquivo salva os seguintes arquivos binarios:
    U.npy - Malha que representa a propagacao da onda 2D ao longo do tempo
    X.npy - Eixo x usado para os calculos que geraram a malha de U.npy
    Y.npy - Eixo y usado para os calculos que geraram a malha de U.npy
    V.npy - Velocidades usadas durante o calculo da malha de U.npy
'''

class interface(object):
    '''
        Herda: object
        Define uma interface na forma de uma reta
    '''

    def __init__(self, a, b):
        '''
            Definicao de construtor
            Recebe:     a - coeficiente angular
                        b - termo independente
        '''
        self.a = a
        self.b = b

    def __call__(self, x):
        '''
            Definicao de funcao
            Recebe :    x - valor nas abscissas
            Retorna:    y - valor nas ordenadas para o valor x
        '''
        return self.a * x + self.b

class velocity(object):
    '''
        Herda: object
        Define uma velocidade como uma funcao quadratica
    '''
    def __init__(self, a = 0., b = 0., c = 1.1):
        '''
            Definicao de construtor
            Recebe:     a - Termo 'a' da funcao quadratica
                        b - Termo 'b' da funcao quadratica
                        c - Termo 'c' da funcao quadratica
        '''
        self.a    = a
        self.b    = b
        self.c    = c

    def getGradientVelocity(self, x, y):
        '''
            Definicao de funcao
            Recebe:     x - valor nas abscissas
                        y - valor nas ordenadas
            Retorna:    y - valor da velocidade em (x, y)
        '''
        return self.a * x + self.b * y + self.c

    def __call__(self, x, y):
        '''
            Uma funcao call para uma classe permite que um objeto desta
            seja chamado como uma funcao. No caso de um objeto velocity ser
            chamado, ele retornara a velocidade v_type(x, y), sendo type o tipo
            de velocidade a ser retornada e derv a derivada da velocidade
        '''
        return self.getGradientVelocity(x, y)

# Criando a classe que define a onda 2D
class wave2D(object):
    '''
        Herda: object
        Define uma onda (por meio de algumas propriedades desta) em um ambiente
        bidimensional heterogeneo
    '''

    def __init__(self, Lx, Ly, tMax, Mx, Ny, w, A, Xp, Yp, Tp):
        '''
            Define um de ondas bidimensionais
            Recebe:     Lx - Comprimento do dominio em relacao ao eixo x
                        Ly - Comprimento do dominio em relacao ao eixo y
                        tMax - Tempo maximo para a propagacao da onda
                        Mx - Numero de pontos no eixo x
                        Ny - Numero de pontos no eixo y
                        w  - Frequencia dominante da onda
                        A  - Amplitude da onda
                        Xp - Posicao em x do pico do pulso da fonte
                        Yp - Posicao em y do pico do pulso da fonte
                        Tp - Tempo do pico do pulso da fonte
        '''
        self.Lx   = Lx
        self.Ly   = Ly
        self.tMax = tMax
        self.Mx   = Mx
        self.Ny   = Ny
        self.w    = w
        self.A    = A
        self.Xp   = Xp
        self.Yp   = Yp
        self.Tp   = Tp
        self.dx   = float(self.Lx) / float (Mx - 1) # Intervalo em x
        self.dy   = self.dx # Intervalo em y
        self.dt   = self.dy / 2.0 # Intervalo no tempo
        # Numero de pontos no tempo
        self.Ot   = int(np.ceil(self.tMax / self.dt)) + 1
        self.R    = np.power(np.pi, 2) * np.power(self.w, 2)

    def evaluateFXYT(self, X, Y, T):
        '''
            Funcao define a fonte da equacao da onda para os valores de
            X, Y e T. Atualmente, a fonte esta definida como uma wavelet Ricker
            Recebe:     X - array de valores no eixo das abscissas
                        Y - array de valores no eixo das ordenadas
                        T - array de valores no eixo temporal
            Retorna:    a funcao da wavelet Ricker
        '''
        termoT = self.R * np.power(T-self.Tp, 2)

        D = np.power(X-self.Xp,2) + np.power(Y-self.Yp,2)

        termoD = self.R * D

        return self.A * np.exp(-termoT) * ((1 - 2 * termoD) * np.exp(-termoD))

    def getVelocityMatrix(self, interfaces, velocidades):
        '''
            Funcao que retorna um array bidimensional de velocidades. Para cada
            ponto do meio em que a onda se propaga calcula-se uma velocidade,
            dependendo de qual camada o ponto se encontra.
            Recebe:     interfaces  - lista de interfaces (se encontram de uma
                                      camada para outra)
                        velocidades - lista de objetos velocidade, cujos itens
                                      sao as funcoes velocidade de cada camada
                                      do meio
        '''
        # Criando matriz de velocidades
        velocities = np.zeros((int(self.Mx), int(self.Ny)))

        # Preenchendo a matriz
        k = 0
        for i in range(0, int(self.Mx - 1)):
            x = i * self.dx     # Dando um passo nas abscissas
            for j in range(0, int(self.Ny - 1)):
                y = j * self.dy     # Dando um passo nas ordenadas
                while y > interfaces[k](x) and k < len(interfaces) - 1:
                    k += 1      # Determinando em que camada o ponto se encontra
                # Calculando a velocidade naquele ponto
                velocities[i, j] = velocidades[k](x, y)
                k = 0

        return velocities

# Carregando os dados do arquivo
data = np.load('../data/configs/waveConfigs.npy')
vl   = np.load('../data/configs/velocities.npy')
it   = np.load('../data/configs/interfaces.npy')

# Criando objeto do tipo wave2D
#                  Lx      Ly       tMax     Mx       Ny       w
Onda2D = wave2D(data[0], data[1], data[2], data[3], data[4], data[5],
#     A        Xp       Yp       Tp
    data[6], data[7], data[8], data[9])

# Organizando dados das interfaces e das velocidades das camadas
interfaces = []
velocidades = []
for i in range(it.shape[0]):
    interfaces.append(interface(it[i, 0], it[i, 1]))
    velocidades.append(velocity(vl[i, 0], vl[i, 1], vl[i, 2]))
velocidades.append(velocity(vl[it.shape[0], 0], vl[it.shape[0], 1],
vl[it.shape[0], 2]))

# Recebendo matriz de velocidades
velocidades = Onda2D.getVelocityMatrix(interfaces, velocidades)

# Criando array de Mx * Ny * Ot pontos
U = np.zeros((int(Onda2D.Mx), int(Onda2D.Ny), int(Onda2D.Ot)))

# Criando vetores X, Y, T
X = np.linspace(0., Onda2D.Lx  , Onda2D.Mx)
Y = np.linspace(0., Onda2D.Ly  , Onda2D.Ny)
T = np.linspace(0., Onda2D.tMax, Onda2D.Ot)

# Aplicando condicoes iniciais U = 0. e dt(U) = 0.
U[:, :, 0:2] = 0.

# Aplicando condicoes de fronteira
U[                 :,                  0, :] = 0.
U[int(Onda2D.Mx - 1),                  :, :] = 0.
U[                 :, int(Onda2D.Ny) - 1, :] = 0.
U[                 0,                  :, :] = 0.

# Indices para os pontos interiores
i = np.arange(1, int(Onda2D.Mx - 1))
j = np.arange(1, int(Onda2D.Ny - 1))

[ii, jj] = np.meshgrid(i, j)

# Criando dx^2
dx2 = Onda2D.dx * Onda2D.dx

# Aplicando o MDF
d = 2 * velocidades[ii, jj]
c = 1 / (d * d)
for k in range(1, Onda2D.Ot - 1):
    U[ii, jj, k + 1] = c * (Onda2D.evaluateFXYT(X[ii], Y[jj], T[k]) - \
    4. * U[ii, jj, k] + U[ii - 1, jj, k] + U[ii + 1, jj, k] + \
    U[ii, jj - 1, k] + U[ii, jj + 1, k]) - U[ii, jj, k - 1] + 2. * U[ii, jj, k]

# Salvando arrays (um em cada arquivo, exceto o T, para evitar confusao)
np.save('../data/outputs/X', X)
np.save('../data/outputs/Y', Y)
np.save('../data/outputs/V', velocidades)
np.save('../data/outputs/U', U)
