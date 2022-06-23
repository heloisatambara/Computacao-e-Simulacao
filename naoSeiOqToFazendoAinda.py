#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#### EP06 ####
#Escreva seus nomes e numeros USP
INFO = {12556819:"Heloisa Tambara",2371457:"Fabricio Barbosa Bittencourt"}

import numpy as np
import math


def fpotencial(theta, a): 
    lista = [] 
    for i in range(len(theta)): 
        lista.append(theta[i]**(a[i]-1)) 
    n = np.array(lista)
    
    
    return np.prod(n)

def f(theta, a): 
    lista = [] 
    for i in range(len(theta)): 
        lista.append(theta[i]**(a[i]-1)) 
    n = np.array(lista)
    
    beta = math.factorial(a[0]-1)*math.factorial(a[1]-1)*math.factorial(a[2]-1)/math.factorial(sum(a)-1)
    return np.prod(n)/beta
    


def amostra_MCMC(x,n):
    """
    Funcao que recebe valores pros vetores x e y, o tamanho n da amostra, 
    gera uma amostra de tamanho n a partir do metodo de monte carlo via 
    cadeias de markov, onde cada elemento da amostra tem tamanho 3 (vetor),
    e retorna uma lista de tamanho n com os potenciais de cada ponto obtido,
    onde cada elemento tem tamanho 1 (escalar).
    
    Nao utilize a fuancao densidade de probabilidade, apenas a funcao potencial!
    """
    a = []
    
    for i in range(len(x)):
        a.append(x[i]) # a é parâmetro para a distribuição de dirichlet
        
    a0 = sum(a)
    #print("ao=",a0 )

    matrix = np.array([[1.0,1.0,1.0],[1.0,1.0,1.0],[1.0,1.0,1.0]])

    for i in range(len(a)):
        for j in range(len(a)):
            if i==j:
                matrix[i][j] = (a[i]*(a0 - a[i]))/(a0**2*(a0+1))   #Var
                
            else:
                matrix[i][j] = (-a[i]*a[j])/((a0**2)*(a0+1))    #Cov
    print('Breakpoint 1')
    

    harmup_n = 10000
    cont = 0
    p0 = np.array([0.3,0.3,0.4])

    sp = p0
    #vez=1
    while cont < harmup_n:
        bol = True
        
        while bol:
            ponto = np.random.multivariate_normal(sp,matrix)
            #if vez<=5: print (ponto)
            #vez+=1
            if ponto[0] >= 0 and ponto[1] >= 0 and ponto[2]>=0:    
                bol = False
                
        alpha = min(1, fpotencial(ponto,a)/fpotencial(sp,a))        #g(xj)=fpotencial(ponto,a)     g(xi)=fpotencial(sp,a)
        #print(alpha, ponto,a, sp, fpotencial(ponto,a),fpotencial(sp,a))
        if alpha >= np.random.uniform():
            
            sp = ponto
        #print(sp)
        cont+=1
    print('Breakpoint 2')



    n = 3900000

    lista = []
    cont = 0

    lp = sp
    while cont < n: #Aqui demora pra bosta
        
        bol = True
        while bol:
            ponto = np.random.multivariate_normal(lp,matrix)
            if ponto[0] >= 0 and ponto[1] >= 0 and ponto[2]>=0:
                
                bol = False


        alpha = min(1, fpotencial(ponto,a)/fpotencial(lp,a))
        if alpha >= np.random.uniform():
    
            lista.append(ponto)
            lp = ponto
            
        else: 
            lista.append(lp)
        
        cont+=1

    print('Breakpoint 3')

    amostra_de_potenciais = lista # ["Nenhuma amostra foi gerada"]
    return amostra_de_potenciais # Exemplo do formato = [0.04867, 0.00236, 0.00014 ... ]








class Estimador:
    """
    Classe para criar o objeto, ele recebe valores para os vetores x e y.
    Os metodos definidos abaixo serao utilizadas por um corretor automatico. Portanto,
    precisa manter os outputs e inputs dos 2 metodos abaixo. 
    """
    def __init__(self,x):
        """
        Inicializador do objeto. Este metodo recebe 
        valores pros vetores x e y em formato de lista 
        e implementa no objeto. 
        """
        self.vetor_x = x #formato: [0,0,0] - List cujo len(x) = 3
        #self.vetor_y = y #formato: [0,0,0] - List cujo len(y) = 3
        #Continue o codigo conforme achar necessario.
        a = []
        for i in range(len(x)): 
          a.append(x[i])
        self.a = a


        lista = amostra_MCMC(x,100)
        self.lista = lista

        n = 3900000
        fv = []
        ftheta = np.array(self.lista)

        for i in range(n):
            fv.append(f(ftheta[i], self.a))

        fv = sorted(fv)
    
        self.k = k = 15000 #A escolha do valor k está explicada no relatório.
        V = [0]
    
        for i in range(k):
            V.append(fv[n//k*i])
        V.append(fv[-1])
        
        self.V = V



    def U(self,v):
        """
        Este metodo recebe um valor para v e, a partir dele, retorna U(v|x,y) a partir dos 
        vetores x e y inicializados anteriormente
        """
        # Continue o codigo conforme achar necessario
        if v < self.V[1]: u = 0
        elif v > self.V[self.k+1]: u = 1
        else:
            acharbin = 1
            a = 1
            while acharbin == 1:
                if v < self.V[a]: acharbin = 0
                a += 1
            u = 1/self.k*(v-self.V[a])/(self.V[a+1]-self.V[a])+(a-1)/self.k


        return u



def main():
    #Coloque seus testes aqui
    print("Segue um exemplo de funcionamento:")
    print("Criando o objeto")
    estimativa = Estimador([1,2,3])
    print("Implementando o valor para v")
    print(f"Temos que U({42}) = {estimativa.U(42)}")
    print(f"Para um novo valor de v, temos que U({5/4}) = {estimativa.U(5/4)}")
    print()
    print(f"Os valores dos vetores utilizados sao: {estimativa.vetor_x,estimativa.vetor_y}")
    print("Este exemmplo foi feito para demonstrar o funcionamento esperado do objeto")

#    print(f"x1={x1}, x3={x3}, Y= {Y}, H={decisao},  θ*= {vetor_theta}, ev(H|X)={ev} e sev(H|X)={sev}")



if __name__ == "__main__":
    main()

