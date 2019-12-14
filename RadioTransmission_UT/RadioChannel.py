import numpy as np


class RadioChannel:
    def __init__(self, snr):
        self.snr = snr

    def __calcSignalPow(self, signal):
        sigPow = 0
        for i in range(int(len(signal))):
            sigPow += np.power(np.abs(signal[i]), 2)
        sigPow /= int(len(signal))
        return sigPow

    def transmit(self, inputSignal, withNoise=False):
        if withNoise:
            noise = np.random.normal(0, 1, int(len(inputSignal))) * self.__calcSignalPow(inputSignal) * pow(10, -self.snr/10)
            inputSignal += noise
        return inputSignal
