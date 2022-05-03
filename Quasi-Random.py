##!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scipy.stats import qmc
# ver como fazer referencia ao kite

from math import exp, cos
from scipy.stats import truncexpon
import time
import random
#Escreva seu nome e numero USP
INFO = {12556819:"Heloisa Tambara"}
A = 0.3 # A = 0.rg
B = 0.4  # B = 0.cpf

# como definir g(x) na importance sampling e na control variate?

class RandomEngine(qmc.QMCEngine):
    def __init__(self, d, seed=None):
        super().__init__(d=d, seed=seed)
    def random(self, n=1):
        self.num_generated += n
        return self.rng.random((n, self.d))


def f(x):
    """
    Esta funcao deve receber x e devolver f(x), como especifcado no enunciado
    Escreva o seu codigo nas proximas linhas
    """
    A = 0.3 # A = 0.rg
    B = 0.4  # B = 0.cpf
    f = exp(-A*x) * cos(B*x)
    
    return f




# Crude
def crude(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x) entre 0 e 1
    usando o metodo crude
    Escreva o seu codigo nas proximas linhas
    """
    t0 = time.time()
    n = 1000000 #inserir n
    soma = 0
    nums = RandomEngine(1).random(n)
    for x in range(n): # gerar n numeros x, calcular suas f(x), somar tudo e dividir por n
        soma += f(nums[x,0])

    mu = soma/n

    
    t1 = time.time()
    t = t1-t0
    print(f'calculado em {t} segundos')
    return mu # Retorne sua estimativa




# Hit or Miss
def hit_or_miss(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo hit or miss
    Escreva o seu codigo nas proximas linhas
    """
    t0 = time.time()
    n = 1000000 # inserir n
    soma = 0
    x, y = RandomEngine(1).random(n), RandomEngine(1).random(n) # gera valor posicional
    for i in range(n):
        if y[i,0] <= f(x[i,0]):
            soma += 1 # sucesso se estiver abaixo da linha da função
    
    mu = soma/n # calcula media 


    t1 = time.time()
    t = t1-t0
    print(f'calculado em {t} segundos') # tempo que levou para estimar

    return mu # Retorne sua estimativa



# Control Variate

# funcao que aproxima f(x) no intervalo e sua integral
def phi(x): return -0.3898874043587 * x + 1
def Phi(x): return -0.3898874043587/2 *x**2+x
    


def control_variate(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo control variate
    Escreva o seu codigo nas proximas linhas
    """

    t0 = time.time()
    n = 1000000 # inserir n
    soma = 0
    x = RandomEngine(1).random(n) 
    for i in range(n):
        soma += f(x[i,0]) - phi(x[i,0]) # diferenca em cada ponto sorteado



    mu = soma/n + Phi(1) - Phi(0) # media das diferencas e integral de phi no intervalo


    t1 = time.time()
    t = t1-t0
    print(f'calculado em {t} segundos') # tempo que levou para calcular


    return mu # Retorne sua estimativa



# Importance Sampling

# funcao que descreve a curva da disribuicao
def probexp(x, a=1, b=1):
    randg = a*exp(-a*x)/(1-exp(-b))
    return randg



def importance_sampling(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo importance sampling
    Escreva o seu codigo nas proximas linhas
    """
    t0 = time.time()
    n = 1000000 # a definir

    soma = 0
    for i in range(n):
        xi = truncexpon.rvs(b = 0.5, scale = 2) # gera valores randomicos segundo a distribuicao escolhida aproximada
        soma += f(xi)/probexp(xi,0.5, 0.5) # media ponderada

    mu = soma/n



    t1 = time.time()
    t = t1-t0
    print(f'calculado em {t} segundos') # tempo que leva para calcular

    return mu #Retorne sua estimativa





# definir convergências
def convergeCrude():
    global n
    x = [crude() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean

def convergeHoM():
    global n
    x = [hit_or_miss() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean

def convergeCV():
    global n
    x = [control_variate() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean

def convergeIS():
    global n
    x = [importance_sampling() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean





def main():
    #Coloque seus testes aqui
    print(f'crude: {crude()}\n')
    print(f'hit or miss: {hit_or_miss()}\n')
    print(f'control variate: {control_variate()}\n')
#    print(f'importance sampling: {importance_sampling()}\n')




if __name__ == "__main__":
    print('Quasi Random')
    # ver quando converge para crude
    t0 = time()
    n = 1
    a = convergeCrude()
    while 1:
        a = convergeCrude()
        if n >= 15366400*a[0]/(a[1]**2):
            break
        n *= 2
    t1 = time() - t0
    print(n, a[1], 'Calculado em', t1, 'segundos')



    # ver quando converge para hit or miss
    t0 = time()
    n = 1
    a = convergeHoM()
    while 1:
        a = convergeHoM()
        if n >= 15366400*a[0]/(a[1]**2):
            break
        n *= 2
    t1 = time() - t0
    print(n, a[1], 'Calculado em', t1, 'segundos')



    # ver quando converge para control variate
    t0 = time()
    n = 1
    a = convergeCV()
    while 1:
        a = convergeCV()
        if n >= 15366400*a[0]/(a[1]**2):
            break
        n*=2
    t1 = time() - t0
    print(n, a[1], 'Calculado em', t1, 'segundos')


    # ver quando converge para importance sampling
    t0 = time()
    n = 1
    a = convergeIS()
    while 1:
        a = convergeis()
        if n >= 15366400*a[0]/(a[1]**2):
            break
        n*=2
    t1 = time() - t0
    print(n, a[1], 'Calculado em', t1, 'segundos')

    #main()              
