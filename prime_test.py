from random_generator import RandomGenerator
from math import log2, ceil


def miller_rabin(n: int, *, trials: int = 10) -> bool:
    """
    O teste de primalidade de miller rabin é baseado em uma generalização do 
    pequeno teorema de Fermat.

    No caso onde todas as bases possíveis são testadas, este algoritmo seria
    determinístico e a resposta sempre seria correta. Porém a complexidade 
    seria exponencial, tornando inviável a utilização em computadores atuais.

    Para contornar o problema o teste é feito de maneira probabilística, testando
    com um número grande de bases escolhidas aleatóriamente e torcendo para que
    os deuses da probabilidade não tenha escolhido justamente as piores possíveis.
    """

    if n % 2 == 0:
        return False

    # finds the bigger d and s such that
    # (2 ** s) * d == n - 1
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    gen = RandomGenerator(num_bits=ceil(log2(n)))

    for _ in range(trials):
        a = gen.generate(2, n)
        x = pow(a, d, n)

        for _ in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y

        if y != 1:
            return False

    return True


def fermat(n: int, *, trials: int = 10) -> bool:
    '''
    Este teste é baseado do pequeno teorema de Fermat, 
    que afirma que a^(p-1) ≡ 1 (mod p) desde que p seja um número
    primo e que a seja menor do que p. 

    O teste funciona de maneira inversa, pois qualquer número primo passa
    no teste, mas não necessariamente SÓ numeros primos passam. Para ter um
    pouco mais de certeza do resultado o teste é feito <trials> vezes.

    Apesar disso é sabido que ainda existem números pseudoprimos que passam neste
    teste independente da base escolhida. 
    '''

    for _ in range(trials):
        gen = RandomGenerator(num_bits=ceil(log2(n)))
        a = gen.generate(2, n)
        if pow(a, (n - 1), n) != 1:
            return False
    return True
