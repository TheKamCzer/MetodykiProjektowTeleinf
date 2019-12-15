import numpy as np


class RadioChannel:
    def __calcSignalPow(self, signal):
        sigPow = 0
        for i in range(int(len(signal))):
            sigPow += np.power(np.abs(signal[i]), 2)
        sigPow /= int(len(signal))
        return sigPow

    def transmit(self, inputSignal, snr=None, signalOffset=None):
        if snr is not None:
            noise = np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)\
                + 1j * np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -snr/10)
            inputSignal += noise
        if signalOffset is not None:
            for i in range(signalOffset):
                inputSignal = np.insert(inputSignal, 0, inputSignal[-1])
                inputSignal = np.delete(inputSignal, int(len(inputSignal) - 1))
        return inputSignal
