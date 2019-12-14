import time

from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_UT.RadioChannel import RadioChannel
import numpy as np


########################################################################################################################
#       CONSTANTS
########################################################################################################################

__BITS = np.random.randint(2, size=44100).tolist()
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 8
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __modulateAndDemodulate(snr=None):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel()

    signal = modulator.modulate(__BITS)
    transmittedSignal = channel.transmit(signal, snr)
    demodulatedBits = demodulator.demodulate(transmittedSignal)
    return demodulatedBits


########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldModulateAndDemodulateBitsWithoutErrorWhenNoiseNotPresent():
    demodulatedBits = __modulateAndDemodulate()
    assert demodulatedBits == __BITS

def shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs40():
    demodulatedBits = __modulateAndDemodulate(40)
    assert demodulatedBits == __BITS

def shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs3():
    demodulatedBits = __modulateAndDemodulate(3)

    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if demodulatedBits[i] != __BITS[i]:
            corruptedBits += 1
    assert(corruptedBits/int(len(__BITS)) < 0.01)

def shouldModulateAndDemodulateBitsWithSmallErrorWhenSnrIs0():
    demodulatedBits = __modulateAndDemodulate(0)

    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if demodulatedBits[i] != __BITS[i]:
            corruptedBits += 1
    assert(corruptedBits/int(len(__BITS)) < 0.03)


########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldModulateAndDemodulateBitsWithoutErrorWhenNoiseNotPresent()
    shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs40()
    shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs3()
    shouldModulateAndDemodulateBitsWithSmallErrorWhenSnrIs0()
