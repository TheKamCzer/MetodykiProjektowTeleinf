import numpy as np
import commpy as cp


class Demodulator:
    def __init__(self, carrierFreq, symbolLength, fi, sampleRate, numOfPeriods):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.sampleRate = sampleRate
        self.numOfPeriods = numOfPeriods
        self.psfFilter = cp.rrcosfilter(int(self.symbolLength) * 10 , 0.35, self.symbolLength / self.sampleRate, self.sampleRate)[1]

    def demodulate(self, inputSignal):
        sigLen = int(len(inputSignal))
        t = np.linspace(0, self.numOfPeriods * sigLen / self.carrierFreq / self.symbolLength, sigLen)
        phase = 2 * np.pi * self.carrierFreq * t + self.fi

        branchI = np.convolve(np.real(inputSignal) * np.cos(phase), self.psfFilter)
        branchI = branchI[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]
        branchQ = np.convolve(np.imag(inputSignal) * -np.sin(phase), self.psfFilter)
        branchQ = branchQ[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]

        bitsI = [1 if x > 0 else 0 for x in branchI[0::self.symbolLength]]
        bitsQ = [1 if x > 0 else 0 for x in branchQ[0::self.symbolLength]]
        return [item for sublist in zip(bitsI, bitsQ) for item in sublist]
