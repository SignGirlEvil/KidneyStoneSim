from .renalpapilla import RenalPapilla
from .constants import *


class Kidney:
    def __init__(self, supersaturation: float, contact_angle: float = CAOX_CONTACT_ANGLE,
                 surface_energy: float = CAOX_SURFACE_ENERGY, nuc_arr: float = NUCLEATION_ARRHENIUS_CONST,
                 grow_arr: float = GROWTH_ARRHENIUS_CONST):
        self.supersaturation = supersaturation
        self.num_papilla = 26
        self.contact_angle = contact_angle
        self.surface_energy = surface_energy
        self.nucleation_arrhenius = nuc_arr
        self.growth_arrhenius = grow_arr

    def determine_time_until_stone(self, max_time: float = 1e50, max_crystals: int = 1000000,
                                   include_prints: bool = False) -> float:
        stone_times: list[float] = []
        papilla = RenalPapilla(self.supersaturation, self.surface_energy, self.growth_arrhenius, self.contact_angle,
                               self.nucleation_arrhenius)

        for i in range(self.num_papilla):
            if include_prints:
                print(f'Iteration: {i}')

            stone_times.append(papilla.determine_time_until_stone(max_time, max_crystals, include_prints))

            if include_prints:
                print(f'Time: {stone_times[-1]:.3e} seconds\n')

        return min(stone_times)
