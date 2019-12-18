import numpy as np


class FrameSynchronization:
    def __init__(self, header, symbolLength):
        self.header = header
        self.headerLen = int(len(self.header))
        self.symbolLength = symbolLength
        self.autoCorrelation = np.multiply(self.header, np.conj(self.header))
        self.autoCorrMean = np.mean(self.autoCorrelation)

    def synchronizeFrame(self, inputData):
        dataAutoCorr = np.multiply(inputData, np.conj(inputData))
        dataAutoCorrMean = np.mean(dataAutoCorr)
        crossCorrelation = np.convolve(dataAutoCorr - dataAutoCorrMean, self.autoCorrelation[::-1] - self.autoCorrMean)
        return np.argmax(abs(crossCorrelation)) + 1

