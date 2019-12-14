from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_UT.RadioChannel import RadioChannel
import numpy as np

__BITS = np.random.randint(2, size=44100).tolist()
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 8
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


def __modulateAndDemodulate(snr=None):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel()

    signal = modulator.modulate(__BITS)
    demodulatedBits = demodulator.demodulate(channel.transmit(signal, snr))
    return demodulatedBits

def modulateAndDemodulateBitsWithoutNoise():
    demodulatedBits = __modulateAndDemodulate()
    assert demodulatedBits == __BITS

def modulateAndDemodulateBitsWithSnr40():
    demodulatedBits = __modulateAndDemodulate(40)
    assert demodulatedBits == __BITS

def modulateAndDemodulateBitsWithSnr0():
    demodulatedBits = __modulateAndDemodulate(0)

    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if demodulatedBits[i] != __BITS[i]:
            corruptedBits += 1
    assert(corruptedBits/int(len(__BITS)) < 0.02)

def run():
    modulateAndDemodulateBitsWithoutNoise()
    modulateAndDemodulateBitsWithSnr40()
    modulateAndDemodulateBitsWithSnr0()
