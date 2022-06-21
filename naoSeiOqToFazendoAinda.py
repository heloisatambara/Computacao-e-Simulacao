#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Escreva seus nomes e numeros USP
INFO = {12556819:"Heloisa Tambara",2371457:"Fabricio Barbosa Bittencourt"}

import numpy as np




def fpotencial(theta, a): 
    lista = [] 
    for i in range(len(theta)): 
        lista.append(theta[i]**(a[i]-1)) 
    n = np.array(lista)
    
    
    return np.prod(n)


class Estimador:
    """
    Classe para criar o objeto, ele recebe valores para os vetores x e y.
    Os metodos definidos abaixo serao utilizadas por um corretor automatico. Portanto,
    precisa manter os outputs e inputs dos 2 metodos abaixo. 
    """
    def __init__(self,x,y):
        """
        Inicializador do objeto. Este metodo recebe 
        valores pros vetores x e y em formato de lista 
        e implementa no objeto. 
        """
        self.vetor_x = x #formato: [0,0,0] - List cujo len(x) = 3
        self.vetor_y = y #formato: [0,0,0] - List cujo len(y) = 3
        #Continue o codigo conforme achar necessario.
        a = []
        for i in range(len(x)): 
          a.append(x[i] + y[i])
        self.a = a


        a0 = sum(a)
        print("ao=",a0 )

        matrix = np.array([[1.0,1.0,1.0],[1.0,1.0,1.0],[1.0,1.0,1.0]])

        for i in range(len(a)):
            for j in range(len(a)):
                if i==j:
                    matrix[i][j] = (a[i]*(a0 - a[i]))/(a0**2*(a0+1))   #Var
                    
                else:
                    matrix[i][j] = (-a[i]*a[j])/((a0**2)*(a0+1))    #Cov

        harmup_n = 10000
        cont = 0
        p0 = np.array([0.3,0.3,0.4])

        sp = p0

        while cont < harmup_n:
            bol = True
            
            while bol:
                ponto = np.random.multivariate_normal(sp,matrix)
                #if vez<=5: print (ponto)
                #vez+=1
                if ponto[0] >= 0 and ponto[1] >= 0 and ponto[2]>=0:    
                    bol = False
                    
            alpha = min(1, fpotencial(ponto,a)/fpotencial(sp,a))        #g(xj)=fpotencial(ponto,a)     g(xi)=fpotencial(sp,a)
     
            if alpha >= np.random.uniform():
                
                sp = ponto
            #print(sp)
            cont+=1



        n = 3900000

        lista = []
        cont = 0

        lp = sp
        while cont < n:
            
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

##########################################################
            fv = []
            ftheta = np.array(lista)

            for i in range(n):
                fv.append(f(ftheta[i], a))

            fv = sorted(fv)

            k = 15000 #A escolha do valor k está explicada no relatório.
            v = [0]

            for i in range(k): v.append(fv[n//k*i])
            v.append(fv[-1])
            print("v1 = ", v[1])
            print("vk = ", v[-1])
            self.v = v





    def U(self,v):
        """
        Este metodo recebe um valor para v e, a partir dele, retorna U(v|x,y) a partir dos 
        vetores x e y inicializados anteriormente
        """

        k = 15000
            
        if v<self.v[1]: U=0
        elif v>self.v[k+1]:U=1
        else:
            acharbin=1
            a=1
            while acharbin ==1:
                if v<self.v[a]: acharbin=0
                a+=1
            U=1/k*(v-self.v[a])/(self.v[a+1]-self.v[a])+(a-1)/k


        print("O valor de U(",v,") é: ",U)

        return U




def main(): #ARRUMAR PARA SAIR ISSO DE QUALQUER JEITO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    estimativa = Estimador([1,2,3],[2,4,6])
    print("Implementando o valor para v")
    print(f"Temos que U({42}) = {estimativa.U(42)}")

    #Coloque seus testes aqui
    print(f"x1={x1}, x3={x3}, Y= {Y}, H={decisao},  θ*= {vetor_theta}, ev(H|X)={ev} e sev(H|X)={sev}")

if __name__ == "__main__":
    main()

