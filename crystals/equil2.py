# It's not pretty, but I formatted it weirdly to better match what the r code for the actual EQUIL2 algorithm looks
# like to make comparisons easier. I might go back and make it not have like one number per line later

import math
import warnings


def equil2(sodium_mEq_L,  # mEq/L
           potassium_mEq_L,  # mEq/L
           calcium_mg_dL,  # mg/dL
           magnesium_mg_dL,  # mg/dL
           ammonia_mEq_L,  # mEq/L
           chloride_mEq_L,  # mEq/L
           phosphate_mg_dL,  # mg/dL
           sulfate_mg_dL,  # mg/dL
           oxalate_mg_dL,  # mg/dL
           citrate_mg_dL,  # mg/dL
           pH,
           urate_mg_dL,  # mg/dL
           tolerance=0.0001,
           max_iterations=50
           ):
    stability_constant = (0,  # adding a zero to the front because R indexing starts at 1
        1730000000000,
        14900000,
        162,
        145.5,
        20750,
        2640000,
        55210,
        1247,
        278000,
        12.9,
        5.433,
        13.4,
        8.5,
        216,
        33.1,
        251.2,
        10,
        8.831001,
        13.4,
        12.6,
        143,
        3597000,
        685,
        31.3,
        229.6,
        2746,
        17.3,
        71.4,
        60000,
        505.2,
        12.5,
        3460000,
        1014,
        31.9,
        188.4,
        4020,
        4.75,
        5.93,
        69900,
        316.7,
        5,
        10,
        12.9,
        13,
        8.5,
        58800000,
        2440000000,
        4970000,
        171,
        7.05,
        562000,
        5500,
        794000000,
        23.1,
        380.19,
        19770000,
        1995000000,
        55.6,
        1940000,
        16600000000,
        0.00123,
        18.6,
        1.03,
        1897,
        946
    )

    idx_species = {
        'sodium': 1,  # input value
        'potassium': 2,  # input value
        'calcium': 3,  # input value
        'magnesium': 4,  # input value
        'ammonia': 5,  # input value
        'phosphate': 6,  # input value
        'sulfate': 7,  # input value
        'oxalate': 8,  # input value
        'citrate': 9,  # input value
        'pH': 24,  # input value
        'urate': 10,  # input value
        'PYRO': 11,
        'CO2': 31,

        'NAHPP': 50,
        'KHPO4': 51,
        'KSO4': 52,
        'KOX': 53,
        'KCIT': 54,
        'KPP': 55,
        'CAPO4': 56,
        'CAHPO4': 57,
        'caso4': 59,
        # 'pp': 11,
        'caox': 60,
        'pp': 12,

        'chloride': 91,  # input value
        'calcium_oxalate': 100,
        'brushite': 101,
        'hydroxyapatite': 102,
        'uric_acid': 104,
        'sodium_urate': 105,
        'ammonium_urate': 106
    }

    a: list[float] = [0] * (120 + 1)  # adding 1 since indexing starts at 1, and I don't want to change every index
    a[idx_species['sodium']] = sodium_mEq_L
    a[idx_species['potassium']] = potassium_mEq_L
    a[idx_species['calcium']] = calcium_mg_dL
    a[idx_species['magnesium']] = magnesium_mg_dL
    a[idx_species['ammonia']] = ammonia_mEq_L
    a[idx_species['chloride']] = chloride_mEq_L
    a[idx_species['phosphate']] = phosphate_mg_dL
    a[idx_species['sulfate']] = sulfate_mg_dL
    a[idx_species['oxalate']] = oxalate_mg_dL
    a[idx_species['citrate']] = citrate_mg_dL
    a[idx_species['pH']] = pH
    a[idx_species['urate']] = urate_mg_dL

    # Mass to molar concentration conversions
    a[1] = a[1] / 1000
    # 'K'
    a[2] = a[2] / 1000
    # 'CA'
    a[3] = a[3] / 4008
    # 'MG'
    a[4] = a[4] / 2431
    # 'PYRO'
    a[11] = a[11] / 2431
    # 'NH4'
    a[5] = a[5] / 1000
    # 'CL'
    a[91] = a[91] / 1000
    # 'CO2'
    a[31] = a[31] / 4401
    # 'P'
    a[6] = a[6] / 3097
    # 'S'
    a[7] = a[7] / 3206
    # 'CIT'
    a[9] = a[9] / 19212
    # 'OX'
    a[8] = a[8] / 8802
    # 'PH'
    # 'UR'
    a[10] = a[10] / 16800
    a[26] = 10 ** (-a[24])

    F1 = 0.7
    F2 = 0.3
    F3 = 0.1
    F4 = 0.02
    # O0 <- 0
    # O1 <- 0
    # O2 <- 0
    # O3 <- 0
    # O4 <- 0
    crystal_conc_prior = [0] * (5 + 1)

    for idx_current in range(1, 10 + 1):
        a[12 + idx_current] = 0.1 * a[idx_current]

    a[12] = 0.1 * a[11]
    a[23] = 0.01 * a[12]
    converged = False
    current_iteration = 0

    while (not converged) and (current_iteration < max_iterations):
        current_iteration = current_iteration + 1
        a[25] = 10 ** (-13.593 + a[24])
        a[27] = stability_constant[1] * a[26] * a[18] * F3 / F2
        a[28] = stability_constant[2] * a[26] * a[27] * F2 / F1
        a[29] = stability_constant[3] * a[26] * a[28] * F1
        a[30] = stability_constant[61] * a[31] * stability_constant[58]
        a[32] = a[30] / (a[26] * stability_constant[59] * F1)
        a[33] = a[32] * F1 / (a[26] * stability_constant[60] * F2)
        a[34] = stability_constant[62] * a[13] * a[33] * F2
        a[35] = stability_constant[63] * a[13] * a[34] * F1 * F1
        a[36] = stability_constant[64] * a[15] * a[33] * F2 * F2
        a[37] = stability_constant[65] * a[16] * a[33] * F2 * F2
        a[38] = stability_constant[4] * a[26] * a[19] * F2 / F1
        a[39] = stability_constant[5] * a[26] * a[20] * F2 / F1
        a[40] = stability_constant[6] * a[26] * a[21] * F3 / F2
        a[41] = stability_constant[7] * a[26] * a[40] * F2 / F1
        a[42] = stability_constant[8] * a[26] * a[41] * F1
        a[43] = stability_constant[9] * a[26] * a[22] * F1
        a[44] = stability_constant[10] * a[13] * a[27] * F2
        a[45] = stability_constant[11] * a[13] * a[19] * F2
        a[46] = stability_constant[12] * a[13] * a[20] * F2
        a[47] = stability_constant[13] * a[13] * a[21] * F3 * F1 / F2
        a[48] = stability_constant[14] * a[13] * a[12] * F1 * F4 / F3
        a[49] = stability_constant[16] * a[13] * a[48] * F1 * F3 / F2
        a[50] = stability_constant[15] * a[13] * a[23] * F1 * F3 / F2
        a[51] = stability_constant[17] * a[14] * a[27] * F2
        a[52] = stability_constant[18] * a[14] * a[19] * F2
        a[53] = stability_constant[19] * a[14] * a[20] * F2
        a[54] = stability_constant[20] * a[14] * a[21] * F3 * F1 / F2
        a[55] = stability_constant[21] * a[14] * a[12] * F1 * F4 / F3
        a[56] = stability_constant[22] * a[15] * a[18] * F3 * F2 / F1
        a[57] = stability_constant[23] * a[15] * a[27] * F2 * F2
        a[58] = stability_constant[24] * a[15] * a[28] * F2
        a[59] = stability_constant[25] * a[15] * a[19] * F2 * F2
        a[60] = stability_constant[26] * a[15] * a[20] * F2 * F2  # CaOx SS
        a[61] = stability_constant[28] * a[15] * a[60]
        a[62] = stability_constant[27] * a[60] * a[20]
        a[63] = stability_constant[29] * a[15] * a[21] * F3 * F2 / F1
        a[64] = stability_constant[30] * a[15] * a[40] * F2 * F2
        a[65] = stability_constant[31] * a[15] * a[41] * F2
        a[66] = stability_constant[32] * a[16] * a[18] * F3 * F2 / F1
        a[67] = stability_constant[33] * a[16] * a[27] * F2 * F2
        a[68] = stability_constant[34] * a[16] * a[28] * F2
        a[69] = stability_constant[35] * a[16] * a[19] * F2 * F2
        a[70] = stability_constant[36] * a[16] * a[20] * F2 * F2
        a[71] = stability_constant[37] * a[16] * a[70]
        a[72] = stability_constant[38] * a[70] * a[20]
        a[73] = stability_constant[39] * a[16] * a[21] * F3 * F2 / F1
        a[74] = stability_constant[40] * a[16] * a[40] * F2 * F2
        a[75] = stability_constant[41] * a[16] * a[41] * F2
        a[76] = stability_constant[42] * a[17] * a[27] * F2
        a[77] = stability_constant[43] * a[17] * a[19] * F2
        a[78] = stability_constant[44] * a[17] * a[20] * F2
        a[79] = stability_constant[45] * a[17] * a[21] * F3 * F1 / F2
        a[23] = stability_constant[47] * a[26] * a[12] * F4 / F3
        a[81] = stability_constant[48] * a[26] * a[23] * F3 / F2
        a[82] = stability_constant[49] * a[26] * a[81] * F2 / F1
        a[83] = stability_constant[50] * a[26] * a[82] * F1
        a[84] = stability_constant[51] * a[15] * a[12] * F4
        a[85] = stability_constant[52] * a[15] * a[23] * F2 * F3 / F1
        a[86] = stability_constant[53] * a[15] * a[25] * a[12] * F4 * F2 / F3
        a[87] = stability_constant[54] * a[15] * a[25] * F2 / F1
        a[88] = stability_constant[55] * a[16] * a[25] * F2 / F1
        a[89] = stability_constant[56] * a[16] * a[12] * F4
        a[90] = stability_constant[57] * a[16] * a[25] * a[12] * F2 * F4 / F3
        total: list = [0] * (12 + 1)  # Replaced 'NA_real_' with zero since they are all overwritten
        total[12] = a[13] + a[44] + a[45] + a[46] + a[47] + a[48] + 2 * a[49] + a[50] + a[34] + 2 * a[35]
        total[1] = a[14] + a[51] + a[52] + a[53] + a[54] + a[55]
        total[2] = a[17] + a[76] + a[77] + a[78] + a[79]
        total[3] = a[15] + a[56] + a[57] + a[58] + a[59] + a[60] + 2 * a[61] + a[63] + a[64] + a[62] + a[65] + a[36] + a[85] + a[84] + a[86] + a[87]
        total[4] = a[16] + a[66] + a[67] + a[68] + a[69] + a[70] + 2 * a[71] + a[73] + a[74] + a[75] + a[72] + a[37] + a[88] + a[89] + a[90]
        total[5] = a[18] + a[27] + a[28] + a[29] + a[44] + a[51] + a[56] + a[57] + a[58] + a[66] + a[67] + a[68] + a[76]
        total[6] = a[19] + a[38] + a[45] + a[52] + a[59] + a[69] + a[77]
        total[7] = a[20] + a[39] + a[60] + a[61] + a[70] + a[71] + a[46] + a[53] + a[78] + 2 * a[62] + 2 * a[72]
        total[8] = a[21] + a[40] + a[41] + a[42] + a[47] + a[54] + a[79] + a[63] + a[64] + a[65] + a[73] + a[74] + a[75]
        total[9] = a[12] + a[23] + a[81] + a[82] + a[83] + a[84] + a[85] + a[86] + a[89] + a[90] + a[48] + a[49] + a[50] + a[55]
        total[10] = a[22] + a[43]
        total[11] = a[33] + a[32] + a[30] + a[34] + a[35] + a[36] + a[37]
        # For I1 = O To 11
        # If T(I1) = 0 Then T(I1) <- 1E-20
        # Next I1
        total = [max(t, 1e-20) for t in total]  # pmax(total, 1e-20)
        a[13] = a[1] * a[13] / total[12]
        a[14] = a[2] * a[14] / total[1]
        a[15] = a[3] * a[15] / total[3]
        a[16] = a[4] * a[16] / total[4]
        a[17] = a[5] * a[17] / total[2]
        a[18] = a[6] * a[18] / total[5]
        a[19] = a[7] * a[19] / total[6]
        a[20] = a[8] * a[20] / total[7]
        a[21] = a[9] * a[21] / total[8]
        a[22] = a[10] * a[22] / total[10]
        a[12] = a[11] * a[12] / total[9]
        a[33] = a[31] * a[33] / total[11]
        S1 = (a[25] + a[26]) / F1 + a[13] + a[14] + a[17] + a[22] + a[91] + a[44] + a[45] + a[46] + a[34] + a[51] + a[52] + a[53] + a[76] + a[77]
        S1 = S1 + a[78] + a[56] + a[58] + a[63] + a[65] + a[85] + a[87] + a[28] + a[32] + a[38] + a[39] + a[41] + a[82] + a[66] + a[68] + a[73] + a[75] + a[88]
        S2 = 4 * (a[15] + a[16] + a[19] + a[20] + a[33] + a[47] + a[49] + a[54] + a[79] + a[84] + a[50] + a[89] + a[27] + a[40] + a[81] + a[61] + a[71] + a[62] + a[72])
        S3 = 9 * (a[18] + a[21] + a[48] + a[55] + a[23] + a[86] + a[90])
        S4 = 16 * a[12]
        S5 = (S1 + S2 + S3 + S4) / 2
        # If S5 > 1 Then S5 <- 1
        # If S5 < 0.000001 Then S5 <- 0.000001
        S5 = max(min(S5, 1), 0.000001)
        S6 = math.sqrt(S5)
        F1 = math.exp(-1.20218 * ((S6 / (1 + S6)) - 0.285 * S5))
        F2 = F1 ** 4
        F3 = F1 ** 9
        F4 = F1 ** 16
        # Check for convergence (lines 2050-2200 in original source)
        crystal_conc_current = (a[15], a[16], a[18], a[20], a[21])
        converged = not any(
            [(abs((curr - prior) / curr) > tolerance) for curr, prior in zip(crystal_conc_current, crystal_conc_prior)]
        )
        crystal_conc_prior = crystal_conc_current

    if current_iteration >= max_iterations:
        warnings.warn(f'{max_iterations} iterations without convergence, interpret results with caution')

    a[92] = current_iteration
    a[93] = S5
    a[94] = F1
    a[95] = F2
    a[96] = F3
    a[97] = F4

    ret_species = {
        'Sodium': a[1] * 1000,
        '[NAHPP]': a[50],
        'Potassium': a[2] * 1000,
        '[KHPO4]': a[51],
        'Calcium': a[3] * 4008,
        '[KSO4]': a[52],
        'Magnesium': a[4] * 2431,
        '[KOX]': a[53],
        'Ammonia': a[5] * 1000,
        '[KCIT]': a[54],
        'Chloride': a[91] * 1000,
        'Phosphate': a[6] * 3097,
        '[KPP]': a[55],
        'Sulfate': a[7] * 3206,
        '[CAPO4]': a[56],
        'Oxalate': a[8] * 8802,
        '[CAHPO4]': a[57],
        'Citrate': a[9] * 19212,
        '[CAH2P04]': a[58],
        'pH': a[24],
        'Urate': a[10] * 16800,
        '[CASO4]': a[59],
        'PP': a[11],
        '[CAOX]': a[60],
        '[PP]': a[12],
        '[CA2OX]': a[61],
        '[NA]': a[13],
        '[CAOX2]': a[62],
        '[K]': a[14],
        '[CACIT]': a[63],
        '[CA]': a[15],
        '[CAHCIT]': a[64],
        '[MG]': a[16],
        '[CAH2CIT]': a[65],
        '[NH4]': a[17],
        '[MGPO4]': a[66],
        '[PO4]': a[18],
        '[MGHPO4]': a[67],
        '[SO4]': a[19],
        '[MGH2PO4]': a[68],
        '[OX]': a[20],
        '[MGSO4]': a[69],
        '[CIT]': a[21],
        '[MGOX]': a[70],
        '[HU]': a[22],
        '[MG2OX]': a[71],
        '[HPP]': a[23],
        '[MGOX2]': a[72],
        'PH': a[24],
        '[MGCIT]': a[73],
        '(OH)': a[25],
        '[MGHCIT]': a[74],
        '(H)': a[26],
        '[MGH2CIT]': a[75],
        '[HPO4]': a[27],
        '[NH4HPO4]': a[76],
        '[H2PO4]': a[28],
        '[NH4SO4]': a[77],
        '[H3PO4]': a[29],
        '[NH4OX]': a[78],
        '[H2CO3]': a[30],
        '[NH4CIT]': a[79],
        'CO2': a[31],
        '[HCO3]': a[32],
        '[H2PP]': a[81],
        '[CO3]': a[33],
        '[H3PP]': a[82],
        '[NACO3]': a[34],
        '[H4PP]': a[83],
        '[NA2CO3]': a[35],
        '[CAPP]': a[84],
        '[CACO3]': a[36],
        '[CAHPP]': a[85],
        '[MGCO3]': a[37],
        '[CAOHPP]': a[86],
        '[HSO4]': a[38],
        '[CAOH]': a[87],
        '[HOX]': a[39],
        '[MGOH]': a[88],
        '[HCIT]': a[40],
        '[MGPP]': a[89],
        '[H2CIT]': a[41],
        '[MGOHPP]': a[90],
        '[H3CIT]': a[42],
        '[CL]': a[91],
        '[H2U]': a[43],
        '[NAHPO4]': a[44],
        'I.S.': a[93],
        '[NASO4]': a[45],
        'F1': a[94],
        '[NAOX]': a[46],
        'F2': a[95],
        '[NACIT]': a[47],
        'F3': a[96],
        '[NAPP]': a[48],
        'F4': a[97],
        '[NA2PP]': a[49],
        'Cycles': a[92]
    }

    # Print #1, Tab(20); 'SS', Tab(43); 'DG'
    supersat_calcium_oxalate = a[60] / 0.00000616
    supersat_brushite = a[15] * a[27] * F2 * F2 / 0.000000237
    X1 = F2 * a[15] * 1000
    X2 = F3 * a[18] * 10000000000
    supersat_hydroxyapatite = (X1 ** 5) * (X2 ** 3) * a[25] / 1.45E-14
    a[103] = F1 * F2 * F3 * a[16] * a[17] * a[18] / 0.000000000000115
    supersat_uric_acid = a[43] / 0.000261
    supersat_sodium_urate = F1 * F1 * a[22] * a[13] / 0.0000279
    supersat_ammonium_urate = F1 * F1 * a[22] * a[17] / 0.000036
    a[107] = F1 * F1 * a[22] * a[14] / 0.0000963

    dg_calcium_oxalate = 1.2935 * math.log(supersat_calcium_oxalate) if supersat_calcium_oxalate > 0 else 0
    dg_brushite = 1.2935 * math.log(supersat_brushite) if supersat_brushite > 0 else 0
    dg_hydroxyapatite = 0.28744 * math.log(supersat_hydroxyapatite) if supersat_hydroxyapatite > 0 else 0
    a[111] = 0.8623 * math.log(a[103]) if a[103] > 0 else 0
    dg_uric_acid = 2.587 * math.log(supersat_uric_acid) if supersat_uric_acid > 0 else 0
    dg_sodium_urate = 1.2935 * math.log(supersat_sodium_urate) if supersat_sodium_urate > 0 else 0
    dg_ammonium_urate = 1.2935 * math.log(supersat_ammonium_urate) if supersat_ammonium_urate > 0 else 0
    a[115] = 1.2935 * math.log(a[107]) if a[107] > 0 else 0

    # supersaturation and delta-Gibbs energy
    # ret_ss =
    # data.frame(
    #     species=c('Calcium Oxalate', 'Brushite', 'Hydroxyapatite',
    #               'Uric Acid', 'Sodium Urate', 'Ammonium Urate'),
    #     super_saturation=c(supersat_calcium_oxalate, supersat_brushite, supersat_hydroxyapatite,
    #                        supersat_uric_acid, supersat_sodium_urate, supersat_ammonium_urate),
    #     neg_delta_Gibbs=c(dg_calcium_oxalate, dg_brushite, dg_hydroxyapatite,
    #                       dg_uric_acid, dg_sodium_urate, dg_ammonium_urate)
    # )
    # ret_ss

    return_dict_keys = ('Calcium Oxalate', 'Brushite', 'Hydroxyapatite', 'Uric Acid', 'Sodium Urate', 'Ammonium Urate')
    ss_values = (supersat_calcium_oxalate, supersat_brushite, supersat_hydroxyapatite, supersat_uric_acid,
                 supersat_sodium_urate, supersat_ammonium_urate)
    neg_delta_Gibbs_values = (dg_calcium_oxalate, dg_brushite, dg_hydroxyapatite, dg_uric_acid, dg_sodium_urate,
                              dg_ammonium_urate)

    ss_dict = dict(zip(return_dict_keys, ss_values))
    neg_del_gibbs_dict = dict(zip(return_dict_keys, neg_delta_Gibbs_values))
    return ss_dict, neg_del_gibbs_dict


