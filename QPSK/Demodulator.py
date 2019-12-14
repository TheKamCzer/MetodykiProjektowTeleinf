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

    def filter(self, inSig):
        filtered = np.convolve(inSig, self.psfFilter)
        filtered = filtered[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]
        return filtered

    def demodulate(self, inputSignal):
        sigLen = int(len(inputSignal))
        t = np.linspace(0, self.numOfPeriods * sigLen / self.carrierFreq / self.symbolLength, sigLen)
        phase = 2 * np.pi * self.carrierFreq * t + self.fi
        branchQ = self.filter(np.imag(inputSignal) * -np.sin(phase))
        branchI = self.filter(np.real(inputSignal) * np.cos(phase))
        result = []
        for i in range(int(len(inputSignal) / self.symbolLength)):
            result.append(0 if branchI[i * self.symbolLength] <= 0 else 1)
            result.append(0 if branchQ[i * self.symbolLength] <= 0 else 1)
        return result
