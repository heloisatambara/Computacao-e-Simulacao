import random
import time

def estima_pi(Seed = None):

    random.seed(Seed)
    #random.random() gera um numero com distribuicao uniforme em (0,1)
    """
    Esta funcao deve retornar a sua estimativa para o valor de PI
    Escreva o seu codigo nas proximas linhas
    """
    t0 = time.time() 
    n = 0 
    A = 1
    total = 0 
    while A:

        n += 1
        x, y = random.uniform(-1,1), random.uniform(-1,1) # gera um valor posicional dentro do quadrado -1 a 1
        inCircunference = x**2 + y**2 <= 1 # define se o valor gerado esta dentro da circunferencia

        if inCircunference: # atribui o resultado da Bernoulli (1 = sucesso - dentro do circulo, 0 = fracasso - fora do circulo)
            r = 1
        else:
            r = 0

        total += r 
            
        
        p = total/n # porcentagem que caiu dentro do cicrulo
        pi = p*4 # sabemos, do valor da area do quadrado e do circulo, que a probabilidade de cair dentro do circulo e pi/4, portanto pi = p*4
        if pi: aux = 61465600/pi**2 # se ja houver um valor de pi diferente de 0, calcula se n ja e grande o suficiente para o erro desejado
        if n >= 3841600 and n >= aux: 
            A = 0 # acaba o loop
    
    print(f'n={n}')
    t1 = time.time() - t0
    print(f'Rodou em {t1} segundos')
    return pi #Retorne sua estimativa

pi = estima_pi()
print(pi)
