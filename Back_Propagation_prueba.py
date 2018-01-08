# Red Neuronal Back-Propagation

import math
import random
import string

random.seed(0)

# Calcula un numero aleatorio donde: a <= rand < b 
def rand(a, b):
    return (b-a)*random.random() + a

# Crea una matriz
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# La funcion sigmoide utilizada en este caso es la tanh, ya que es un poco mejor que la estandar 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)
    #return 1/(1+math.e**(-x))

# La derivada de la funcion sigmoide en terminos de la salida (y)
def dsigmoid(y):
    return 1.0 - y**2
    #return sigmoid(y)*(1-sigmoid(y))

class NN:
    def __init__(self, ni, nh, no):
        # Cantidad de nodos de las capas de entrada, oculta y salida
        self.ni = ni + 1 # +1 para el nodo de bias
        self.nh = nh 
        self.no = no

        # Activaciones para los nodos
        self.ai = [0.0]*self.ni
        self.ah = [0.0]*self.nh
        self.ao = [0.0]*self.no
        
        # Se crea las matrices de pesos
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)

        # Se dan valores aleatorios para los pesos
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.1, 0.1)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-0.01, 0.01)

        # Ultimo cambio en los pesos por el factor de inercia
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('Numero incorrecto de entradas')

        # Activacion de entrada
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # Activaciones de oculta
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # Activaciones de salida
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            val = sigmoid(sum)
            if(val >= 0.9 and val <=1.1):
                val = 1
            elif(val >= -0.1 and val <=0.1):
                val = 0
            elif(val <= -0.9 and val >= -1.1):
                val = -1
            self.ao[k] = val

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('Numero incorrecto de salida')

        # Calcula el error para la capa de salida
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # Calcula el error para la capa oculta 
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # Actualiza los pesos de oculta-salida
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # Actualiza los pesos de entrada-oculta
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # Calcula el error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
        ans = []
        for p in patterns:
            ans.append(self.update(p[0]))
            #print p[0], '->', self.update(p[0])
        return ans

    def weights(self):
        print('Pesos de Entrada:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Pesos de Salida:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=2000, N=0.01, M=0):
        # N: factor de aprendizaje
        # M: factor de inercia
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error_anterior = error
                error = error + self.backPropagate(targets, N, M)
                """if (error_anterior == error and N < 0.9):
                    N += 0.0001
                elif (error_anterior < error and N > 0.1):
                    N -= 0.0001"""
            """if i % 100 == 0:
                print('error %-.5f' % error )
                print N"""
            if (error == 0):
                print ('Iteraciones: ', i)
                break
        print (error)


def BP(tam_in, tam_out):
    """tam_in = int(input("Ingrese la cantidad de entradas de cada par: "))
    print tam_in
    tam_out = int(input("Ingrese la cantidad de salidas de cada par: "))
    print tam_out"""


    """
    pat = []
    for i in range(0,tam,1):
        pares = []
        valores = []
        for j in range(0,tam_in,1):
            valores.append(int(input()))
        pares.append(valores)
        valores = []
        for j in range(0,tam_out,1):
            valores.append(int(input()))
        pares.append(valores)
        pat.append(pares)"""

    pat = [
    [[0, 1, 0, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, -1, 0, 0]],
    [[1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, -1, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, -1, 1, 1], [0, 0, 0, -1, 0, 0, -1, 1, 1]],
    [[0, 1, 0, 0, -1, 0, 0, 0, 1], [-1, 1, 0, 0, -1, 0, 0, 0, 1]],
    [[0, 1, -1, 0, 0, 1, 0, 0, 0], [0, 1, -1, 0, 0, 1, 0, -1, 0]],
    [[1, 0, 0, 0, 1, 0, 0, 0, -1], [1, 0, 0, 0, 1, 0, -1, 0, -1]],
    [[0, 0, -1, 0, 0, 1, 1, 0, 0], [0, 0, -1, 0, -1, 1, 1, 0, 0]],
    [[0, 0, 1, 0, 0, 0, 0, 1, -1], [0, 0, 1, 0, -1, 0, 0, 1, -1]],
    [[-1, 0, 0, 1, 0, 0, 0, 1, 0], [-1, 0, -1, 1, 0, 0, 0, 1, 0]],
    [[0, 0, 1, 0, -1, 0, 1, 0, 0], [0, 0, 1, 0, -1, -1, 1, 0, 0]],
    [[1, 0, 0, -1, 1, 1, 0, 0, -1], [1, 0, 0, -1, 1, 1, -1, 0, -1]],
    [[1, -1, 1, 0, -1, 0, 0, 1, 0], [1, -1, 1, 0, -1, 0, 0, 1, -1]],
    [[0, 0, 0, 1, 0, -1, -1, 1, 1], [0, -1, 0, 1, 0, -1, -1, 1, 1]],
    [[1, -1, 0, 0, 0, 1, 0, 1, -1], [1, -1, 0, -1, 0, 1, 0, 1, -1]],
    [[0, 1, -1, 0, -1, 1, 1, 0, 0], [0, 1, -1, 0, -1, 1, 1, 0, -1]],
    [[0, 0, 1, -1, 0, 1, 0, 1, -1], [-1, 0, 1, -1, 0, 1, 0, 1, -1]],
    
    [[0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, -1, 0, 0]],
    #[[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, -1]],
    [[0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, -1, 0, 1, 0, 0]],
    [[0, 0, 1, 0, 0, 1, 0, 0, -1], [0, 0, 1, 0, 0, 1, 0, -1, -1]],
    [[0, 0, 1, 1, -1, 0, 0, 0, 0], [0, 0, 1, 1, -1, 0, -1, 0, 0]],
    [[-1, 1, 0, 1, 0, 0, 0, 0, 0], [-1, 1, 0, 1, 0, -1, 0, 0, 0]],
    [[0, 0, -1, 0, 1, 0, 1, 0, 0], [0, 0, -1, 0, 1, 0, 1, 0, -1]],
    [[-1, 1, 0, 0, 0, 0, 0, 0, 1], [-1, 1, 0, 0, -1, 0, 0, 0, 1]],
    [[1, 0, -1, 0, 0, 1, 0, 0, 0], [1, 0, -1, 0, -1, 1, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 1, -1, 1, 0], [-1, 0, 0, 0, 0, 1, -1, 1, 0]],
    [[1, 0, 0, 0, -1, 0, 0, 0, 1], [1, -1, 0, 0, -1, 0, 0, 0, 1]],
    [[0, 1, -1, 0, 1, 0, 1, -1, 0], [0, 1, -1, 0, 1, 0, 1, -1, -1]],
    [[1, 0, 0, -1, -1, 1, 1, 0, 0], [1, 0, -1, -1, -1, 1, 1, 0, 0]],
    [[0, -1, 1, 0, 0, 1, 0, 1, -1], [0, -1, 1, -1, 0, 1, 0, 1, -1]],
    [[0, 1, -1, -1, 0, 1, 1, 0, 0], [0, 1, -1, -1, 0, 1, 1, -1, 0]],
    [[-1, 1, 0, 1, -1, 0, 0, 0, 1], [-1, 1, -1, 1, -1, 0, 0, 0, 1]],
    [[1, 1, -1, 0, 0, 1, 0, -1, 0], [1, 1, -1, 0, 0, 1, -1, -1, 0]],

    [[0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, -1]],
    #[[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, -1, 0, 1, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, -1, 0, 0, 0, 1]],
    [[1, 1, -1, 0, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, -1, 0, 0, 0]],
    [[1, 0, 0, 0, -1, 0, 0, 1, 0], [1, 0, 0, 0, -1, 0, 0, 1, -1]],
    [[0, 0, 0, 1, 0, 0, -1, 1, 0], [0, -1, 0, 1, 0, 0, -1, 1, 0]],
    [[-1, 0, 0, 0, 1, 0, 0, 0, 1], [-1, 0, -1, 0, 1, 0, 0, 0, 1]],
    [[0, 0, 1, 1, 0, 0, -1, 0, 0], [0, 0, 1, 1, -1, 0, -1, 0, 0]],
    [[-1, 1, 0, 0, 0, 0, 1, 0, 0], [-1, 1, 0, 0, -1, 0, 1, 0, 0]],
    [[0, 1, 0, 0, 0, 1, 0, 0, -1], [0, 1, 0, 0, 0, 1, -1, 0, -1]],
    #[[0, 0, 1, 0, -1, 0, 1, 0, 0], [0, 0, 1, -1, -1, 0, 1, 0, 0]],
    [[-1, 0, 0, 1, 1, -1, 0, 0, 1], [-1, 0, -1, 1, 1, -1, 0, 0, 1]],
    [[0, 1, 0, 0, -1, 0, 1, -1, 1], [-1, 1, 0, 0, -1, 0, 1, -1, 1]],
    [[1, 1, -1, -1, 0, 1, 0, 0, 0], [1, 1, -1, -1, 0, 1, 0, -1, 0]],
    [[-1, 1, 0, 1, 0, 0, 0, -1, 1], [-1, 1, 0, 1, 0, -1, 0, -1, 1]],
    [[0, 0, 1, 1, -1, 0, -1, 1, 0], [-1, 0, 1, 1, -1, 0, -1, 1, 0]],
    [[-1, 1, 0, 1, 0, -1, 1, 0, 0], [-1, 1, 0, 1, 0, -1, 1, 0, -1]],

    [[0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, -1, 0, 0, 1, 0, 0, 0]],
    #[[0, 0, 0, 0, 1, 0, 0, 0, 0], [-1, 0, 0, 0, 1, 0, 0, 0, 0]],
    [[0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, -1, 0, 0, 0, 0]],
    [[-1, 0, 0, 1, 0, 0, 1, 0, 0], [-1, -1, 0, 1, 0, 0, 1, 0, 0]],
    [[0, 0, 0, 0, -1, 1, 1, 0, 0], [0, 0, -1, 0, -1, 1, 1, 0, 0]],
    [[0, 0, 0, 0, 0, 1, 0, 1, -1], [0, 0, 0, -1, 0, 1, 0, 1, -1]],
    [[0, 0, 1, 0, 1, 0, -1, 0, 0], [-1, 0, 1, 0, 1, 0, -1, 0, 0]],
    [[1, 0, 0, 0, 0, 0, 0, 1, -1], [1, 0, 0, 0, -1, 0, 0, 1, -1]],
    [[0, 0, 0, 1, 0, 0, -1, 0, 1], [0, 0, 0, 1, -1, 0, -1, 0, 1]],
    [[0, 1, -1, 1, 0, 0, 0, 0, 0], [0, 1, -1, 1, 0, 0, 0, 0, -1]],
    #[[1, 0, 0, 0, -1, 0, 0, 0, 1], [1, 0, 0, 0, -1, 0, 0, -1, 1]],
    [[0, -1, 1, 0, 1, 0, -1, 1, 0], [-1, -1, 1, 0, 1, 0, -1, 1, 0]],
    [[0, 0, 1, 1, -1, -1, 0, 0, 1], [0, 0, 1, 1, -1, -1, -1, 0, 1]],
    [[-1, 1, 0, 1, 0, 0, 1, -1, 0], [-1, 1, 0, 1, 0, -1, 1, -1, 0]],
    [[0, 0, 1, 1, 0, -1, -1, 1, 0], [0, -1, 1, 1, 0, -1, -1, 1, 0]],
    [[1, 0, 0, 0, -1, 1, 0, 1, -1], [1, 0, 0, 0, -1, 1, -1, 1, -1]],
    [[0, -1, 0, 1, 0, 0, -1, 1, 1], [0, -1, -1, 1, 0, 0, -1, 1, 1]],

    [[-1, 1, 1, 0, -1, 0, 0, 0, 0], [-1, 1, 1, 0, -1, 0, 0, 0, -1]]
    ]

    # Crea una red con tam_in nodos de entradas, (tam_in+tam_out)/2 nodos para la oculta y tam_out nodos de salida
    n = NN(tam_in, (tam_in)*4, tam_out)
    return n, pat

def BPTrain(n, pat):
    n.train(pat)

def BPTest(n, pat):
    sol = n.test(pat)
    return sol
    
if __name__ == '__main__':
    n, pat = BP(9,9)
    BPTrain(n, pat)
