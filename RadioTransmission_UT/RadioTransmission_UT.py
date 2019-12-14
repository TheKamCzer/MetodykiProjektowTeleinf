from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_UT.RadioChannel import RadioChannel

__BITS = [0, 0, 1, 0, 0, 1, 1, 1]
__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


def modulateAndDemodulateBitsWithoutNoise():
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel(40)

    signal = modulator.modulate(__BITS)
    demodulatedBits = demodulator.demodulate(channel.transmit(signal))
    assert demodulatedBits == __BITS

def modulateAndDemodulateBitsWithSnr40():
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                          __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                              __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel(40)

    signal = modulator.modulate(__BITS)
    demodulatedBits = demodulator.demodulate(channel.transmit(signal, withNoise=True))
    assert demodulatedBits == __BITS

def modulateAndDemodulateBitsWithSnr0():
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                          __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                              __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel(0)

    signal = modulator.modulate(__BITS)
    demodulatedBits = demodulator.demodulate(channel.transmit(signal, withNoise=True))
    assert demodulatedBits == __BITS

def run():
    modulateAndDemodulateBitsWithoutNoise()
    modulateAndDemodulateBitsWithSnr40()
    modulateAndDemodulateBitsWithSnr0()
