from crystals.constants import *
from utils import radius_from_volume, volume_from_radius
import math


class Crystal:
    def __init__(self, nucleation_time: float, release_time: float, growth_constant: float, location: float):
        if nucleation_time < 0:
            raise ValueError('Nucleation time must be positive.')

        if nucleation_time > release_time:
            raise ValueError('Nucleation must occur before release.')

        if not (0 <= location <= 1):
            raise ValueError('Location must be between zero and one, inclusive.')

        self.nucleation_time: float = nucleation_time
        self.release_time: float = release_time
        self._growth_const: float = growth_constant
        self.location: float = location

        self.last_update_time: float = nucleation_time
        self.volume: float = 0.0
        self.aggregation_occurred: bool = False

    def __repr__(self):
        return f'Crystal({self.nucleation_time:.1f} - {self.release_time:.1f})'

    def __str__(self):
        return f'Crystal with volume of {self.volume:.3f}'

    def __lt__(self, other):
        return self.location < other.location

    @property
    def radius(self) -> float:
        return radius_from_volume(self.volume)

    @staticmethod
    def calculate_growth_activation_barrier(caox_supersaturation: float, surface_energy: float) -> float:
        numerator = math.pi * (2 * CAOX_MOLECULE_RADIUS) * (surface_energy ** 2) * CAOX_MOLECULE_VOL
        denominator = THERMAL_ENERGY * math.log(caox_supersaturation)
        return numerator / denominator

    @staticmethod
    def calculate_growth_constant(caox_supersaturation: float, surface_energy: float, growth_arrhenius: float) -> float:
        activation_barrier = Crystal.calculate_growth_activation_barrier(caox_supersaturation, surface_energy)
        return growth_arrhenius * math.exp(-activation_barrier / THERMAL_ENERGY)

    @staticmethod
    def calculate_max_lifespan(growth_constant: float, max_volume: float) -> float:
        if growth_constant <= 0:
            return 1e50

        return 3 * (max_volume ** ONE_THIRD) / growth_constant

    @staticmethod
    def calculate_min_problem_lifespan(growth_constant: float) -> float:
        problem_volume = volume_from_radius(PROBLEM_RADIUS)
        return Crystal.calculate_max_lifespan(growth_constant, problem_volume)

    def grow(self, growth_time: float) -> None:
        self.volume = ((self._growth_const * growth_time / 3) + (self.volume ** ONE_THIRD)) ** 3

    def update(self, current_time: float) -> None:
        grow_time = current_time - self.last_update_time
        self.grow(grow_time)
        self.last_update_time = current_time
