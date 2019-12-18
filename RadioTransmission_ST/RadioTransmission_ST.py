from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
import numpy as np


########################################################################################################################
#       CONSTANTS
########################################################################################################################

__SEED = np.random.seed(238924)
__BITS = np.random.randint(2, size=200).tolist()
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 1
__SYMBOL_LENGTH_IN_BITS = 4
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __modulateSignal():
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    return modulator.modulate(__BITS)

def __demodulateSignal(signal):
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    return demodulator.demodulate(signal)

def __modulateAndDemodulate(snr=None, attenuation=1):
    channel = RadioChannel()
    signal = __modulateSignal()
    transmittedSignal = channel.transmit(signal, snr, channelAttenuation=attenuation)
    return __demodulateSignal(transmittedSignal)

def __assertBerLessThan(signal, maxBer):
    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if signal[i] != __BITS[i]:
            corruptedBits += 1
    assert (corruptedBits / int(len(__BITS)) <= maxBer)


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
    __assertBerLessThan(demodulatedBits, 0.02)

def shouldModulateAndDemodulateBitsWithSmallErrorWhenSnrIs0():
    demodulatedBits = __modulateAndDemodulate(0)
    __assertBerLessThan(demodulatedBits, 0.1)

def shouldModulateAndDemodulateBitsWithoutErrorWhenHighAttenuationPresent():
    demodulatedBits = __modulateAndDemodulate(attenuation=10e6)
    assert demodulatedBits == __BITS

########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldModulateAndDemodulateBitsWithoutErrorWhenNoiseNotPresent()
    shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs40()
    shouldModulateAndDemodulateBitsWithNoErrorWhenSnrIs3()
    shouldModulateAndDemodulateBitsWithSmallErrorWhenSnrIs0()
    shouldModulateAndDemodulateBitsWithoutErrorWhenHighAttenuationPresent()
