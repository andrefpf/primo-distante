from random_generator import RandomGenerator
from math import log2, ceil


def miller_rabin(n: int, *, trials=1) -> bool:
    """
    Test if n is (probably) prime.
    """

    # finds the bigger d and s such that
    # (2 ** s) * d == n - 1
    s = 0
    d = n - 1
    while s % 2 == 0:
        s += 1
        d //= 2

    gen = RandomGenerator(num_bits=ceil(log2(n)))

    for _ in range(trials):
        a = gen.generate(2, n)
        x = a**d % n

        for _ in range(s):
            y = x * x % n
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y

        if y != 1:
            return False

    return True


def fermat(n: int) -> bool:
    gen = RandomGenerator(num_bits=ceil(log2(n)))
    a = gen.generate(2, n)
    return a ** (n - 1) % n == 1
