##!/usr/bin/env python3
# -*- coding: utf-8 -*-




from scipy.stats import qmc
from math import exp, cos, log
from time import time
import random
#Escreva seu nome e numero USP
INFO = {12556819:"Heloisa Tambara"}
A = 0.397318431 # A = 0.rg
B = 0.43292242835  # B = 0.cpf


def f(x):
    """
    Esta funcao deve receber x e devolver f(x), como especifcado no enunciado
    Escreva o seu codigo nas proximas linhas
    """
    A = 0.397318431 # A = 0.rg
    B = 0.43292242835  # B = 0.cpf
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
    global n #inserir n
    soma = 0
    sampler = qmc.Sobol(d=1, scramble=True)
    sample = sampler.random_base2(m=n)
    for x in range(2**n): # gerar 2^n numeros x, calcular suas f(x), somar tudo e dividir por 2^n
        soma += f(sample[x,0])
    mu = soma/2**n

    return mu # Retorne sua estimativa




# Hit or Miss
def hit_or_miss(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo hit or miss
    Escreva o seu codigo nas proximas linhas
    """
    global n # inserir n
    soma = 0
    sampler = qmc.Sobol(d=2, scramble=True)
    sample = sampler.random_base2(m=n)
    x, y = sample[:,0], sample[:,1] # gera valor posicional
    for i in range(2**n):
        if y[i] <= f(x[i]):
            soma += 1 # sucesso se estiver abaixo da linha da função
    mu = soma/2**n # calcula media 

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
    global n # inserir n
    soma = 0
    sampler = qmc.Sobol(d=1, scramble=True)
    x = sampler.random_base2(m=n)
    for i in range(2**n):
        soma += f(x[i,0]) - phi(x[i,0]) # diferenca em cada ponto sorteado
    mu = soma/2**n + Phi(1) - Phi(0) # media das diferencas e integral de phi no intervalo
    return mu # Retorne sua estimativa



# Importance Sampling

# funcao que descreve a curva da disribuicao
def fcp(x, a=1):
    y = - exp(-a*x)/(1-exp(-a)) #- 0.3
    zero = - exp(-a*0)/(1-exp(-a))
    return y - zero

def fdp(x, a=1):
    y = a*exp(-a*x)/(1-exp(-a))
    return y


def importance_sampling(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo importance sampling
    Escreva o seu codigo nas proximas linhas
    """
    global n # a definir
    sampler = qmc.Sobol(d=1, scramble=True)
    x = sampler.random_base2(m=n)
    x1 = [fcp(i,0.5) for i in x]
    x2 = [fdp(i, .5) for i in x1]
    soma = 0
    for i in range(2**n):
        soma += f(x1[i])/x2[i] # media ponderada

    mu = soma/2**n

    return mu #Retorne sua estimativa




# definir convergências
def convergeCrude():
    x = [crude() for i in range(100)] # gera 100 estimadores
    x2 = [X**2 for X in x]
    mean = (sum(x)/100) # calcula media dos estimadores
    var = sum(x2)/100 - mean**2 # variancia dos estimadores
    return var, mean

def convergeHoM():
    x = [hit_or_miss() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean

def convergeCV():
    x = [control_variate() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean

def convergeIS():
    x = [importance_sampling() for i in range(100)]
   # print(x[1:10])
    x2 = [X**2 for X in x]
    mean = (sum(x)/100)
    var = sum(x2)/100 - mean**2
    return var, mean





def main():
    #Coloque seus testes aqui
    print('Para n = 2^10:')
    print(f'crude: {crude()}\n')
    print(f'hit or miss: {hit_or_miss()}\n')
    print(f'control variate: {control_variate()}\n')
    print(f'importance sampling: {importance_sampling()}\n')




if __name__ == "__main__":
    n = 10
    main()

    print('Quasi Random convergência')
    # ver quando converge para crude
    t0 = time()
    n = 1
    a = convergeCrude()
    while 1:
        a = convergeCrude()
        if 2**n >= 15366400*a[0]/(a[1]**2): # condicao do intervalo de confianca
            break
        n += 1
    t1 = time() - t0
    print(f'n = {2**n}, crude = {a[1]},  Calculado em {t1} segundos')


    # ver quando converge para hit or miss
    t0 = time()
    n = 1
    a = convergeHoM()
    while 1:
        a = convergeHoM()
        if 2**n >= 15366400*a[0]/(a[1]**2):
            break
        n += 1
    t1 = time() - t0
    print(f'n = {2**n}, hom = {a[1]},  Calculado em {t1} segundos')


    # ver quando converge para control variate
    t0 = time()
    n = 1
    a = convergeCV()
    while 1:
        a = convergeCV()
        if 2**n >= 15366400*a[0]/(a[1]**2):
            break
        n += 1
    t1 = time() - t0
    print(f'n = {2**n}, cv = {a[1]},  Calculado em {t1} segundos')


    # ver quando converge para importance sampling
    t0 = time()
    n = 1
    a = convergeIS()
    while 1:
        a = convergeIS()
        if 2**n >= 15366400*a[0]/(a[1]**2):
            break
        n += 1
    t1 = time() - t0

    print(f'n = {2**n}, is = {a[1]},  Calculado em {t1} segundos')

