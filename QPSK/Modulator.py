import numpy


def createSignalI(bit, carrierFreq, fi, time):
    return bit * numpy.cos(2 * numpy.pi * carrierFreq * time + fi)


def createSignalQ(bit, carrierFreq, fi, time):
    return -1j * bit * numpy.sin(2 * numpy.pi * carrierFreq * time + fi)


class Modulator:

    def __init__(self, carrierFreq, symbolLength, fi, numOfPeriods):
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.fi = fi
        self.numOfPeriods = numOfPeriods

    def modulate(self, bitsToModulate):
        time = numpy.linspace(0, self.numOfPeriods/self.carrierFreq, self.symbolLength)
        result = []
        for i in range(0, len(bitsToModulate), 2):
            signalI = createSignalI(bitsToModulate[i], self.carrierFreq, self.fi, time)
            signalQ = createSignalQ(bitsToModulate[i+1], self.carrierFreq, self.fi, time)
            result.extend(signalI + signalQ)
        return result
