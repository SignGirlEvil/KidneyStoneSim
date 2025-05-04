import math
from crystals.constants import ONE_THIRD


def volume_from_radius(rad: float) -> float:
    # Kind of insane to import one third instead of just dividing by three, but I never
    # claimed to be sane. If you're reading this, I tip my hat to you. Are you another
    # senior design group? A research group perhaps? I would love to get updated on
    # this project if it is continued somehow! Contact me at aidantoad@gmail.com
    return 4 * ONE_THIRD * math.pi * (rad ** 3)


def radius_from_volume(vol: float) -> float:
    return (vol / (4 * ONE_THIRD * math.pi)) ** ONE_THIRD
