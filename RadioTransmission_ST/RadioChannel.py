import numpy as np
from scipy import interpolate as inter


class RadioChannel:
    def __calcSignalPow(self, signal):
        sigPow = 0
        for i in range(int(len(signal))):
            sigPow += np.power(np.abs(signal[i]), 2)
        sigPow /= int(len(signal))
        return sigPow

    def transmit(self, inputSignal, snr=None, signalOffset=0, channelAttenuation=1, channelPhase=0, carrierFreqErr=0,
                 carrierPhaseErr=0, adcSamplingErr=None):
        if snr is not None:
            noise = np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)\
                + 1j * np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)
            inputSignal += noise

        for i in range(signalOffset):
            inputSignal = np.insert(inputSignal, 0, np.random.normal(0, 1, 1))

        inputSignal = inputSignal * 1 / channelAttenuation * np.exp(1j * channelPhase)
        t = np.arange(0, int(len(inputSignal)), 1)
        inputSignal = inputSignal * np.exp(1j * (2 * np.pi * carrierFreqErr * t + carrierPhaseErr))

        if adcSamplingErr is not None:
            interpFunc = inter.interp1d(t, inputSignal, kind='cubic')
            inputSignal = interpFunc(np.arange(adcSamplingErr, adcSamplingErr + int(len(inputSignal)) - 1, 1))

        return inputSignal
