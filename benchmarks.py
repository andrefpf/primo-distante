from tabulate import tabulate
from time import time
from random_generator import RandomGenerator, xorshift_32, lcg_32
from prime_test import fermat, miller_rabin
from prime_generator import generate_prime


def benchmark_xorshift():
    number_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    gen = RandomGenerator(algorithm=xorshift_32)

    table = []

    for size in number_sizes:
        gen.num_bits = size
        s = time()
        for i in range(500):
            gen.generate()
        e = time()
        print(size)
        table.append(["xorshift", f"{size} bits", f"{(e-s):.3f} sec"])

    print(tabulate(table, tablefmt="fancy_grid"))


def benchmark_lcg():
    number_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    gen = RandomGenerator(algorithm=lcg_32)

    table = []

    for size in number_sizes:
        gen.num_bits = size
        s = time()
        for i in range(500):
            gen.generate()
        e = time()
        print(size)
        table.append(["lcg", f"{size} bits", f"{(e-s):.3f} sec"])

    print(tabulate(table, tablefmt="fancy_grid"))


def benchmark_fermat():
    number_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    table = []

    for size in number_sizes:
        s = time()
        prime = generate_prime(size, xorshift_32, fermat)
        e = time()
        row = ["Fermat + xorshift", f"{size} bits", f"prime found: {prime}", f"{(e-s):.3f} sec"]
        print(size)
        table.append(row)
    print()

    for size in number_sizes:
        s = time()
        prime = generate_prime(size, lcg_32, fermat)
        e = time()
        print(size)
        row = ["Fermat + LCG", f"{size} bits", f"prime found: {prime}", f"{(e-s):.3f} sec"]
        table.append(row)

    print(tabulate(table, tablefmt="fancy_grid"))


def benchmark_miller_rabin():
    number_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    table = []

    for size in number_sizes:
        s = time()
        prime = generate_prime(size, xorshift_32, miller_rabin)
        e = time()
        row = ["Miller Rabin + xorshift", f"{size} bits", f"prime found: {prime}", f"{(e-s):.3f} sec"]
        print(size)
        table.append(row)
    print()

    for size in number_sizes:
        s = time()
        prime = generate_prime(size, lcg_32, miller_rabin)
        e = time()
        row = ["Miller Rabin + LCG", f"{size} bits", f"prime found: {prime}", f"{(e-s):.3f} sec"]
        print(size)
        table.append(row)

    print(tabulate(table, tablefmt="fancy_grid"))


benchmark_xorshift()
benchmark_lcg()

benchmark_fermat()
benchmark_miller_rabin()