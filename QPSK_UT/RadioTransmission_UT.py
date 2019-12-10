from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator

__INPUT_BITS = [-1, -1, 1, -1, -1, 1, 1, 1]
__END_BITS = [0, 0, 1, 0, 0, 1, 1, 1]
__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


def modulateAndDemodulateBitsWithoutNoise():
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)

    signal = modulator.modulate(__INPUT_BITS)
    demodulatedBits = demodulator.demodulate(signal)
    assert demodulatedBits == __END_BITS
