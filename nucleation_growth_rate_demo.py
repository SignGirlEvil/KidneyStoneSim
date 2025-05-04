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

    nuc_rates = get_nuc_rate(caox_ss)
    grow_consts = get_grow_const(caox_ss)

    fig, ((ax_nuc_lin, ax_grow_lin), (ax_nuc_log, ax_grow_log)) = plt.subplots(2, 2)

    ax_nuc_lin.plot(caox_ss, nuc_rates)
    ax_nuc_lin.set_title('Nucleation Rate vs CaOx SS\nLinear Scale')
    ax_nuc_lin.set_xlabel('CaOx SS')
    ax_nuc_lin.set_ylabel('Nucleation Rate (s^-1)')

    ax_grow_lin.plot(caox_ss, grow_consts)
    ax_grow_lin.set_title('Growth Rate vs CaOx SS\nLinear Scale')
    ax_grow_lin.set_xlabel('CaOx SS')
    ax_grow_lin.set_ylabel('Growth Rate (s^-1)')

    ax_nuc_log.plot(caox_ss, nuc_rates)
    ax_nuc_log.set_yscale('log')
    ax_nuc_log.set_title('Nucleation Rate vs CaOx SS\nLogarithmic Scale')
    ax_nuc_log.set_xlabel('CaOx SS')
    ax_nuc_log.set_ylabel('Nucleation Rate (s^-1)')

    ax_grow_log.plot(caox_ss, grow_consts)
    ax_grow_log.set_yscale('log')
    ax_grow_log.set_title('Growth Rate vs CaOx SS\nLogarithmic Scale')
    ax_grow_log.set_xlabel('CaOx SS')
    ax_grow_log.set_ylabel('Growth Rate (s^-1)')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
