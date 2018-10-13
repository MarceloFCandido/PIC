from exceptionsRT import singularMatrix as sm
import numpy as np

# --------------------- Funcoes auxiliares ao Runge-Kutta -------------------- #
def didItTouchTheInterface(x, y, _i, s):
    """
        Funcao que determina se o raio ainda esta na camada atual
        Recebe:         (x, y) - ponto atual do raio
                        _i     - proxima interface
                        s      - sentido que o raio esta seguindo (para cima ou
                                 para baixo)
        Retorna:        Caso o raio esteja descendo pelo meio, se a ultima coor-
                        denada y calculada para ele foi maior que o y da inter-
                        face calculado para o x do raio, entao ele ultrapassou a
                        interface.
                        Caso ele esteja subindo pelo meio e seu y for menor que
                        o y calculado para o x do raio na interface, entao o
                        raio ultrapassou a interface
    """
    if s == 1:
        if y > _i(x):
            return 1
        else:
            return 0
    else:
        if y < _i(x):
            return 1
        else:
            return 0
# ---------------------------------------------------------------------------- #

def rungeKutta4Ordem(EDO, tMax, h, To, Yo, paramRK = 0):
    """
        Funcao que implementa o metodo de Runge-Kutta de quarta ordem (RK4)
        Recebe:         EDO     - edos a serem resolvidas numericamente pelo RK4
                        tMax    - final do intervalo I de tempo para o qual a
                                  edo sera resolvida (I = [To, tMax])
                        h       - Passo dado no tempo
                        To      - Inicio do intervalo I
                        Yo      - array com os valores iniciais das equacoes a
                                  serem resolvidas pelo RK4
                        paramRK - parametros para o RK4
       Retorna:         T       - array com todos os valores calculados para o
                                  tempo durante a execucao do RK4
                        Y       - Valores das equacoes calculados para cada pas-
                                  so dado pelo RK4
    """
    # Variavel para indexacao dos vetores
    i = 0

    # Determinando o passo
    N = int(tMax / h)

    # Recebe o numero de equacoes a serem resolvidas pelo metodo
    numEq = EDO.dimension

    # Criando vetores de tempo e imagem
    T = np.zeros(        N + 1)
    Y = np.zeros((numEq, N + 1))

    # Criacao de vetores de constantes
    K1 = np.zeros((numEq, 1))
    K2 = np.zeros((numEq, 1))
    K3 = np.zeros((numEq, 1))
    K4 = np.zeros((numEq, 1))

    # Preenchimento inicial dos vetores
    T[0]          = To
    Y[0:numEq, 0] = Yo

    # Descrevendo quais sao os parametros
    v    = paramRK[0]
    _i   = paramRK[1]
    dimX = paramRK[2]
    s    = paramRK[3]

    for i in range(0, N):
        # Constantes do metodo de Runge-Kutta
        K1 = EDO.evaluate(Y[0:numEq, i]               , v)
        K2 = EDO.evaluate(Y[0:numEq, i] + 0.5 * h * K1, v)
        K3 = EDO.evaluate(Y[0:numEq, i] + 0.5 * h * K2, v)
        K4 = EDO.evaluate(Y[0:numEq, i] +       h * K3, v)

        # Prepara o proximo Y
        Y[0:numEq, i + 1] = (Y[0:numEq, i] + (h / 6.0) * (K1 + 2.0 * (K2 + K3) \
                            + K4))

        # Testando se o raio saiu do dominio
        if Y[0, i + 1] > dimX or Y[0, i + 1] < 0. or Y[1, i + 1] < 0.:
            return Y[:,:i + 2], T[:i + 1]

        # Testando se o raio passou para outra camada
        if (didItTouchTheInterface(Y[0, i + 1], Y[1, i + 1], _i, s)):
            # Imaginamos uma reta ligando os dois ultimos pontos tracados
            diretor = np.array([Y[2, i], Y[3, i]])
            # Criando a matriz com as componentes dos vetores diretores da reta
            # e da interface (matriz A)
            A = np.array([[diretor[0], -_i.vDiretor[0]], [diretor[1], -_i.vDiretor[1]]])

            # Para o caso da matriz A ser singular
            det = np.linalg.det(A)
            if det > -.0005 and det < .0005:
                raise sm()

            # Criando a matriz B
            B = np.array([-Y[0, i], _i.b - Y[1, i]])

            # Resolvendo o sistema linear
            X = np.linalg.solve(A, B)

            # Recolhendo o parametro s_0 para determinar o ponto de intersecao
            # entre as retas
            s_0 = X[1]

            # Determinando o ponto de intersecao
            Y[0, i + 1] =      + _i.vDiretor[0] * s_0
            Y[1, i + 1] = _i.b + _i.vDiretor[1] * s_0
            return Y[:,:i + 2], T[:i + 1]

        # Prepara o proximo tempo
        T[i + 1] = T[i] + h
    return Y, T
