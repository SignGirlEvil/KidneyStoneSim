from unittest import TestCase
from crystals.crystal import Crystal
from crystals.constants import GROWTH_ARRHENIUS_CONST
import math


class CrystalTest(TestCase):
    def test_neg_nucleation_time(self):
        self.assertRaises(ValueError, Crystal, -1, 2, 1, 1)

    def test_release_time_after_nucleation_time(self):
        self.assertRaises(ValueError, Crystal, 3, 2, 1, 1)

    def test_location_below_zero(self):
        self.assertRaises(ValueError, Crystal, 2, 3, 1, -1)

    def test_location_above_one(self):
        self.assertRaises(ValueError, Crystal, 2, 3, 1, 1.1)

    def test_less_than(self):
        lesser_crystal = Crystal(1, 2, 3, 0.1)
        greater_crystal = Crystal(1, 2, 3, 0.2)
        self.assertLess(lesser_crystal, greater_crystal)

    def test_radius(self):
        c = Crystal(1, 2, 3, 0.5)
        c.volume = 4

        expected = 0.9847
        actual = c.radius
        self.assertAlmostEqual(expected, actual, 4)

    def test_growth_activation_barrier(self):
        expected = 2.7345e-18
        actual = Crystal.calculate_growth_activation_barrier(5)
        self.assertAlmostEqual(expected, actual, 4)

    def test_growth_constant(self):
        caox_ss = 9
        pre_exp = (caox_ss - 1) * GROWTH_ARRHENIUS_CONST
        expected = pre_exp * math.exp(-467.9839)
        actual = Crystal.calculate_growth_constant(caox_ss)
        self.assertAlmostEqual(expected, actual, 30)

    def test_max_lifespan(self):
        expected = 2.56496
        actual = Crystal.calculate_max_lifespan(2, 5)
        self.assertAlmostEqual(expected, actual, 5)

    def test_grow_vol_starts_at_zero(self):
        c = Crystal(1, 10, 2, 0.5)
        c.grow(3)

        expected = 8.0
        actual = c.volume
        self.assertAlmostEqual(expected, actual)

    def test_grow_vol_starts_at_non_zero(self):
        c = Crystal(1, 10, 2, 0.5)
        c.volume = 1.5
        c.grow(3)

        expected = 31.0988
        actual = c.volume
        self.assertAlmostEqual(expected, actual, 4)

    def test_update_once(self):
        c = Crystal(0, 10, 2, 0.5)
        c.update(3)

        expected = 8.0
        actual = c.volume
        self.assertAlmostEqual(expected, actual)

    def test_update_twice(self):
        c = Crystal(0, 10, 2, 0.5)
        c.update(3)
        c.update(6)

        expected = 64.0
        actual = c.volume
        self.assertAlmostEqual(expected, actual)

    def test_update_twice_with_volume_add_in_between(self):
        c = Crystal(0, 10, 2, 0.5)
        c.update(3)
        c.volume += 2.0
        c.update(6)

        expected = 71.7027
        actual = c.volume
        self.assertAlmostEqual(expected, actual, 4)
