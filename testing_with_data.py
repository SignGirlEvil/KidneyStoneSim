from crystals import Kidney
from crystals.constants import *
from utils.distributions import sample_beta_dist
import matplotlib.pyplot as plt
import statistics
from random import random


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


def run_test(num_patients: int, contact_angle: float = CAOX_CONTACT_ANGLE, surface_energy: float = CAOX_SURFACE_ENERGY,
             nuc_arr: float = NUCLEATION_ARRHENIUS_CONST, grow_arr: float = GROWTH_ARRHENIUS_CONST,
             show_results: bool = True, include_prints: bool = False):
    patient_bloods = get_bloods(num_patients)

    stone_former_ss_dist = [supersaturation for supersaturation in patient_bloods[:int(num_patients / 10)]]
    caox_ss_dist = [supersaturation for supersaturation in patient_bloods]

    all_stone_times: list[float] = []
    usable_stone_times: list[float] = []
    usable_stone_caox_ss: list[float] = []
    kidney: Kidney = Kidney(patient_bloods[0], contact_angle, surface_energy, nuc_arr, grow_arr)

    for i, supersaturation in enumerate(patient_bloods):
        if include_prints:
            print(f'i: {i}, SS: {supersaturation:.2f}', end=', ')
        kidney.supersaturation = supersaturation
        next_time = kidney.determine_time_until_stone(max_crystals=100, include_prints=False,
                                                      max_time=10 * SECONDS_PER_YEAR) / SECONDS_PER_YEAR

        if include_prints:
            print(next_time)
        all_stone_times.append(next_time)

        if next_time <= 5:
            usable_stone_times.append(next_time)
            usable_stone_caox_ss.append(supersaturation)

    if len(usable_stone_caox_ss) < 2:
        return False

    if not show_results:
        return (statistics.mean(usable_stone_caox_ss), statistics.stdev(usable_stone_caox_ss),
                100 * len(usable_stone_caox_ss) / num_patients)

    print(f'Stone Prevalence: {100 * len(usable_stone_caox_ss) / num_patients:.2f}%')
    print(f'Mean CaOx SS of Predicted Stone Formers: {statistics.mean(usable_stone_caox_ss)}')
    print(f'Standard Deviation CaOx SS of Predicted Stone Formers: {statistics.stdev(usable_stone_caox_ss)}')
    print(f'Mean Stone Form Time: {statistics.mean(usable_stone_times):.3f} years')
    print(f'St Dev of CaOx SS of Artificial Stone Formers: {statistics.stdev(caox_ss_dist[:num_patients // 10])}')

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


def find_min_error_by_guessing(num_iters: int = 10):
    num_patients = 8000

    best_total_error = 1e50
    best_contact_angle = CAOX_CONTACT_ANGLE
    best_surface_energy = CAOX_SURFACE_ENERGY
    best_nuc_arr = NUCLEATION_ARRHENIUS_CONST
    best_grow_arr = GROWTH_ARRHENIUS_CONST
    best_mean = 0
    best_stdev = 0
    best_prev = 100

    def weighted_total_err(i_mean_err, i_stdev_err, i_prev_err):
        return (3 * i_mean_err) + (1 * i_stdev_err) + (2 * i_prev_err)

    for i in range(num_iters):
        contact_angle = best_contact_angle + ((4 * random() - 2) * (i > 0))
        surface_energy = best_surface_energy + ((0.002 * random() - 0.001) * (i > 0))
        nuc_arr = best_nuc_arr * (10 ** ((2 * random() - 1) * (i > 0)))
        grow_arr = best_grow_arr * (10 ** ((2 * random() - 1) * (i > 0)))

        print(f'Iter: {i}, Angle: {contact_angle:.4f}, Surf E: {surface_energy:.7f}, Nuc A: {nuc_arr:.5e}, '
              f'Grow A: {grow_arr:.5e}')

        results = run_test(num_patients, contact_angle, surface_energy, nuc_arr, grow_arr, show_results=False)

        if not results:
            print('0% prevalence')
            print('------------------------')
            continue

        mean, stdev, prev = results[0], results[1], results[2]

        mean_err = abs((mean - 6.7) / 6.7)
        stdev_err = abs((stdev - 3.1) / 3.1)
        prev_err = abs((prev - 10) / 10)
        total_err = weighted_total_err(mean_err, stdev_err, prev_err)

        print(f'Mean: {mean:.4f}, StDev: {stdev:.4f}, Prev: {prev:.4f}')
        print(f'Mean Err: {mean_err:.4f}, StDev Err: {stdev_err:.4f}, Prev Err: {prev_err:.4f}, '
              f'Weighted Total Err: {total_err:.4f}')

        if total_err < best_total_error:
            best_total_error = total_err
            best_contact_angle = contact_angle
            best_surface_energy = surface_energy
            best_nuc_arr = nuc_arr
            best_grow_arr = grow_arr
            best_mean = mean
            best_stdev = stdev
            best_prev = prev
            print('New best!')

        print('------------------------')

    print('Best:')
    print(f'Angle: {best_contact_angle}, Surf E: {best_surface_energy}, Nuc A: {best_nuc_arr}, Grow A: {best_grow_arr}')
    print(f'Mean: {best_mean:.4f}, StDev: {best_stdev:.4f}, Prev: {best_prev:.4f}')

    mean_err = abs((best_mean - 6.7) / 6.7)
    stdev_err = abs((best_stdev - 3.1) / 3.1)
    prev_err = abs((best_prev - 10) / 10)
    total_err = weighted_total_err(mean_err, stdev_err, prev_err)
    print(f'Mean Err: {mean_err:.4f}, StDev Err: {stdev_err:.4f}, Prev Err: {prev_err:.4f}, '
          f'Weighted Total Err: {total_err:.4f}')


if __name__ == '__main__':
    # Have this line uncommented for the robust test
    run_test(50000, show_results=True, include_prints=True)

    # Have this line uncommented for the quick test
    # run_test(1000)

    # Have this line uncommented for finding the optimal parameters
    # find_min_error_by_guessing(100)
