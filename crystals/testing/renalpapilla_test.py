from unittest import TestCase
from crystals.renalpapilla import RenalPapilla
from crystals.constants import CAOX_CONTACT_ANGLE, NUCLEATION_ARRHENIUS_CONST, THERMAL_ENERGY
import math


class RenalPapillaTest(TestCase):
    def test_supersat_setter_consistency(self):
        rp = RenalPapilla(4)

        old_nuc_rate = rp.nucleation_rate
        old_grow_const = rp.growth_constant
        old_max_life = rp.max_crystal_lifespan

        rp.supersaturation = 4

        new_nuc_rate = rp.nucleation_rate
        new_grow_const = rp.growth_constant
        new_max_life = rp.max_crystal_lifespan

        self.assertAlmostEqual(old_nuc_rate, new_nuc_rate, msg='Nucleation rates don\'t equal')
        self.assertAlmostEqual(old_grow_const, new_grow_const, msg='Growth constants don\'t equal')
        self.assertAlmostEqual(old_max_life, new_max_life, msg='Max crystal lifespans don\'t equal')

    def test_het_mult(self):
        expected = 0.0938399
        actual = RenalPapilla.calculate_heterogeneous_multiplier(0.9)
        self.assertAlmostEqual(expected, actual, 5)

    def test_nucleation_activation_barrier(self):
        het_mult = RenalPapilla.calculate_heterogeneous_multiplier(math.radians(CAOX_CONTACT_ANGLE))
        expected = het_mult * 1.186262e-16
        actual = RenalPapilla.calculate_nucleation_activation_barrier(5)
        self.assertAlmostEqual(expected, actual, 20)

    def test_nucleation_rate(self):
        caox_ss = 5
        activation_barrier = RenalPapilla.calculate_nucleation_activation_barrier(caox_ss)
        pre_exp = (caox_ss - 1) * NUCLEATION_ARRHENIUS_CONST
        expected = pre_exp * math.exp(-activation_barrier / THERMAL_ENERGY)
        actual = RenalPapilla.calculate_nucleation_rate(caox_ss)
        self.assertAlmostEqual(expected, actual, 20)
