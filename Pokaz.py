import numpy as np

from QPSK.Demodulator import Demodulator
from QPSK.Modulator import Modulator
from Transmission.Transmitter import Transmitter

__BITS = np.random.randint(2, size=200).tolist()

__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL

modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS,  __SAMPLING_RATE)
demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)
transmitter = Transmitter(__SAMPLING_RATE, __CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS)

modulatedSig = modulator.modulate(__BITS)
transmitter.transmit(modulatedSig)
demodulatedBits = demodulator.demodulate(modulatedSig)


