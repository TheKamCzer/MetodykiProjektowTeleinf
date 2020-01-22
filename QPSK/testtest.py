"""
Implementation of QAM modulation.

"""
from QPSK import Modulator
import numpy as np
import commpy as cp
from scipy import signal
import matplotlib.pyplot as plt
from typing import List, Dict

import sys
sys.path.insert(
    0, '/home/pwozny/sync/projects/agh/cps/MetodykiProjektowTeleinf/QPSK/')


class ModulatorQAM(Modulator.Modulator):

    def __init__(self, upsamplingFactor, carrierFreq,  sampleRate, symbolLength, debug=False):
        """
            sampleRate - sample rate of output stream (eg. PLUTO) 
        """

        super().__init__(carrierFreq, symbolLength, sampleRate)

        self.debug = debug

        self._MAPPING_TABLE_QAM16 = {
            # TODO: check corectness of the table
            (0, 0, 0, 0): -3-3j,
            (0, 0, 0, 1): -3-1j,
            (0, 0, 1, 0): -3+3j,
            (0, 0, 1, 1): -3+1j,
            (0, 1, 0, 0): -1-3j,
            (0, 1, 0, 1): -1-1j,
            (0, 1, 1, 0): -1+3j,
            (0, 1, 1, 1): -1+1j,
            (1, 0, 0, 0):  3-3j,
            (1, 0, 0, 1):  3-1j,
            (1, 0, 1, 0):  3+3j,
            (1, 0, 1, 1):  3+1j,
            (1, 1, 0, 0):  1-3j,
            (1, 1, 0, 1):  1-1j,
            (1, 1, 1, 0):  1+3j,
            (1, 1, 1, 1):  1+1j
        }

    def modulateQAM(self, bitsToModulate):
        """
        takes bit array of bits to modulate and
        returns complex modulated signal.
        Can be called multiple times because it keeps track
        of the timebase
        """

        print("Modulating QAM16")

        # gruping data into chunks of 4
        bitsGroupped = np.array(bitsToModulate).reshape(
            (int(self.symbolLength/4), 4))

        # using dictionary to convert input data array to symbols
        symbolsQAM16 = np.array(
            [self._MAPPING_TABLE_QAM16[tuple(b)] for b in bitsGroupped])

        N = int(len(bitsToModulate) / 2)
        signalI = signal.upfirdn([1], np.real(symbolsQAM16), self.symbolLength)
        signalQ = signal.upfirdn([1], np.imag(symbolsQAM16), self.symbolLength)

        filteredI = np.convolve(signalI, self.psfFilter)
        signalI = filteredI[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]
        filteredQ = np.convolve(signalQ, self.psfFilter)
        signalQ = filteredQ[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]

        t = np.arange(0, N * self.symbolLength *
                      self.sampleTime, self.sampleTime)

        if self.debug == True:
            fig0, axs0 = plt.subplots(2, 2, constrained_layout=True)
            fig0.suptitle('Symbols', fontsize=16)
            axs0[0][0].plot(signalI)
            axs0[0][0].set_title('I - before filtration')
            axs0[0][0].set_xlabel('sample')
            axs0[0][0].set_ylabel('value')
            axs0[0][1].plot(signalQ)
            axs0[0][1].set_title('Q - before filtration')
            axs0[0][1].set_xlabel('sample')
            axs0[0][1].set_ylabel('value')
            axs0[1][0].plot(signalIFilt)
            axs0[1][0].set_title('I - after filtration')
            axs0[1][0].set_xlabel('sample')
            axs0[1][0].set_ylabel('value')
            axs0[1][1].plot(signalQFilt)
            axs0[1][1].set_title('Q - after filtration')
            axs0[1][1].set_xlabel('sample')
            axs0[1][1].set_ylabel('value')
            plt.show()

        return np.multiply(signalI, np.cos(2 * np.pi * self.carrierFreq * t)) - 1j * np.multiply(signalQ, np.sin(2 * np.pi * self.carrierFreq * t))
