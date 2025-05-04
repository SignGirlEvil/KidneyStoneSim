import unittest
from utils.sphere_math import *


class SphereMathTest(unittest.TestCase):
    def test_volume_from_radius(self):
        expected = 7.606
        actual = volume_from_radius(1.22)
        self.assertAlmostEqual(expected, actual, 3)

    def test_radius_from_volume(self):
        expected = 1.22
        actual = radius_from_volume(7.606)
        self.assertAlmostEqual(expected, actual, 3)
