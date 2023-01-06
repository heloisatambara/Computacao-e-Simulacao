import scipy as sp
from scipy.sparse import linalg, csr_matrix
import numpy as np
from math import exp, cos, sin, log2

def u(x):
    y = exp(cos(x))
    return y

def f(x):
    y = (cos(x)-(sin(x))**2)*exp(cos(x))
    return y



def create_matrix(n):
    A= np.zeros((n, n))

    
 # gera o meio da matriz
    for i in range(2,n-2):
        A[i,(i-2)%n] = -1
        A[i,(i-1)%n] = 16
        A[i,i] = -30
        A[i,(i+1)%n] = 16
        A[i,(i+2)%n] = -1
    
 # arruma ao início e o fim   
    A[0,0],A[0,1] = -2, 1
    A[1,0], A[1,1], A[1,2] =1, -2, 1 
    
    A[n-1,n-1], A[n-1,n-2] =-2, 1
    A[n-2,n-1], A[n-2,n-2], A[n-2,n-3]=1, -2, 1

    return A



def erro(u, norma, Solution):
    return np.linalg.norm((u - Solution), norma)

def p(i, norma, Solution):
    p = erro(i, norma, Solution)/erro(i/2, norma, Solution) 
    return p





def main():
    a = 0
    b = 1
    n = 128
    print("n          h            erro 1            erro 2        log")
    while n <= 16384:
        h = (b-a)/n
 # cria a matriz A
        A = create_matrix(n)
        
 # cria o vetor B a partir da matriz A e o vetor real de u
        vetor = [u(a + h*k) for k in range(n)]
        B = np.dot(A, vetor)
 # acha a solução pelo método de diferenças finitas
        A = csr_matrix(A)
        Solution = sp.sparse.linalg.spsolve(A, B.astype(np.float64))
        #print(Solution)
        #print(vetor)

        e1 = erro(vetor, 2, Solution)
        e2 = erro(vetor, np.inf, Solution)
        pe = p(n, 2, Solution)
        print(n, h, e1, e2, pe)
        n *= 2
        

main()
