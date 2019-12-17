from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from Record_Play.Recorder import Recorder
from Record_Play.Player import Player
import sounddevice as sd
import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "/Users/marcingadek/PycharmProjects/MetodykiProjektowTeleinf/Record_Play/myfile.wav"
p = pyaudio.PyAudio()  # Create an interface to PortAudio

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


def changeBitsToPolar(bits):
    resultBits = []
    for i in range(0, len(bits)):
        bit = bits[i]
        if bit == 0:
            bit = -1
        resultBits.append(bit)
    return resultBits


recorder = Recorder(chunk, sample_format, channels, fs, seconds, p, stream, filename)
inputBits = recorder.record()

modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __NUM_OF_PERIODS_IN_SYMBOL)
demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)

modulatedSig = modulator.modulate(inputBits)

demodulatedBits = demodulator.demodulate(modulatedSig)
sd.play(changeBitsToPolar(demodulatedBits), fs)

