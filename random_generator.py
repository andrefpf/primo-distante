from time import time


def xorshift_32(seed):
    modulus = 1 << 32
    while True:
        seed ^= seed >> 13
        seed ^= seed >> 17
        seed ^= seed << 5
        yield seed % modulus


def lcg_32(seed):
    multiplier = 1664525
    increment = 1013904223
    modulus = 1 << 32
    while True:
        seed = (multiplier * seed + increment) % modulus
        yield seed


class RandomGenerator:
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
