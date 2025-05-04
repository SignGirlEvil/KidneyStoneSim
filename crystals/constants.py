# File: constants.py

# Important ones for testing:
# CAOX_CONTACT_ANGLE
# NUCLEATION_ARRHENIUS_CONST
# GROWTH_ARRHENIUS_CONST

CUBIC_METERS_PER_CUBIC_CM = 1e-6
CUBIC_METERS_PER_100_ML = 1e-4
GRAMS_PER_MILLIGRAM = 1e-3
SECONDS_PER_YEAR = 60 * 60 * 24 * 365.25

ONE_THIRD = 1.0 / 3.0
PI = 3.141592653589793

AVOGADRO = 6.0221415e23  # mol^-1
BOLTZMANN = 1.3806503e-23  # m^2 * kg * s^-2 * K^-1

CALCIUM_MOLAR_MASS = 40.0789  # g / mol
CITRATE_MOLAR_MASS = 210.14  # g / mol
OXALATE_MOLAR_MASS = 88.018  # g / mol
CAOX_MOLAR_MASS = CALCIUM_MOLAR_MASS + OXALATE_MOLAR_MASS  # g / mol (128.0969)

CAOX_DENSITY = 2.20  # g / cm^3
CAOX_MOLECULE_VOL = CAOX_MOLAR_MASS / AVOGADRO / CAOX_DENSITY * CUBIC_METERS_PER_CUBIC_CM  # m^3 (9.668630940731572e-29)
CAOX_MOLECULE_RADIUS = (0.75 * CAOX_MOLECULE_VOL / PI) ** ONE_THIRD  # m (2.8472490581461027e-10)
CAOX_SOLUBILITY = 0.61  # mg / 100g H2O

KIDNEY_TEMP = 310.0  # Kelvin
THERMAL_ENERGY = KIDNEY_TEMP * BOLTZMANN

PLASMA_VOL_FLOW = 1e-5  # m^3 / s
PROBLEM_RADIUS = 1e-3  # m (The minimum radius stones must be to cause problems)

# After writing the report we actually found and fixed some small bugs in the code, but that
# means these constants are no longer the "ideal" ones. And I don't want to spend any more time
# tuning this mess. I'm sorry. I'm just too burnt out. I want to graduate and get outta here.
# I'm so tired. That said, I am pretty proud of what we have been able to put together. Considering
# we are a group of mechanical engineers way out of our depth, this is...certainly something.
# If someone out there is reading this, and is actually looking to do something with this,
# please try to contact the owner of this github repo! I'd love to chat
CAOX_CONTACT_ANGLE = 75.9336  # degrees
CAOX_SURFACE_ENERGY = 0.0057052  # J / m^2  (water surface energy)
NUCLEATION_ARRHENIUS_CONST = 7.82292e-10
GROWTH_ARRHENIUS_CONST = 3.18542e+03


