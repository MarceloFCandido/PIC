from utilRT     import projVetorial
from rungeKutta import rungeKutta4Ordem as RK4
import numpy                            as np

def refract(i, v1, v2, r, s):
    """
        Procedimento que realiza a refracao do raio
        i   - objeto interface
        v1  - objeto velocidade da camada 1
        v2  - objeto velocidade da camada 2
        r   - objeto ray
        s   - sentido do raio (descendo ou subindo)
    """
    # Vetor direcao atual do raio
    XY = np.array([r.XP[0, -1], r.XP[1, -1]])
    P  = np.array(r.XP[2, -1], r.XP[3, -1])

    # Preparando as velocidades a serem utilizadas
    v1_ponto = v1(XY[0], XY[1], "0")
    v2_ponto = v2(XY[0], XY[1], "0")
    sinTheta1 = np.linalg.norm(projVetorial(P, i.vDiretor))

    # Aplicando a lei de fato
    sinTheta2 = v2_ponto / v1_ponto * sinTheta1

    # Obtendo o cosTheta2 e as novas componentes do raio
    cosTheta2 = np.sqrt(1 - sinTheta2 * sinTheta2)

    # Definindo o novo vetor para o raio
    if s > 0:   # Descendo
        P = cosTheta2 * i.vNormal + sinTheta2 * i.vDiretor
    else:   # Subindo
        P = cosTheta2 * -i.vNormal + sinTheta2 * i.vDiretor

    # Colocando nova direcao para o raio
    r.XP[2, -1], r.XP[3, -1] = P

def reflect(i, r):
    """
        Procedimento que realiza a reflexao do raio
        i - objeto interface
        r - objeto ray
    """
    P        = np.array([r.XP[2, -1], r.XP[3, -1]])
    S        = projVetorial(P, i.vNormal)
    r.XP[2, -1], r.XP[3, -1] = P - 2 * S

def go(v, i, r, s, dimX, tMax):
    """
        Procedimento que calcula o prosseguimento do raio
        v    - objeto velocity
        i    - objeto interface
        r    - objeto ray
        s    - sentido do raio (descendo ou subindo)
        dimX - dimensao em X do meio
        tMax - tempo maximo que um raio pode permanecer em uma camada
    """
    # Usando o rungeKutta
    # O tempo maximo deve ser o tempo atual + tMax
    tMax     = r.time[-1] + tMax
    h        = .01      # Passo do RK4
    To       = r.time[-1]   # Tempo inicial
    Yo       = r.XP[:, -1]  # Valores iniciais das EDOs
    paramRK  = [v, i, dimX, s]  # Parametros do RK4
    XP, time = RK4(r, tMax, h, To, Yo, paramRK)

    # Anexando os arrays
    r.XP   = np.append(r.XP  , XP  , axis=1)
    r.time = np.append(r.time, time        )
