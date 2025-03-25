import random
import numpy as np


def exp(time_mean):
    a = 0.0
    while a == 0:
        a = random.random()
    a = -time_mean * np.log(a)
    return a


def uniform(time_min, time_max):
    a = 0.0
    while a == 0:
        a = random.random()
    a = time_min + a * (time_max - time_min)
    return a


def norm(time_mean, time_deviation):
    return time_mean + time_deviation * random.gauss(0.0, 1.0)


def erlang(time_mean, k):
    a = 1
    for i in range(k):
        a *= random.random()
    return - np.log(a) / (k * time_mean)


def empirical(x, y):
    n = len(x)
    r = random.random()
    for i in range(1, n - 1):
        if y[i - 1] < r <= y[i]:
            a = x[i - 1] + (r - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1])
            return a

    a = x[n - 2] + (r - y[n - 2]) * (x[n - 1] - x[n - 2]) / (y[n - 1] - y[n - 2])
    return a
