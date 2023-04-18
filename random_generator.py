from time import time


def xorshift_32(seed):
    '''
    Implementação do algoritmo de xorshift para geração de números aleatórios de 32 bits.
    Isso é um gerador, então baseado em um seed ele embaralha os bits com deslocamentos
    e xors, e utiliza o valor anterior para gerar o próximo infinitamente.
    '''
    modulus = 1 << 32
    while True:
        seed ^= seed << 13
        seed ^= seed >> 17
        seed ^= seed << 5
        yield seed % modulus


def lcg_32(seed):
    '''
    Implementação do algoritmo Linear Congruential Generator de 32 bits. 
    Isso também é um gerador que a partir de um único seed que a cada iteração atualiza o valor
    anterior e retorna em seguida. 
    
    Esse algoritmo funciona multiplicando o seed por um valor enorme, somando outro valor igualmente
    enorme e calculando o módulo necessário, nesse caso 32 bits. O valor da operação linear é meio 
    imprevisível mas sempre será um número de 32 bits.

    Em python não preciso me preocupar com overflow, por isso o cálculo é feito assim diretamente.
    '''
    multiplier = 1372383749
    increment = 1289706101
    modulus = 1 << 32
    while True:
        seed = (multiplier * seed + increment) % modulus
        yield seed


class RandomGenerator:
    '''
    Essa classe é responsável por gerar números aleatórios de tamanhos arbitrários.
    Para isso a classe gera números de tamanhos fixos, tarefa muito mais fácil e rápida
    e em seguida concatena todos eles cuidando especialmente nas partes finais.

    Detalhe importante: O algoritmo não gera números de EXATAMENTE num_bits, e sim números
    de até num_bits. Devido às magias da probabilidade os números costumam ser bem grandes
    e próximos do máximo.

    Para gerar números de exatamente num_bits bastaria setar em 1 o bit na posição (1 << num_bits),
    mas isso não parece vantajoso no contexto de geração de primos.
    '''

    def __init__(self, *, seed=None, algorithm=None, num_bits=64):
        if seed is None:
            seed = int(time())  # sec people love this one

        if algorithm is None:
            algorithm = lcg_32

        self.seed = seed
        self.num_bits = num_bits
        self.generator_32 = algorithm(seed)

        self._iterator = iter(self)

    def generate(self, minimum=0, maximum=None):
        rand = next(self)
        if maximum is not None:
            rand %= maximum - minimum
        rand += minimum
        return rand

    def __iter__(self):
        random_blocks = self.num_bits // 32
        remaining_block = self.num_bits % 32

        while True:
            val = 0
            for _ in range(random_blocks):
                val <<= 32
                val |= next(self.generator_32)

            if remaining_block:
                val <<= remaining_block
                val |= next(self.generator_32) % (1 << remaining_block)

            yield val

    def __next__(self):
        return next(self._iterator)


if __name__ == "__main__":
    gen = RandomGenerator()
    for i in range(100):
        rand = gen.generate()
        print(i, rand)
        assert (len(bin(rand)) - 2) == 64
