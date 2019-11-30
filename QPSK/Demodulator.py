import numpy
from scipy import signal


class Demodulator:
    def __init__(self, carrierFreq, symbolLength, fi, sampleRate, numOfPeriods):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.sampleRate = sampleRate
        self.numOfPeriods = numOfPeriods

    def demodulate(self, inputSignal):
        sigLen = int(len(inputSignal))
        t = numpy.linspace(0, self.numOfPeriods * sigLen / self.carrierFreq / self.symbolLength, sigLen)
        fi = 2 * numpy.pi * self.carrierFreq * t + self.fi
        branchQ = inputSignal * numpy.sin(fi)
        branchI = inputSignal * numpy.cos(fi)
        firFilter = signal.firwin(int(self.symbolLength / 2) - 1 , self.carrierFreq / self.sampleRate, pass_zero=True)
        filterDelay = signal.lfilter_zi(firFilter, 1)
        result = []
        for i in range(int(len(inputSignal) / self.symbolLength)):
            signalQ, _ = signal.lfilter(firFilter, 1, branchQ[i * self.symbolLength : (i + 1) * self.symbolLength], zi=filterDelay)
            signalI, _ = signal.lfilter(firFilter, 1, branchI[i * self.symbolLength : (i + 1) * self.symbolLength], zi=filterDelay)

            bitQ = 1
            bitI = 1

            if numpy.mean(signalI) <= 0:
                bitI = -1

            if numpy.mean(signalQ) <= 0:
                bitQ = -1
            result.append(bitI)
            result.append(bitQ)
        return result
