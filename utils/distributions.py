# File: distributions.py
import math
from math import exp, log, sqrt
from random import random
from scipy.special import erfinv
from scipy.stats import beta


# Returns the likelihood of a random event occurring with x amount of time
def exp_dist_cdf(x: float, rate_param: float) -> float:
    if rate_param <= 0.0:
        raise ValueError('The rate parameter must be a positive, non-zero number.')

    if x < 0:
        return 0
    else:
        return 1 - exp(-rate_param * x)


# Returns the x-value for the exponential distribution CDF that yields probability p
def exp_dist_cdf_inverse(p: float, rate_param: float) -> float:
    if rate_param <= 0.0:
        raise ValueError('The rate parameter must be a positive, non-zero number.')

    if not (0.0 <= p < 1.0):
        raise ValueError('The probability cannot be less than zero, equal to one, or greater than one')

    return -log(1 - p) / rate_param


def sample_exp_dist(rate_param: float) -> float:
    return exp_dist_cdf_inverse(random(), rate_param)


def triangular_dist_cdf_inverse(p: float, low_bound: float, high_bound: float, mode: float) -> float:
    if not (0.0 <= p < 1.0):
        raise ValueError('The probability cannot be less than zero, equal to one, or greater than one')

    inflection_pt = (mode - low_bound) / (high_bound - low_bound)

    if p <= inflection_pt:
        mult = (high_bound - low_bound) * (mode - low_bound)
        return sqrt(mult * p) + low_bound
    else:
        mult = (high_bound - low_bound) * (high_bound - mode)
        return high_bound - sqrt(mult * (1 - p))


def sample_triangular_dist(low_bound: float, high_bound: float, mode: float) -> float:
    return triangular_dist_cdf_inverse(random(), low_bound, high_bound, mode)


def normal_dist_cdf_inverse(p: float, mean: float, stdev: float) -> float:
    return mean + (stdev * math.sqrt(2) * erfinv((2 * p) - 1))


def sample_normal_dist(mean: float, stdev: float) -> float:
    return normal_dist_cdf_inverse(random(), mean, stdev)


def beta_dist_cdf_inverse(p: float, alph: float, bet: float, low_bound: float = 0.0, high_bound: float = 1.0) -> float:
    scale = high_bound - low_bound
    loc = low_bound
    return beta.ppf(p, alph, bet, loc, scale)


def sample_beta_dist(alph: float, bet: float, low_bound: float = 0.0, high_bound: float = 1.0) -> float:
    return beta_dist_cdf_inverse(random(), alph, bet, low_bound, high_bound)
