import numpy as np
from scipy import signal as sig
from scipy import interpolate as inter
from matplotlib import pyplot as plt
import commpy as cp


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

    def upConversion(self, signal, carrierFreq):
        n = np.arange(0, int(len(signal)-1))
        plt.subplot(2, 1, 1)
        phase = 2 * np.pi * carrierFreq/self.samplingRate * n
        plt.psd(signal, Fs=self.samplingRate)
        # plt.magnitude_spectrum(signal)
        # signal1 = np.multiply(np.real(signal), np.cos(phase)) - np.multiply(np.imag(signal), np.sin(phase))
        signal1 = np.multiply(0.5*signal[:len(n)], np.exp(1j*phase))
        plt.subplot(2, 1, 2)
        # plt.magnitude_spectrum(signal1)
        plt.psd(signal1, Fs=self.samplingRate)
        plt.show()
        return signal1

    def downConversion(self, signal, carrierFrequency):
        phase = (2 * np.pi * carrierFrequency/self.samplingRate) * np.arange(0, int(len(signal)))
        result = np.multiply(2 * signal, np.exp(-1j * phase))

        numOfProb = 250
        fir = cp.rrcosfilter(numOfProb, 0.35, self.samplingTime, self.samplingRate)[1]
            # sig.firwin(numOfProb, [0.25, 0.75], nyq=self.samplingRate * 0.5, pass_zero=False, window='hamming', scale=False)

        signal = np.convolve(result, fir)
        signal1 = signal[: int(len(phase))]

        return result

    def transmit(self, inputSignal, snr=None, carrFreq=None, signalOffset=0, channelAttenuation=1, freqErr=0, phaseErr=0, adcSamplingErr=None):
        if carrFreq is not None:
            inputSignal = self.upConversion(inputSignal, carrFreq)

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

        if carrFreq is not None:
            inputSignal = self.downConversion(inputSignal, carrFreq)

        return inputSignal
