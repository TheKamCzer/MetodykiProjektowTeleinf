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

    def modulateQAM16(self, bitsToModulate, isSignalUpconverted=False, debug=False):
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

        # upconvert signals
        signalI = signal.upfirdn(
            [1]*self.upsamplingFactor, np.real(symbolsQAM16), self.upsamplingFactor)
        signalQ = signal.upfirdn(
            [1]*self.upsamplingFactor, np.imag(symbolsQAM16), self.upsamplingFactor)

        # apply raised cosine shaped filter
        # scalingFactor = sum(np.abs(self.psfFilter))
        filteredI = np.convolve(signalI, self.psfFilter)  # /scalingFactor
        filteredQ = np.convolve(signalQ, self.psfFilter)  # /scalingFactor
        # removing initial and last samples that where introduced by convolution
        signalIFilt = filteredI[int(
            self.upsamplingFactor * 5): - int(self.upsamplingFactor * 5) + 1]
        signalQFilt = filteredQ[int(
            self.upsamplingFactor * 5): - int(self.upsamplingFactor * 5) + 1]

        if debug == True:
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

        if isSignalUpconverted==True:
            pass
        else:
            pass

        print("a")
        #  =
