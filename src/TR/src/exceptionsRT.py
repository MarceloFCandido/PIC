
class criticalAngle(Exception):
    """
        Herda: Exception
        Define a excecao de angulo critico
    """
    def __init__(self, ray, layer, actualAngle, criticAngle):
        """
            Definicao de construtor
            Recebe:         ray - numero do raio com que ocorreu a excecao
                            layer - numero da camada com a qual ocorreu a
                                    excecao
                            actualAngle - angulo do raio ray
                            criticAngle - angulo critico da camada layer
        """
        self.ray         = ray
        self.layer       = layer
        self.actualAngle = actualAngle
        self.criticAngle = criticAngle
        super(criticalAngle, self).__init__(self.getMsg())

    def getMsg(self):
        """
            Funcao que retorna a mensagem exibida pela excecao
        """
        return "O atual angulo do raio ", self.ray, " (", self.actualAngle, ") e \
        maior que o angulo critico da camada ", self.layer, " (" \
        , self.criticAngle, ")"

class singularMatrix(Exception):
    #TODO: Explicar qual o problema de uma matriz singular
    """
        Classe que define a excecao de existencia de matriz singular para um
        determinado raio numa determinada camada
    """
    def __init__(self, A):
        print "A seguinte matriz e singular: "
        print A
