import matplotlib.pyplot as plt
import numpy as np
from crystals import RenalPapilla, Crystal
from crystals.constants import *


def main():
    caox_ss = np.linspace(2, 12, 500)

    get_nuc_rate = np.vectorize(
        lambda ss: RenalPapilla.calculate_nucleation_rate(ss, CAOX_CONTACT_ANGLE, NUCLEATION_ARRHENIUS_CONST,
                                                          CAOX_SURFACE_ENERGY)
    )

    get_grow_const = np.vectorize(
        lambda ss: Crystal.calculate_growth_constant(ss, CAOX_SURFACE_ENERGY, GROWTH_ARRHENIUS_CONST)
    )

    get_max_life = np.vectorize(
        lambda ss: Crystal.calculate_max_lifespan(
            growth_constant=Crystal.calculate_growth_constant(ss, CAOX_SURFACE_ENERGY, GROWTH_ARRHENIUS_CONST),
            max_volume=4 * ONE_THIRD * PI * ((RenalPapilla.RENAL_PAP_DIAM / 2.0) ** 3)
        )
    )

    nuc_rates = get_nuc_rate(caox_ss)
    grow_consts = get_grow_const(caox_ss)
    max_lives = get_max_life(caox_ss)

    fig, (ax_nuc_lin, ax_grow_lin, max_life_lin) = plt.subplots(1, 3)

    ax_nuc_lin.plot(caox_ss, nuc_rates)
    ax_nuc_lin.set_title('Nucleation Rate vs CaOx SS')
    ax_nuc_lin.set_xlabel('CaOx SS')
    ax_nuc_lin.set_ylabel('Nucleation Rate (s^-1)')
    ax_nuc_lin.grid()

    ax_grow_lin.plot(caox_ss, grow_consts)
    ax_grow_lin.set_title('Growth Rate vs CaOx SS')
    ax_grow_lin.set_xlabel('CaOx SS')
    ax_grow_lin.set_ylabel('Growth Rate (s^-1)')
    ax_grow_lin.grid()

    max_life_lin.plot(caox_ss, max_lives)
    max_life_lin.set_title('Maximum Lifespan vs CaOx SS')
    max_life_lin.set_xlabel('CaOx SS')
    max_life_lin.set_ylabel('Max Life (s)')
    max_life_lin.grid()

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
