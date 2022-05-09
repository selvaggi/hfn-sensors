import math
import numpy as np
import matplotlib.pyplot as plt
from param import *

## charge to fC conversion
qe2fc = 1.60217646e-4
energy_per_ehpair = 3.6  ## in eV in Silicon

"""
charge deposited in silicon per um (in eV/um)
these are MPV per micron
the thinner the sensor, the smaller the MPV (per um!)
"""

eV_per_um = {80: 230, 100: 235, 120: 241, 160: 250, 200: 252, 300: 263, 320: 265}

# _______________________________________________________________________________
""" sensor class for easier manipulation """


class Sensor:
    def __init__(self, type, d, A, cce_param, ileak_param):
        self.d = d  # sensor depth in um
        self.A = A  # sensor area in cm2
        self.vol = (self.d * 1.0e-04) * self.A  # in cm3
        self.cce_param = cce_param
        self.ileak_param = ileak_param
        self.type = type
        self.label = "{} {} $\mu$m".format(self.type, self.d)
        self.nehpairs_per_um = (
            eV_per_um[self.d] / energy_per_ehpair
        )  # electron-hole pairs per eV deposited

    """ compute leakage current (uA) as function of fluence """

    def get_ileak(self, fluence):
        volume = self.vol
        unitToMicro = 1.0e6
        unitToMicroLog = np.log(unitToMicro)
        conv = np.log(volume) + unitToMicroLog
        ileak = np.exp(ileakParam[0] * np.log(fluence) + ileakParam[1] + conv)
        return ileak

    """ compute capacitance, for now independent on fluence """

    def get_capacitance(self, fluence):
        # recompute capacitance based on 120 um reference for epi and 200 um for std

        ones = np.copy(fluence)
        ones.fill(1)  ## constnace vs F for now
        cap = np.where(
            self.type == "epi",
            50 * (self.A / 0.5) * (120.0 / self.d) * ones,
            65 * (self.A / 1.0) * (200.0 / self.d) * ones,
        )
        return cap

    """ ileak in uA, returns equivalent noise in fC"""

    def get_encs_cmssw(self, ileak):
        def conditions(ileak):
            if ileak > 45.40:
                return 23.30 * ileak + 1410.04
            elif ileak > 38.95:
                return 30.07 * ileak + 1156.76
            elif ileak > 32.50:
                return 38.58 * ileak + 897.94
            elif ileak > 26.01:
                return 193.67 * ileak ** 0.70 + 21.12
            elif ileak > 19.59:
                return 167.60 * ileak ** 0.77
            elif ileak > 13.06:
                return 162.35 * ileak ** 0.82
            elif ileak > 6.53:
                return 202.73 * ileak ** 0.81
            else:
                return 457.15 * ileak ** 0.57

        func = np.vectorize(conditions)
        return func(ileak) * qe2fc

    """ ileak in uA, returns equivalent noise in fC"""

    def get_encs_an(self, ileak):
        return 870 * np.sqrt(ileak) * qe2fc

    """ s in fC and capac in pF
     compute s in ADC counts
    need to compute first least significant bit for each gain scenario (320 fC, 160fC, 80 fC)
    assuming 10 bits.
    """

    def get_s_adc(self, s):
        def conditions(s):
            best_gain = 320.0
            best_lsb = best_gain / 1024.0
            best_s = s / best_lsb
            for gain, params in gain_parameters.items():
                lsb = gain / 1024.0  ## fC to ADC conversion (assumes 10-bit)
                s_in_adc_counts = s / lsb
                # print (s, lsb, s_in_adc_counts)
                if s_in_adc_counts > 16.0:
                    break
                best_s = s_in_adc_counts
            return best_s

        func = np.vectorize(conditions)
        return func(s)

    """ s in fC and capac in pF, returns equivalent noise in fC
     compute s in ADC counts
    need to compute first least significant bit for each gain scenario (320 fC, 160fC, 80 fC)
    assuming 10 bits.
    """

    def get_encp(self, s, c):
        def conditions(s):
            best_gain = 320.0
            for gain, params in gain_parameters.items():
                lsb = gain / 1024.0  ## fC to ADC conversion (assumes 10-bit)
                s_in_adc_counts = s / lsb
                # print (s, lsb, s_in_adc_counts)
                if s_in_adc_counts > 16.0:
                    break
                best_gain = gain
            return best_gain
            # print(best_gain)

        func = np.vectorize(conditions)
        gain = func(s)
        params = np.vectorize(gain_parameters.get)(gain)

        return (params[0] + params[1] * c + params[2] * c ** 2) * qe2fc

    """ depth in um, return Signal MPV in fC"""

    def get_s(self, cce):
        return cce * self.d * self.nehpairs_per_um * qe2fc

    """ returns equivalent Noise in fC"""

    def get_encn(self, encs, ensp):
        return np.sqrt(encs ** 2 + ensp ** 2)

    """ returns equivalent Noise in fC"""

    def get_sn(self, s, encn):
        return s / encn

    """ compute charge collection efficiency as function of fluence """

    def get_cce_cmssw(self, x, a, b, c):
        cce = np.where(
            x < a, 1 + [b] * x, (1 - c * np.log(x)) + (b * a + c * np.log(a))
        )
        cce = np.where(cce < 0, 0.0, cce)
        cce = np.where(cce > 1, 1.0, cce)
        return cce
