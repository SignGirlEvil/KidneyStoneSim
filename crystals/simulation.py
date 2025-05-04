from crystals.constants import SECONDS_PER_YEAR
from crystals.kidney import Kidney
import matplotlib.pyplot as plt


def run_simulation(caox_supersat: float, num_iters: int = 1000):
    kidney = Kidney(caox_supersat)

    stone_times = []

    for i in range(num_iters):
        print(i)
        stone_times.append(kidney.determine_time_until_stone(max_crystals=1000) / SECONDS_PER_YEAR)

    fig, ax = plt.subplots()

    ax.set_title('Distribution of Times Until Kidney Stone Forms')
    ax.set_xlabel('Time Until Stone Forms (Years)')
    ax.set_ylabel('Observations')
    ax.hist(stone_times, bins=25)

    plt.show()
