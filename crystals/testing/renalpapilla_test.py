from unittest import TestCase
from crystals.renalpapilla import RenalPapilla
from crystals.constants import *
import math


class RenalPapillaTest(TestCase):
    def test_supersat_setter_consistency(self):
        rp = RenalPapilla(4, CAOX_SURFACE_ENERGY, GROWTH_ARRHENIUS_CONST, CAOX_CONTACT_ANGLE,
                          NUCLEATION_ARRHENIUS_CONST)

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
        expected = 1.9695e-22
        actual = RenalPapilla.calculate_nucleation_activation_barrier(5, CAOX_CONTACT_ANGLE,
                                                                      CAOX_SURFACE_ENERGY)
        self.assertAlmostEqual(expected * 1e22, actual * 1e22, 3)

    def test_nucleation_rate(self):
        caox_ss = 5
        expected = 7.4710e-10
        actual = RenalPapilla.calculate_nucleation_rate(caox_ss, CAOX_CONTACT_ANGLE, NUCLEATION_ARRHENIUS_CONST,
                                                        CAOX_SURFACE_ENERGY)
        self.assertAlmostEqual(expected * 1e10, actual * 1e10, 3)
