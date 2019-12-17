from Synchronization.FrameSynchronization import FrameSynchronization
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
import numpy as np

########################################################################################################################
#       CONSTANTS
########################################################################################################################

__HEADER = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
__SEED = np.random.seed(238923)
__BITS = np.random.randint(2, size=500).tolist()
__FRAME = __HEADER + __BITS
__SYMBOL_LENGTH_IN_BITS = 8
__BUFFER_SIZE = 1024
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __transmitSignalWithFrameSynchronization(expectedDataPosition=32*__SYMBOL_LENGTH_IN_BITS, snr=None, offset=0,
                                             freqErr=0, phaseErr=0):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                              __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel()
    frameSync = FrameSynchronization(modulator.modulate(__HEADER), __SYMBOL_LENGTH_IN_BITS)

    signal = modulator.modulate(__FRAME)
    transmittedSignal = channel.transmit(signal, snr=snr, signalOffset=offset, freqErr=freqErr, phaseErr=phaseErr)
    dataPosition = frameSync.synchronizeFrame(transmittedSignal)
    assert(dataPosition == expectedDataPosition + offset)

    demodulatedBits = demodulator.demodulate(transmittedSignal[dataPosition:])
    return demodulatedBits

def __assertBerLessThan(signal, maxBer):
    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if signal[i] != __BITS[i]:
            corruptedBits += 1
    assert (corruptedBits / int(len(__BITS)) <= maxBer)


########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldFindFrameWithoutNoiseAtTheBeginningOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization()
    assert(demodulatedBits == __BITS)

def shouldFindFrameWithoutNoiseInTheMiddleOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(offset=177)
    assert(demodulatedBits == __BITS)

def shouldFindFrameWithSnr3AtTheBeginningOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=3)
    __assertBerLessThan(demodulatedBits, 0.05)

def shouldFindFrameWithSnr3InTheMiddleOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=3, offset=242)
    __assertBerLessThan(demodulatedBits, 0.05)

def shouldFindFrameWithSmallPhaseError():
    __transmitSignalWithFrameSynchronization(snr=10, phaseErr=np.pi/17)

def shouldFindFrameWithLargePhaseError():
    __transmitSignalWithFrameSynchronization(snr=3, phaseErr=np.pi)

def shouldFindFrameWithSmallFreqError():
    __transmitSignalWithFrameSynchronization(snr=10, freqErr=10e-4 * __CARRIER_FREQ)

def shouldFindFrameWithLargeFreqAndPhaseError():
    __transmitSignalWithFrameSynchronization(snr=10, freqErr=10e-2 * __CARRIER_FREQ, phaseErr=np.pi/2)

########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldFindFrameWithoutNoiseAtTheBeginningOfStream()
    shouldFindFrameWithoutNoiseInTheMiddleOfStream()
    shouldFindFrameWithSnr3AtTheBeginningOfStream()
    shouldFindFrameWithSnr3InTheMiddleOfStream()
    shouldFindFrameWithSmallPhaseError()
    shouldFindFrameWithLargePhaseError()
    shouldFindFrameWithSmallFreqError()
    shouldFindFrameWithLargeFreqAndPhaseError()
