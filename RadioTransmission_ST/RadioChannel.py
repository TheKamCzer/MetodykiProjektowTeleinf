import numpy as np
from scipy import interpolate as inter


class RadioChannel:
    def __init__(self, samplingRate):
        self.samplingRate = samplingRate
        self.samplingTime = 1 / self.samplingRate

    def __calcSignalPow(self, signal):
        sigPow = 0
        for i in range(int(len(signal))):
            sigPow += np.power(np.abs(signal[i]), 2)
        sigPow /= int(len(signal))
        return sigPow

    def transmit(self, inputSignal, snr=None, signalOffset=0, channelAttenuation=1, freqErr=0, phaseErr=0, adcSamplingErr=None):

        if snr is not None:
            noise = np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)\
                + 1j * np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)
            inputSignal += noise

        for i in range(signalOffset):
            inputSignal = np.insert(inputSignal, 0, np.random.normal(0, 1, 1) + 1j * np.random.normal(0, 1, 1))
            inputSignal = np.insert(inputSignal, int(len(inputSignal)), np.random.normal(0, 1, 1) + 1j * np.random.normal(0, 1, 1))

        t = np.arange(0, int(len(inputSignal)) * self.samplingTime,  self.samplingTime)
        inputSignal = inputSignal * 1 / channelAttenuation * np.exp(1j * (2 * np.pi * freqErr * t + phaseErr))

        if adcSamplingErr is not None and adcSamplingErr <= 1:
            interpFunc = inter.interp1d(t, inputSignal, kind='cubic')
            newT = np.arange(abs(adcSamplingErr) / (self.samplingRate * (1 + adcSamplingErr)), int(len(inputSignal) - 1) / self.samplingRate, 1 / (self.samplingRate * (1 + adcSamplingErr)))
            inputSignal = interpFunc(newT)

        return inputSignal
