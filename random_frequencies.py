from random_generator import xorshift_32, lcg_32
import matplotlib.pyplot as plt
import numpy as np


def create_histogram(data, num_classes):
    histogram = [0 for i in range(num_classes)]
    for i in data:
        bucket = i * num_classes // (1 << 32)
        histogram[bucket] += 1
    return histogram


def evaluate_algorithm(algorithm, seed, repetitions):
    generator = algorithm(seed)
    random_values = [next(generator) for i in range(repetitions)]
    return create_histogram(random_values, 32)


xorshift_frequency = evaluate_algorithm(xorshift_32, 1234, 10_000)
lcg_frequency = evaluate_algorithm(lcg_32, 1234, 10_000)

x = range(len(xorshift_frequency))
plt.bar(x, xorshift_frequency, color="darkblue")
plt.bar(x, lcg_frequency, color="darkred")
plt.show()
