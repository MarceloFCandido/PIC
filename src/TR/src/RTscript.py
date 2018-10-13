
"""
    Arquivo: RTscript.py
    Programa central do tracamento de raios. Recebe os parametros do tracamento
    pela entrada do usuario e aplica as acoes necessarias para que o tracamento
    ocorra, utilizando os demais arquivos como acessorios
"""

from classesRT import ray, source, layer, medium
from methodsRT import refract, reflect, go
from exceptionsRT import criticalAngle, singularMatrix
from utilRT import (buildMedium, degreesToRadians, radiansToDegrees, plot,
userInput)
import numpy as np

(dimension, posY, nLayers, nRays, angMin, angMax, lateralPoints,
velocidades, tMax, refletora) = userInput()
angMin = degreesToRadians(angMin)
angMax = degreesToRadians(angMax)

# Construindo um meio
medium = buildMedium(dimension, posY, nLayers, nRays, angMin, angMax,
            lateralPoints, velocidades)

# Tracando raios
u = 0   # Para indexacao do array M
for i in range(0, 1):
    for j in range(0, nRays):
        k = 0
        # Descendo
        while True:
            # Tracando o raio
            go(medium.layers[k].velocity, medium.layers[k + 1].supInt,
                medium.s0.rays[j], 1, dimension[0], tMax)
            # Caso SIM, partir para a reflexao
            if k + 1 == refletora:
                reflect(medium.layers[k + 1].supInt, medium.s0.rays[j])
                break
            else:
                # Executando a lei de Snell para refracao
                refract(medium.layers[k + 1].supInt, medium.layers[k].velocity,
                    medium.layers[k + 1].velocity, medium.s0.rays[j], 1)
            k += 1
        # Subindo
        while True:
            # Tracando o raio
            go(medium.layers[k].velocity, medium.layers[k].supInt,
                medium.s0.rays[j], -1, dimension[0], tMax)
            # Caso SIM, chegamos ao topo
            if k == 0:
                break
            # Executando a lei de Snell para refracao
            else:
                refract(medium.layers[k].supInt, medium.layers[k].velocity,
                    medium.layers[k - 1].velocity, medium.s0.rays[j], -1)
            k -= 1

plot(medium.s0.rays, dimension[0], lateralPoints)
