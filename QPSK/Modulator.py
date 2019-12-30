import numpy as np
import commpy as cp
from scipy import signal


class Modulator:
    def __init__(self, carrierFreq, symbolLength, fi, sampleRate):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.sampleRate = sampleRate
        self.psfFilter = cp.rrcosfilter(int(self.symbolLength) * 10, 0.35, self.symbolLength / self.sampleRate, self.sampleRate)[1]
        self.sampleTime = 1 / self.sampleRate

    def modulate(self, bitsToModulate):
        bitsToModulate = [1 if x > 0 else -1 for x in bitsToModulate]
        N = int(len(bitsToModulate) / 2)
        signalI = signal.upfirdn([1]*self.symbolLength, bitsToModulate[0::2], self.symbolLength)
        signalQ = signal.upfirdn([1]*self.symbolLength, bitsToModulate[1::2], self.symbolLength)

        filteredI = np.convolve(signalI, self.psfFilter)
        signalI = filteredI[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]
        filteredQ = np.convolve(signalQ, self.psfFilter)
        signalQ = filteredQ[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]

        t = np.arange(0, N * self.symbolLength * self.sampleTime, self.sampleTime)
        return np.multiply(signalI, np.cos(2 * np.pi * self.carrierFreq * t + self.fi)) - 1j * np.multiply(signalQ, np.sin(2 * np.pi * self.carrierFreq * t + self.fi))
