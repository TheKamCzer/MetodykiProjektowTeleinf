import numpy as np


class FrameSynchronization:
    def __init__(self, startHeader, stopHeader, symbolLength, samplingRate):
        self.startHeader = startHeader
        self.stopHeader = stopHeader
        self.headerLen = int(len(self.startHeader))
        self.stopHeaderLen = int(len(self.stopHeader))
        self.symbolLength = symbolLength
        self.startAutoCorrelation = np.multiply(self.startHeader, np.conj(self.startHeader))
        self.startAutoCorrMean = np.mean(self.startAutoCorrelation)
        self.stopAutoCorrelation = np.multiply(self.stopHeader, np.conj(self.stopHeader))
        self.stopAutoCorrMean = np.mean(self.stopAutoCorrelation)
        self.samplingRate = samplingRate
        self.samplingTime = 1 / self.samplingRate
        self.receivedHeader = []

    def synchronizeStartHeader(self, inputData):
        dataAutoCorr = np.multiply(inputData, np.conj(inputData))
        dataAutoCorrMean = np.mean(dataAutoCorr)
        crossCorrelation = np.convolve(dataAutoCorr - dataAutoCorrMean, self.startAutoCorrelation[::-1] - self.startAutoCorrMean)
        dataPosition = np.argmax(crossCorrelation) + 1
        self.receivedHeader = inputData[dataPosition - self.headerLen : dataPosition]
        return dataPosition

    def synchronizeStopHeader(self, inputData):
        dataAutoCorr = np.multiply(inputData, np.conj(inputData))
        dataAutoCorrMean = np.mean(dataAutoCorr)
        crossCorrelation = np.convolve(dataAutoCorr - dataAutoCorrMean, self.stopAutoCorrelation[::-1] - self.stopAutoCorrMean)
        dataPosition = np.argmax(abs(crossCorrelation)) + 1
        return dataPosition - self.stopHeaderLen

    def correctFreqAndPhase(self, inputSignal): #TODO: Camcore95 - do sth when snr is less than 20
        headerAutoCorr = np.multiply(self.receivedHeader[::self.symbolLength], np.conj(self.startHeader[::self.symbolLength]))
        phi = np.angle(headerAutoCorr[round(self.headerLen / self.symbolLength / 2)])
        headerAutoCorr = headerAutoCorr * np.exp(-1j*phi)
        ang = np.unwrap(np.angle(headerAutoCorr))
        temp = np.polyfit(np.arange(0, self.headerLen / self.samplingRate, self.symbolLength / self.samplingRate), ang, 1)
        dph = temp[1] + phi
        df = temp[0] / (2 * np.pi)
        t = np.arange(0, int(len(inputSignal)) * self.samplingTime, self.samplingTime)
        inputSignal = inputSignal * np.exp(-1j * (2 * np.pi * df * t + dph))
        return inputSignal
