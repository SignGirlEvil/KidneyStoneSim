from crystals import Kidney
from crystals.constants import *
from utils.distributions import sample_beta_dist
import matplotlib.pyplot as plt
import statistics


# molar_mass in g / mol
def mmol_per_liter_to_mg_per_100_ml(mmol_per_liter: float, molar_mass: float) -> float:
    mol_per_liter = mmol_per_liter / 1000.0
    mol_per_100_ml = mol_per_liter / 10.0
    grams_per_100_ml = mol_per_100_ml * molar_mass
    mg_per_100_ml = grams_per_100_ml * 1000.0

    return mg_per_100_ml


def get_bloods(num_patients: int) -> list[float]:
    percent_stone_formers = 0.1

    # SS overrides from: https://www.kidney-international.org/article/S0085-2538(15)46052-1/pdf
    # caox_rs_healthy_mean = 5.3
    # caox_rs_healthy_stdev = 1.7
    caox_rs_healthy_low = 2.6
    caox_rs_healthy_high = 8.6
    caox_rs_healthy_alpha = 1.388
    caox_rs_healthy_beta = 1.696

    # caox_rs_stone_former_mean = 5.7
    # caox_rs_stone_former_stdev = 3.1
    caox_rs_stone_former_low = 1.01
    caox_rs_stone_former_high = 14.2
    caox_rs_stone_former_alpha = 1.476
    caox_rs_stone_former_beta = 2.674

    patient_bloods = []
    for i in range(num_patients):
        percent = float(i) / float(num_patients)
        if percent < percent_stone_formers:
            caox_ss = sample_beta_dist(caox_rs_stone_former_alpha, caox_rs_stone_former_beta,
                                       caox_rs_stone_former_low, caox_rs_stone_former_high) + 1
        else:
            caox_ss = sample_beta_dist(caox_rs_healthy_alpha, caox_rs_healthy_beta,
                                       caox_rs_healthy_low, caox_rs_healthy_high) + 1

        patient_bloods.append(caox_ss)

    return patient_bloods


def main():
    num_patients = 50000
    patient_bloods = get_bloods(num_patients)

    stone_former_ss_dist = [supersaturation for supersaturation in patient_bloods[:int(num_patients/10)]]
    caox_ss_dist = [supersaturation for supersaturation in patient_bloods]

    all_stone_times: list[float] = []
    usable_stone_times: list[float] = []
    usable_stone_caox_ss: list[float] = []
    kidney: Kidney = Kidney(patient_bloods[0])

    for i, supersaturation in enumerate(patient_bloods):
        print(f'i: {i}, SS: {supersaturation:.2f}', end=', ')
        kidney.supersaturation = supersaturation
        next_time = kidney.determine_time_until_stone(max_crystals=100, include_prints=False,
                                                      max_time=10*SECONDS_PER_YEAR) / SECONDS_PER_YEAR

        print(next_time)
        all_stone_times.append(next_time)

        if next_time <= 5:
            usable_stone_times.append(next_time)
            usable_stone_caox_ss.append(supersaturation)

        # print(f'Appended: {all_stone_times[-1]} Years')

    print(f'Stone Prevalence: {100 * len(usable_stone_caox_ss) / num_patients:.2f}%')

    if not usable_stone_caox_ss:
        return

    print(f'Mean CaOx SS of Predicted Stone Formers: {statistics.mean(usable_stone_caox_ss)}')
    print(f'Standard Deviation CaOx SS of Predicted Stone Formers: {statistics.stdev(usable_stone_caox_ss)}')
    print(f'Mean Stone Form Time: {statistics.mean(usable_stone_times):.3f} years')
    print(f'St Dev of CaOx SS of Artificial Stone Formers: {statistics.stdev(caox_ss_dist[:num_patients//10])}')

    fig, axs = plt.subplots(2, 3)

    axs[0, 0].hist(caox_ss_dist, bins=75)
    axs[0, 0].set_xlabel('CaOx SS')
    axs[0, 0].set_ylabel('Number of Patients')
    axs[0, 0].set_title(f'Distribution of CaOx SS\nin Artificial Patients (n = {num_patients})')

    axs[0, 1].hist(all_stone_times, bins=150)
    axs[0, 1].set_xlabel('Years for Stone to Develop')
    axs[0, 1].set_ylabel('Number of Patients')
    axs[0, 1].set_title(f'Distribution of Stone Development Time\nin Artificial Patients (n = {num_patients})')

    axs[1, 2].hist(usable_stone_caox_ss, bins=75)
    axs[1, 2].set_xlabel('CaOx SS')
    axs[1, 2].set_ylabel('Number of Patients')
    axs[1, 2].set_title(f'Distribution of CaOx SS\nin Artificial Stone Formers '
                        f' (n = {len(usable_stone_caox_ss)})')

    axs[1, 1].hist(usable_stone_times, bins=150)
    axs[1, 1].set_xlabel('Years for Stone to Develop')
    axs[1, 1].set_ylabel('Number of Patients')
    axs[1, 1].set_title(f'Distribution of Stone Development Time\nin Artificial Stone Formers'
                        f' (n = {len(usable_stone_times)})')

    axs[0, 2].hist(stone_former_ss_dist, bins=75)
    axs[0, 2].set_xlabel('CaOx SS')
    axs[0, 2].set_ylabel('Number of Patients')
    axs[0, 2].set_title(f'Distribution of CaOx SS\nin Real-World Stone Formers '
                        f' (n = {len(stone_former_ss_dist)})')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
