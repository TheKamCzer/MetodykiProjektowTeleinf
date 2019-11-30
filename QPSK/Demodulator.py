import numpy
from scipy import signal


class Demodulator:
    def __init__(self, carrierFreq, symbolLength, fi, sampleRate, numOfPeriods):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.sampleRate = sampleRate
        self.numOfPeriods = numOfPeriods
        self.firFilter = signal.firwin(int(self.symbolLength / 2) - 1 , self.carrierFreq / self.sampleRate)
        self.filterDelay = signal.lfilter_zi( self.firFilter, 1)

    def demodulate(self, inputSignal):
        sigLen = int(len(inputSignal))
        t = numpy.linspace(0, self.numOfPeriods * sigLen / self.carrierFreq / self.symbolLength, sigLen)
        phase = 2 * numpy.pi * self.carrierFreq * t + self.fi
        branchQ = inputSignal * numpy.sin(phase)
        branchI = inputSignal * numpy.cos(phase)
        result = []
        for i in range(int(len(inputSignal) / self.symbolLength)):
            signalQ, _ = signal.lfilter(self.firFilter, 1, branchQ[i * self.symbolLength : (i + 1) * self.symbolLength], zi=self.filterDelay)
            signalI, _ = signal.lfilter(self.firFilter, 1, branchI[i * self.symbolLength : (i + 1) * self.symbolLength], zi=self.filterDelay)

            result.append(0 if numpy.mean(signalI) <= 0 else 1)
            result.append(0 if numpy.mean(signalQ) <= 0 else 1)
        return result
