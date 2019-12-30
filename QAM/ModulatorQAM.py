"""
Implementation of QAM modulation.

"""
import numpy as np
import commpy as cp
from scipy import signal
import matplotlib.pyplot as plt


class ModulatorQAM:

    def __init__(self, carrierFreq, upsamplingFactor, sampleRate, fi=0):
        self.carrierFreq = carrierFreq
        self.upsamplingFactor = upsamplingFactor
        self.fi = fi
        self.sampleRate = sampleRate
        self.psfFilter = cp.rrcosfilter(int(
            self.upsamplingFactor) * 10, 0.35, self.upsamplingFactor / self.sampleRate, self.sampleRate)[1]
        self.sampleTime = 1 / self.sampleRate
        self.currentTime = 0
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

    def __get_timebase(self, requiredLength: int):

        __BITS_PER_SYMBOL = 4
        t = np.arange(self.currentTime,
                      requiredLength*self.sampleTime,
                      self.sampleTime, )
        self.currentTime = t[-1]+self.sampleTime
        return t

    def modulateQAM16(self, bitsToModulate, isSignalUpconverted=True, debug=False):
        """
        Returns complex modulated signal.
        Can be called multiple times because it keeps track
        of the timebase

        """

        __BITS_PER_SYMBOL = 4
        # flatting array allows working with input data that comes directly
        # from pyAudio as well as made up in unitest 
        bitsToModulate = np.ndarray.flatten(bitsToModulate)

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

        if isSignalUpconverted == False:
            # return baseband signal. Used in communication with PLUTO without IF frequency
            return np.add(signalIFilt, 1j*signalQFilt, dtype=np.complex128)
        else:
            t = self.__get_timebase(len(signalI))
            modSig = np.add(np.multiply(signalIFilt, np.cos(2 * np.pi * self.carrierFreq * t + self.fi)),
                            1j * np.multiply(signalQFilt, np.sin(2 *
                                                                 np.pi * self.carrierFreq * t + self.fi)))
            if debug == True:
                fig1, axs1 = plt.subplots(2, 1, constrained_layout=True)
                fig1.suptitle('Upconverted symbols', fontsize=16)
                axs1[0].plot(np.real(modSig))
                axs1[0].set_title('I component')
                axs1[0].set_xlabel('sample')
                axs1[0].set_ylabel('value')
                axs1[1].plot(np.imag(modSig))
                axs1[1].set_title('Q component')
                axs1[1].set_xlabel('sample')
                axs1[1].set_ylabel('value')
                plt.show()

            return modSig

        # print("a")
        #  =
