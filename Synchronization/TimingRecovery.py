import numpy as np


class TimingRecovery:
    def __init__(self, symbolLength):
        self.symbolLength = symbolLength
        self.damp = np.sqrt(2) / 2
        self.band = (0.5 * np.pi / 500) / (self.damp + 1 / (4 * self.damp))
        self.mi1 = (4 * self.damp * self.band) / (1 + 2 * self.damp * self.band + self.band * self.band)
        self.mi2 = (4 * self.band * self.band) / (1 + 2 * self.damp * self.band + self.band * self.band)

    def __recoverTime(self, inputData):
        I = np.real(inputData)
        Q = np.imag(inputData)

        adap1 = 0
        adap2 = 0
        offset = 0
        toRemove = []
        toAdd = []
        f = 0
        for i in range(int(np.floor(len(inputData) / self.symbolLength) - 2)):
            actualIdx = i * self.symbolLength + offset
            nextIdx = actualIdx + self.symbolLength
            iActual = I[actualIdx]
            iNext = I[nextIdx]
            qActual = Q[actualIdx]
            qNext = Q[nextIdx]

            err = -(iActual * np.sign(iNext) - iNext * np.sign(iActual) + qActual * np.sign(qNext) - qNext * np.sign(qActual))
            if adap1 > 1 :
                adap1 -= 1
            elif adap1 < -1 :
                adap1 += 1

            adap2 += self.mi2 * err
            adap1 += adap2 + self.mi1 * err
            offset = int(round(adap1 * self.symbolLength))

            if offset - f > 0 :
                f += 1
                toRemove.append(actualIdx)
            elif offset + f < 0 :
                f += 1
                toAdd.append(actualIdx)

        return toRemove, toAdd

    def synchronizeTiming(self, inputData):
        indexesToRemove, indexesToAdd = self.__recoverTime(inputData)
        inputData = np.delete(inputData, indexesToRemove)
        inputData = np.insert(inputData, indexesToAdd, 0)
        return inputData
