from Synchronization.TimingRecovery import TimingRecovery
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
import numpy as np

########################################################################################################################
#       CONSTANTS
########################################################################################################################

__SEED = np.random.seed(238923)
__BITS = np.random.randint(2, size=2070).tolist()
__SYMBOL_LENGTH_IN_BITS = 32
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __transmitSignalWithTimingSynchronization(samplingErr):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)
    timeRecover = TimingRecovery(__SYMBOL_LENGTH_IN_BITS)
    channel = RadioChannel(__SAMPLING_RATE)

    signal = modulator.modulate(__BITS)
    transmittedSignal = channel.transmit(signal, adcSamplingErr=samplingErr, snr=10)
    transmittedSignal = timeRecover.synchronizeTiming(transmittedSignal)
    demodulatedBits = demodulator.demodulate(transmittedSignal)
    return demodulatedBits

########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldProperlyDemodulateBitsWithLittleTooHighSampling():
    demodulatedBits = __transmitSignalWithTimingSynchronization(0.001)
    assert(demodulatedBits == __BITS)

def shouldProperlyDemodulateBitsWithLittleTooLowSampling():
    demodulatedBits = __transmitSignalWithTimingSynchronization(-0.001)
    assert(demodulatedBits == __BITS)


########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldProperlyDemodulateBitsWithLittleTooHighSampling()
    shouldProperlyDemodulateBitsWithLittleTooLowSampling()
