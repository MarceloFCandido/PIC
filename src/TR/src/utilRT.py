from classesRT import ray, source, velocity, layer, medium
import matplotlib.pyplot as plt
import numpy as np

def userInput():
    """
        Funcao que recebe as entradas do usuario
        Retorna:        dimension - array com as dimensoes do meio
                        posY - posicao em y da fonte
                        nLayers - numero de camadas do meio
                        nRays - numero de raios a serem tracados
                        angMin - angulo minimo da emissao dos raios
                        angMax - angulo maximo da emissao dos raios
                        lateralPoints - coordenadas em y dos pontos laterais de
                                        cada interface
                        velocidades - array dos coeficientes das funcoes veloci-
                                      dade de cada camada
                        tMax - tempo maximo que os raios podem permanecer em
                               uma camada
                        refletora - camada onde os raios devem refletir
    """
    print "Seja bem-vindo ao tracador de raios!"
    print ""
    print "OBS: muitas entradas aqui serao em ponto flutuante"
    print "por isso, nao se esqueca de usar '.' ao inves de ','"
    print ""
    dimension = np.zeros(2)
    print "Digite as dimensoes desejadas para o meio (separadas por espaco): "
    dimension = input()
    print "Digite a posicao vertical da fonte: "
    posY = input()
    print "Digite o numero de camadas: "
    nLayers = input()
    print "Digite o numero de raios: "
    nRays = input()
    print "Digite os angulos minimo e maximo de emissao dos raios"
    print "OBS: separado por espaco"
    angMin, angMax = input()
    lateralPoints = np.zeros(nLayers, dtype=(float, 2))
    print "A seguir, entre com os pontos laterais de cada interface"
    print "LEMBRE-SE: voce definiu ", nLayers, " camadas, entao haverao "
    print nLayers - 1, " interfaces, sem contar o topo do meio!"
    print "OBS: separe os pontos com espaco para cada interface"
    for i in range(1, nLayers):
        print "Interface: ", i
        lateralPoints[i, :] = input()
    velocidades = np.zeros(nLayers, dtype=(float, 3))
    print "A seguir, entre com os coeficientes das funcoes velocidade de cada ",
    print "camada"
    print "LEMBRE-SE: voce definiu ", nLayers, " camadas, entao haverao "
    print nLayers, " funcoes velocidade!"
    print "OBS: separe os coeficientes com espaco para cada camada"
    for i in range(0, nLayers):
        print "Camada: ", i
        velocidades[i, :] = input()
    print "Digite o tempo maximo que o raio pode ficar dentro de cada camada: "
    tMax = input()
    print "Digite a camada refletora: "
    refletora = input()

    return (dimension, posY, nLayers, nRays, angMin, angMax, lateralPoints,
        velocidades, tMax, refletora)

def buildMedium(dimension, posY, nLayers, nRays, angMin, angMax, lateralPoints,
                velocidades):
    """
        Funcao que constroi o meio em que os raios propagarao
        Recebe:         dimension - dimensoes do meio
                        posY - posicao y da fonte
                        nLayers - numero de camadas do meio
                        nRays - numero de raios que propagarao no meio
                        angMin - inicio do intervalo angular de disparo dos
                                 raios
                        angMax - fim desse intervalo
                        lateralPoints - lista de coordenadas em y dos pontos
                                        laterais das interfaces
                        velocidades - array contendo os coeficientes dos modelos
                                      de velocidades das interfaces
        Retorna:        m - objeto medium
    """
    # Criando camadas
    layers = []
    for i in range(0, nLayers):
        vel = velocity("0", velocidades[i][0], velocidades[i][1],
                velocidades[i][2])
        aux = layer(dimension, [lateralPoints[i][0], lateralPoints[i][1]], vel)
        layers.append(aux)

    # Setando as interfaces inferiores nas camadas
    for i in range(nLayers - 2, 0, -1):
        layers[i].setInfInt(layers[i + 1].supInt)

    # Construindo a fonte e seus raios
    s0 = source(posY, angMin, angMax, nRays, layers[0].velocity(0., 0., "0"))
    # Criando o meio
    m = medium(dimension, s0, layers)

    return m

def deprecated_somaEspessuras(l, k):
    """
        Soma as espessuras das camadas passadas por parametro ate a camada k
    """
    summ = 0.
    for i in range(0, k):
        summ += l[i].espessura
    return summ

def degreesToRadians(angle):
    """
        Funcao que retorna um angulo passado em graus, por parametro, convertido
        para radianos
    """
    return angle * np.pi / 180

def radiansToDegrees(angle):
    """
        Funcao que retorna um angulo passado em radianos, por parametro, conver-
        tido para graus
    """
    return angle * 180 / np.pi

def plot(rays, dimX, pontosLaterais):
    """
        Metodo que realiza e salva a plotagem dos raios propagando pelo meio.
        Recebe:         rays - lista de raios, que possuem os pontos a serem
                               plotados
                        dimX - dimensao do meio em x
                        pontosLaterais - pontos usados para auxiliar a exibicao
                                         das interfaces
    """
    # Criando figura
    fig = plt.figure()

    # Adicionando eixos
    fig.add_axes()

    # Criando subplot no eixo
    ax = fig.add_subplot(111)

    # Plotando os raios
    for i in range(0, len(rays)):
        ax.plot(rays[i].XP[0, :], rays[i].XP[1, :])

    # Colocando titulo e legendas no grafico
    ax.set(ylabel='Profundidade', xlabel='Alcance')

    # Plotando as Camadas
    for i in range(0, pontosLaterais.size / 2):
        ax.plot((0., dimX), (pontosLaterais[i][0], pontosLaterais[i][1]), '-k')

    # Invertendo o eixo y
    plt.gca().invert_yaxis()

    # Salvando a imagem
    # Definindo caminho da plotagem
    caminho = '../images/TR.png'
    plt.savefig(caminho)

def projVetorial(v, u):
    """
        Funcao que retorna a projecao vetorial do vetor v sobre o vetor u
        Recebe:         v - array que representa o vetor a ser projetado
                        u - array que representa o vetor que recebera a projecao
        Retorna:        a projecao vetorial de v sobre u
    """
    num = v.dot(u)
    den = u.dot(u)
    return num / den * u
