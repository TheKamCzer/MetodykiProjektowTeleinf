import numpy as np
import commpy as cp

class Demodulator:
    def __init__(self, carrierFreq, symbolLength, fi, sampleRate, numOfPeriods):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.sampleRate = sampleRate
        self.numOfPeriods = numOfPeriods
        _, self.psfFilter = cp.rrcosfilter(int(self.symbolLength / 2 - 1), 0.35, self.symbolLength * self.sampleRate, self.sampleRate)

    def filter(self, inSig):
        filtered = np.convolve(inSig, self.psfFilter)
        filtered = filtered[int((self.symbolLength / 2 - 1) / 2): - int((self.symbolLength / 2 - 1) / 2)]
        return filtered

    def demodulate(self, inputSignal):
        sigLen = int(len(inputSignal))
        t = np.linspace(0, self.numOfPeriods * sigLen / self.carrierFreq / self.symbolLength, sigLen)
        phase = 2 * np.pi * self.carrierFreq * t + self.fi
        branchQ = np.imag(inputSignal) * -np.sin(phase)
        branchI = np.real(inputSignal) * np.cos(phase)
        result = []
        for i in range(int(len(inputSignal) / self.symbolLength)):
            signalQ = self.filter(branchQ[i * self.symbolLength : (i + 1) * self.symbolLength])
            signalI = self.filter(branchI[i * self.symbolLength : (i + 1) * self.symbolLength])
            result.append(0 if np.mean(signalI) <= 0 else 1)
            result.append(0 if np.mean(signalQ) <= 0 else 1)
        return result
