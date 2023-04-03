from random_generator import RandomGenerator, xorshift_32
from time import time
from prime_test import miller_rabin

def generate_prime(num_bits, random_algorithm, prime_test_algorithm):
    generator = RandomGenerator(num_bits=num_bits, algorithm=random_algorithm)

    for i, random in enumerate(generator):
        if random % 2 == 0:
            random += 1

        if prime_test_algorithm(random):
            return random
