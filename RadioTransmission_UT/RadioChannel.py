import numpy as np


class RadioChannel:
    def __calcSignalPow(self, signal):
        sigPow = 0
        for i in range(int(len(signal))):
            sigPow += np.power(np.abs(signal[i]), 2)
        sigPow /= int(len(signal))
        return sigPow

    def transmit(self, inputSignal, snr=None):
        if snr is not None:
            noise = np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)
            inputSignal += noise
        return inputSignal
