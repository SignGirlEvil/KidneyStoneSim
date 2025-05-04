# File: distributions_test.py

import unittest
from utils.distributions import *


class DistributionsTest(unittest.TestCase):
    def test_exp_dist_cdf_below_zero(self):
        expected = 0.0
        actual = exp_dist_cdf(-0.1, 1)

        self.assertEqual(expected, actual)

    def test_exp_dist_cdf_above_zero_case_1(self):
        expected = 0.864665  # Found using my TI-84 calculator
        actual = exp_dist_cdf(1, 2)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_exp_dist_cdf_above_zero_case_2(self):
        expected = 0.789864  # Found using my TI-84 calculator
        actual = exp_dist_cdf(0.4, 3.9)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_exp_dist_cdf_negative_rate(self):
        self.assertRaises(ValueError, exp_dist_cdf, x=1, rate_param=-1)

    def test_exp_dist_cdf_zero_rate(self):
        self.assertRaises(ValueError, exp_dist_cdf, x=1, rate_param=0.0)

    def test_exp_dist_cdf_inverse_p_below_zero(self):
        self.assertRaises(ValueError, exp_dist_cdf_inverse, p=-1, rate_param=1.0)

    def test_exp_dist_cdf_inverse_p_equals_one(self):
        self.assertRaises(ValueError, exp_dist_cdf_inverse, p=1, rate_param=1.0)

    def test_exp_dist_cdf_inverse_p_above_one(self):
        self.assertRaises(ValueError, exp_dist_cdf_inverse, p=1.1, rate_param=1.0)

    def test_exp_dist_cdf_inverse_negative_rate(self):
        self.assertRaises(ValueError, exp_dist_cdf_inverse, p=0.5, rate_param=-1.0)

    def test_exp_dist_cdf_inverse_case_1(self):
        expected = 1.0
        actual = exp_dist_cdf_inverse(0.864665, 2)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_exp_dist_cdf_inverse_case_2(self):
        expected = 0.4
        actual = exp_dist_cdf_inverse(0.789864, 3.9)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_tri_dist_cdf_inverse_p_below_zero(self):
        self.assertRaises(ValueError, triangular_dist_cdf_inverse, p=-1, low_bound=1.0, high_bound=2.0, mode=1.75)

    def test_tri_dist_cdf_inverse_p_equals_one(self):
        self.assertRaises(ValueError, triangular_dist_cdf_inverse, p=1, low_bound=1.0, high_bound=2.0, mode=1.75)

    def test_tri_dist_cdf_inverse_p_above_one(self):
        self.assertRaises(ValueError, triangular_dist_cdf_inverse, p=1.1, low_bound=1.0, high_bound=2.0, mode=1.75)

    def test_tri_dist_cdf_inverse_case_1(self):
        expected = 1.5
        actual = triangular_dist_cdf_inverse(p=0.333333, low_bound=1.0, high_bound=2.0, mode=1.75)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_tri_dist_cdf_inverse_case_2(self):
        expected = 1.9
        actual = triangular_dist_cdf_inverse(p=0.96, low_bound=1.0, high_bound=2.0, mode=1.75)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_normal_dist_cdf_inverse_case_1(self):
        expected = 2.9
        actual = normal_dist_cdf_inverse(p=0.62551583, mean=2.5, stdev=1.25)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_normal_dist_cdf_inverse_case_2(self):
        expected = -1.4
        actual = normal_dist_cdf_inverse(p=0.00090426, mean=2.5, stdev=1.25)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_beta_dist_cdf_inverse_case_1(self):
        expected = 17.0
        actual = beta_dist_cdf_inverse(p=0.910, alph=1, bet=2, low_bound=10, high_bound=20)

        self.assertAlmostEqual(expected, actual, places=5)

    def test_beta_dist_cdf_inverse_case_2(self):
        expected = 14.0
        actual = beta_dist_cdf_inverse(p=0.640, alph=1, bet=2, low_bound=10, high_bound=20)

        self.assertAlmostEqual(expected, actual, places=5)
