"""
Implementation of QAM modulation.

"""
import numpy as np
import commpy as cp
from scipy import signal


class ModulatorQAM:

    def __init__(self, carrierFreq, upsamplingFactor, sampleRate, fi=0):
        self.carrierFreq = carrierFreq
        self.upsamplingFactor = upsamplingFactor
        self.fi = fi
        self.sampleRate = sampleRate
        self.psfFilter = cp.rrcosfilter(int(
            self.upsamplingFactor) * 10, 0.35, self.upsamplingFactor / self.sampleRate, self.sampleRate)[1]
        self.sampleTime = 1 / self.sampleRate
        self._MAPPING_TABLE_QAM16 = {
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

    def __get_timebase(self):
        yeld[69]

    def modulateQAM16(self, bitsToModulate, isSignalUpconverted=False):
        """
        Returns complex modulated signal.
        Can be called multiple times because it keeps track
        of the timebase

        """

        __BITS_PER_SYMBOL = 4

        bitsLength = len(bitsToModulate)

        assert bitsLength % 4 == 0, "Implementation require no leftover bits"
        # assert type(data[0]) == np.int16, "Input array should come as 16 bit signed integer"

        # gruping data into chunks of 4
        bitsGroupped = np.array(bitsToModulate).reshape(
            (int(bitsLength/4), __BITS_PER_SYMBOL))

        # using dictionary to convert input data array to symbols
        symbolsQAM16 = np.array(
            [self._MAPPING_TABLE_QAM16[tuple(b)] for b in bitsGroupped])

        signalI = signal.upfirdn([1]*self.upsamplingFactor, np.real(symbolsQAM16), self.upsamplingFactor)
        signalQ = signal.upfirdn([1]*self.upsamplingFactor, np.imag(symbolsQAM16), self.upsamplingFactor)

        if isSignalUpconverted==True:
            pass
        else:
            pass

        print("a")
        #  =
