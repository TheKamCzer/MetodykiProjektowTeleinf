import numpy as np


class TimingRecovery:
    def __init__(self, symbolLength):
        self.symbolLength = symbolLength
        self.damp = np.sqrt(2) / 2
        self.band = (0.5 * np.pi / 500) / (self.damp + 1 / (4 * self.damp))
        self.mi1 = (4 * self.damp * self.band) / (1 + 2 * self.damp * self.band + self.band * self.band)
        self.mi2 = (4 * self.band * self.band) / (1 + 2 * self.damp * self.band + self.band * self.band)

    def synchronizeTiming(self, inputData):
        I = np.real(inputData)
        Q = np.imag(inputData)

        toRemove = []
        toAdd = []
        adap1 = 0
        adap2 = 0
        offset = 0
        numOfWrongSamples = 0
        for i in range(0, int(len(inputData) - 2 * self.symbolLength), self.symbolLength):
            actualIdx = i + offset
            nextIdx = actualIdx + self.symbolLength

            iActual = I[actualIdx]
            iNext = I[nextIdx]
            qActual = Q[actualIdx]
            qNext = Q[nextIdx]

            err = -(iActual * np.sign(iNext) - iNext * np.sign(iActual) + qActual * np.sign(qNext) - qNext * np.sign(qActual))
            if adap1 > 1 : adap1 -= 1
            elif adap1 < -1 : adap1 += 1

            adap2 += self.mi2 * err
            adap1 += adap2 + self.mi1 * err
            offset = int(round(adap1 * self.symbolLength))

            if offset - numOfWrongSamples > 0 :
                numOfWrongSamples += 1
                toRemove.append(actualIdx)
            elif offset + numOfWrongSamples < 0 :
                numOfWrongSamples += 1
                toAdd.append(actualIdx)

        inputData = np.delete(inputData, toRemove)
        inputData = np.insert(inputData, toAdd, 0)
        return inputData
