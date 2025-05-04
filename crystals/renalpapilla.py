from .constants import *
from .crystal import Crystal
from random import random
from utils import distributions
import math


class RenalPapilla:
    RENAL_PAP_DIAM = 3e-3  # m
    RENAL_PAP_CROSS_SECTIONAL_AREA = 0.25 * math.pi * (RENAL_PAP_DIAM ** 2)  # m^2

    RENAL_PAP_MIN_LEN = 6.5e-3  # m (https://www.knowyourbody.net/renal-papilla.html)
    RENAL_PAP_MAX_LEN = 14e-3  # m (https://www.knowyourbody.net/renal-papilla.html)
    RENAL_PAP_LEN = 10.5e-3  # m (Halfway between min and max length)

    RENAL_PAP_SURFACE_AREA = RENAL_PAP_CROSS_SECTIONAL_AREA * RENAL_PAP_LEN  # m^2 (7.422012644105886e-08)

    PLASMA_VOLUME_FLOW = 1e-5  # m^3 / s
    PLASMA_VELOCITY = PLASMA_VOLUME_FLOW / RENAL_PAP_CROSS_SECTIONAL_AREA  # m / s

    def __init__(self, supersaturation: float):
        self._supersaturation: float = supersaturation
        self._nucleation_rate = self.calculate_nucleation_rate(supersaturation)

        max_crystal_volume = 4 * ONE_THIRD * math.pi * ((self.RENAL_PAP_DIAM / 2.0) ** 3)
        self._growth_constant = Crystal.calculate_growth_constant(supersaturation)
        self._max_crystal_lifespan = Crystal.calculate_max_lifespan(self._growth_constant, max_crystal_volume)

    @property
    def supersaturation(self) -> float:
        return self._supersaturation

    @supersaturation.setter
    def supersaturation(self, new_ss: float):
        self._supersaturation = new_ss
        self._nucleation_rate = self.calculate_nucleation_rate(new_ss)

        max_crystal_volume = 4 * ONE_THIRD * math.pi * ((self.RENAL_PAP_DIAM / 2.0) ** 3)
        self._growth_constant = Crystal.calculate_growth_constant(new_ss)
        self._max_crystal_lifespan = Crystal.calculate_max_lifespan(self._growth_constant, max_crystal_volume)

    @property
    def nucleation_rate(self) -> float:
        return self._nucleation_rate

    @property
    def growth_constant(self) -> float:
        return self._growth_constant

    @property
    def max_crystal_lifespan(self) -> float:
        return self._max_crystal_lifespan

    @staticmethod
    def calculate_heterogeneous_multiplier(theta: float) -> float:
        return (2.0 - (3.0 * math.cos(theta)) + (math.cos(theta) ** 3)) / 4.0

    @staticmethod
    def calculate_nucleation_activation_barrier(caox_supersaturation: float) -> float:
        het_mult = RenalPapilla.calculate_heterogeneous_multiplier(math.radians(CAOX_CONTACT_ANGLE))
        numerator = 16 * math.pi * (CAOX_SURFACE_ENERGY ** 3) * (CAOX_MOLECULE_VOL ** 2)
        denominator = 3 * ((THERMAL_ENERGY * math.log(caox_supersaturation)) ** 2)
        return het_mult * numerator / denominator

    @staticmethod
    def calculate_nucleation_rate(caox_supersaturation: float) -> float:
        activation_barrier = RenalPapilla.calculate_nucleation_activation_barrier(caox_supersaturation)
        return NUCLEATION_ARRHENIUS_CONST * math.exp(-activation_barrier / THERMAL_ENERGY)

    def determine_time_until_stone(self, max_time: float = 1e50, max_crystals: int = 1000,
                                   include_prints: bool = False) -> float:
        release_events: list[_ReleaseEvent] = []
        crystals: list[Crystal] = []

        next_nucleation_time = distributions.exp_dist_cdf_inverse(random(), self._nucleation_rate)
        next_release_time = next_nucleation_time + \
            distributions.sample_triangular_dist(0, self._max_crystal_lifespan, self._max_crystal_lifespan)
        curr_time = next_nucleation_time

        found_problem_crystal = False
        latest_time_until_stone = max_time
        min_problem_lifespan = Crystal.calculate_min_problem_lifespan(self._growth_constant)

        while curr_time <= max_time:
            # Continuously nucleate until a crystal is released
            while next_nucleation_time <= next_release_time:
                new_lifespan = distributions.exp_dist_cdf_inverse(random(), 1.0 / (0.2 * self._max_crystal_lifespan))
                new_release_time = next_nucleation_time + new_lifespan
                new_crystal = Crystal(next_nucleation_time, new_release_time, self._growth_constant, random())

                release_events.append(_ReleaseEvent(new_release_time, new_crystal))
                crystals.append(new_crystal)

                if new_lifespan >= min_problem_lifespan:
                    found_problem_crystal = True
                    latest_time_until_stone = min(new_release_time, latest_time_until_stone)

                    if include_prints:
                        print(f'Problem stone identified at time {next_nucleation_time:.3e} '
                              f'(with release at {new_release_time:.3e}) (Total crystals: {len(crystals)})')

                if include_prints:
                    print(f'Nucleation occurred at time {next_nucleation_time:.3e} making a crystal with a lifespan of '
                          f'{new_lifespan:.3e}', end=' ')

                next_nucleation_time += distributions.exp_dist_cdf_inverse(random(), self._nucleation_rate)
                next_release_time = min(new_release_time, next_release_time)

                if include_prints:
                    print(f'(next release at {next_release_time:.3e}) (Total crystals = {len(crystals)})', end=' ')
                    if found_problem_crystal:
                        print(f'(End time: {latest_time_until_stone - min_problem_lifespan:.3e})')

                if found_problem_crystal and (latest_time_until_stone - next_nucleation_time < min_problem_lifespan):
                    if include_prints:
                        print(f'No more opportunity for problem stone to form before {latest_time_until_stone:.3e}')
                    return latest_time_until_stone

                if found_problem_crystal and (len(crystals) >= max_crystals):
                    if include_prints:
                        print(f'Too many crystals, returning time soonest problem crystal will release ('
                              f'{latest_time_until_stone:.3e})')

                    return latest_time_until_stone

            # Update current time and crystal volumes
            curr_time = next_release_time
            for crystal in crystals:
                crystal.update(curr_time)

            if not release_events:
                next_release_time = next_nucleation_time + self._max_crystal_lifespan + 1
                continue

            # Sort the lists in preparation for what's to come
            crystals.sort()

            # Find and pop the crystal being released
            next_release_event_index = release_events.index(min(release_events))
            next_release_event = release_events.pop(next_release_event_index)
            released_crystal_index = crystals.index(next_release_event.crystal)
            released_crystal = crystals.pop(released_crystal_index)

            # Update next release time variable
            if release_events:
                next_release_time = min(release_events).time
            else:
                next_release_time = next_nucleation_time + self._max_crystal_lifespan + 1

            # Determine the likelihood of aggregation
            aggregation_chance_per_crystal = max(0, (PROBLEM_RADIUS - released_crystal.radius) / PROBLEM_RADIUS)
            num_crystals_downstream = len(crystals) - released_crystal_index
            chance_of_failing_aggregation = (1 - aggregation_chance_per_crystal) ** num_crystals_downstream

            # If it fails to aggregate, check its size and return the time if it's large
            if random() <= chance_of_failing_aggregation:
                if released_crystal.radius >= PROBLEM_RADIUS:
                    if include_prints:
                        print(f'Problem crystal escaped at time {curr_time:.3e} (Total crystals left = '
                              f'{len(crystals)}) (Aggregation occurred = {released_crystal.aggregation_occurred})')
                    return curr_time
                else:
                    if include_prints:
                        print(f'Non-problem crystal escaped at time {curr_time:.3e} (Total crystals left = '
                              f'{len(crystals)})')
                    continue
            else:
                # If aggregation occurs, select a random crystal to aggregate with
                aggregated_crystal_index = int(random() * num_crystals_downstream) + released_crystal_index
                crystals[aggregated_crystal_index].volume += released_crystal.volume
                crystals[aggregated_crystal_index].aggregation_occurred = True

                if include_prints:
                    print(f'Aggregation occurred at time {curr_time:.3e} at the location '
                          f'{crystals[aggregated_crystal_index].location:.4f} (Total crystals left = {len(crystals)})')

        if include_prints:
            print('Took max time!!')
        return curr_time


class _ReleaseEvent:
    def __init__(self, time: float, crystal: Crystal):
        self.time: float = time
        self.crystal: Crystal = crystal

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return f'ReleaseEvent({self.time})'


class _Event:
    NUCLEATION, RELEASE = 0, 1

    def __init__(self, time: float, event_type: int, crystal: Crystal | None = None):
        self.time = time
        self.event_type = event_type
        self.crystal = crystal

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        if self.event_type == _Event.NUCLEATION:
            return f'Nucleation Event at time {self.time}'
        else:
            return f'Release Event at time {self.time}'

    def __str__(self):
        return self.__repr__()
