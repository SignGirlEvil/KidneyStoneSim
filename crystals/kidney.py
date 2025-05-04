from .renalpapilla import RenalPapilla


class Kidney:
    def __init__(self, supersaturation: float):
        self.supersaturation = supersaturation
        self.num_papilla = 26

    def determine_time_until_stone(self, max_time: float = 1e50, max_crystals: int = 1000000,
                                   include_prints: bool = False) -> float:
        stone_times: list[float] = []
        papilla = RenalPapilla(self.supersaturation)

        for i in range(self.num_papilla):
            if include_prints:
                print(f'Iteration: {i}')

            stone_times.append(papilla.determine_time_until_stone(max_time, max_crystals, include_prints))

            if include_prints:
                print(f'Time: {stone_times[-1]:.3e} seconds\n')

        return min(stone_times)
