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

def __transmitSignalWithFrameSynchronization(expectedDataPosition=256, snr=None, offset=0):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE,
                              __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel()
    frameSync = FrameSynchronization(modulator.modulate(__HEADER), __SYMBOL_LENGTH_IN_BITS)

    signal = modulator.modulate(__FRAME)
    transmittedSignal = channel.transmit(signal, snr=snr, signalOffset=offset)
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
    demodulatedBits = __transmitSignalWithFrameSynchronization(offset=171)
    assert(demodulatedBits == __BITS)

def shouldFindFrameWithSnr3AtTheBeginningOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=3)
    __assertBerLessThan(demodulatedBits, 0.05)

def shouldFindFrameWithSnr3InTheMiddleOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=3, offset=242)
    __assertBerLessThan(demodulatedBits, 0.05)

########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldFindFrameWithoutNoiseAtTheBeginningOfStream()
    shouldFindFrameWithoutNoiseInTheMiddleOfStream()
    shouldFindFrameWithSnr3AtTheBeginningOfStream()
    shouldFindFrameWithSnr3InTheMiddleOfStream()
