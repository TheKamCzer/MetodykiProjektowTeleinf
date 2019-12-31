from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from Transmission import Transmitter
import _thread as thread
import numpy as np


__BITS = np.random.randint(2, size=200).tolist()

__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL

transmitter = Transmitter(__SAMPLING_RATE, __CARRIER_FREQ)
modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __NUM_OF_PERIODS_IN_SYMBOL)
demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)

modulatedSig = modulator.modulate(__BITS)
transmitter.transmit(modulatedSig)
demodulatedBits = demodulator.demodulate(modulatedSig)

# fir = signal.firwin(199, [__CARRIER_FREQ * 0.6, __CARRIER_FREQ * 1.4], nyq=__SAMPLING_RATE * 0.5, pass_zero=False,
#                   window='hamming', scale=False)
#
#      transmittedSignal = np.convolve(transmittedSignal, fir)
#      transmittedSignal = transmittedSignal[int(99): - 100]

