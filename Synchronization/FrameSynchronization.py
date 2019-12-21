import numpy as np


class FrameSynchronization:
    def __init__(self, header, symbolLength, samplingRate):
        self.header = header
        self.headerLen = int(len(self.header))
        self.symbolLength = symbolLength
        self.autoCorrelation = np.multiply(self.header, np.conj(self.header))
        self.autoCorrMean = np.mean(self.autoCorrelation)
        self.samplingRate = samplingRate
        self.receivedHeader = []

    def synchronizeFrame(self, inputData):
        dataAutoCorr = np.multiply(inputData, np.conj(inputData))
        dataAutoCorrMean = np.mean(dataAutoCorr)
        crossCorrelation = np.convolve(dataAutoCorr - dataAutoCorrMean, self.autoCorrelation[::-1] - self.autoCorrMean)
        dataPosition = np.argmax(abs(crossCorrelation)) + 1
        self.receivedHeader = inputData[dataPosition - self.headerLen : dataPosition]
        return dataPosition

    def correctFreqAndPhase(self, inputSignal): #TODO: Camcore95 - do sth when snr is less than 20 and check performance
        headerAutoCorr = np.multiply(self.receivedHeader[::self.symbolLength], np.conj(self.header[::self.symbolLength]))
        phi = np.angle(headerAutoCorr[round(self.headerLen / self.symbolLength / 2)])
        headerAutoCorr = headerAutoCorr * np.exp(-1j*phi)
        ang = np.unwrap(np.angle(headerAutoCorr))
        temp = np.polyfit(np.arange(0, self.headerLen / self.samplingRate, self.symbolLength / self.samplingRate), ang, 1)
        dph = temp[1] + phi
        df = temp[0] / (2 * np.pi)
        t = np.arange(0, int(len(inputSignal)) / self.samplingRate, 1 / self.samplingRate)
        inputSignal = inputSignal * np.exp(-1j * (2 * np.pi * df * t + dph))
        return inputSignal
