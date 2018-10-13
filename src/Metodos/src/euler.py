# a  - margem do intervalo a esquerda
# b  - margem do intervalo a direita
# m  - numero de subintervalos
# y0 - valor de f(a)

def Euler(a, b, m, y0):
    h       = (b - a) / m # Calculando o tamanho do passo de acordo com o numero de pontos
    x       = a
    y       = y0
    Fxy     = f(x, y) # Avaliando a funcao no extremo esquerdo (sendo a < b)
    
    vetX[0] = x # Colocando os primeiros valores de x e y nos vetores
    vetY[0] = y
    
    for i in range(0, m):
        x   = a + i * h # Calculando x(i)
        y   = y + h * Fxy
        Fxy = f(x, y)
        
        print "i: " + i + "x: " + x + "y: " + y + "Fxy: " + Fxy
        
        vetX[i + 1] = x
        vetY[i + 1] = y
        
    return vetX, vetY