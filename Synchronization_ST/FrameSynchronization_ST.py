from Synchronization.FrameSynchronization import FrameSynchronization
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
from Synchronization.TimingRecovery import TimingRecovery
import numpy as np

########################################################################################################################
#       CONSTANTS
########################################################################################################################

__HEADER = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
__SEED = np.random.seed(283319)
__BITS = np.random.randint(2, size=2000).tolist()
__FRAME = __HEADER + __BITS
__SYMBOL_LENGTH_IN_BITS = 8
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
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel(__SAMPLING_RATE)
    frameSync = FrameSynchronization(modulator.modulate(__HEADER), __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)

    signal = modulator.modulate(__FRAME)
    transmittedSignal = channel.transmit(signal, snr=snr, signalOffset=offset, freqErr=freqErr, phaseErr=phaseErr)
    dataPosition = frameSync.synchronizeFrame(transmittedSignal)
    assert(dataPosition == expectedDataPosition + offset)

    transmittedSignal = frameSync.correctFreqAndPhase(transmittedSignal[dataPosition:])
    demodulatedBits = demodulator.demodulate(transmittedSignal)
    return demodulatedBits

def __transmitSignalWithFrameSynchronizationAndSamplingError(samplingError, offset, snr=None):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    channel = RadioChannel(__SAMPLING_RATE)
    frameSync = FrameSynchronization(modulator.modulate(__HEADER), __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)
    timeRecover = TimingRecovery(__SYMBOL_LENGTH_IN_BITS)

    signal = modulator.modulate(__FRAME)
    transmittedSignal = channel.transmit(signal, signalOffset=offset, adcSamplingErr=samplingError, snr=snr)
    dataPosition = frameSync.synchronizeFrame(transmittedSignal)
    transmittedSignal = transmittedSignal[dataPosition:]
    transmittedSignal = timeRecover.synchronizeTiming(transmittedSignal)

    demodulatedBits = demodulator.demodulate(transmittedSignal)
    return demodulatedBits

def __assertBerLessThan(signal, maxBer):
    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if signal[i] != __BITS[i]:
            corruptedBits += 1
    assert(corruptedBits / int(len(__BITS)) <= maxBer)


########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldFindFrameWithoutNoiseAtTheBeginningOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization()
    assert(demodulatedBits == __BITS)

def shouldFindFrameWithoutNoiseInTheMiddleOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(offset=177)
    assert(demodulatedBits == __BITS)

def shouldFindFrameWithSnr10AtTheBeginningOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=10)
    __assertBerLessThan(demodulatedBits, 0.05)

def shouldFindFrameWithSnr10InTheMiddleOfStream():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=20, offset=242)
    __assertBerLessThan(demodulatedBits, 0.08)

def shouldFindFrameWithSmallPhaseError():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=20, phaseErr=np.pi/17)
    __assertBerLessThan(demodulatedBits, 0.001)

def shouldFindFrameWithLargePhaseError():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=20, phaseErr=np.pi)
    __assertBerLessThan(demodulatedBits, 0.001)

def shouldFindFrameWithSmallFreqError():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=20, freqErr=10e-4 * __CARRIER_FREQ)
    __assertBerLessThan(demodulatedBits, 0.001)

def shouldFindFrameWithLargeFreqAndPhaseError():
    demodulatedBits = __transmitSignalWithFrameSynchronization(snr=40, freqErr=-2*10e-4 * __CARRIER_FREQ, phaseErr=np.pi)
    __assertBerLessThan(demodulatedBits, 0.001)

def shouldProperlyDemodulateSignalWithGivenBerWhenFrameAndHigherSamplingRate():
    demodulatedBits = __transmitSignalWithFrameSynchronizationAndSamplingError(samplingError=0.001, offset=534, snr=10)
    assert(demodulatedBits == __BITS)

def shouldProperlyDemodulateSignalWithGivenBerWhenFrameAndLowerSamplingRate():
    demodulatedBits = __transmitSignalWithFrameSynchronizationAndSamplingError(samplingError=-0.0001, offset=345, snr=10)
    assert(demodulatedBits == __BITS)


########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldFindFrameWithoutNoiseAtTheBeginningOfStream()
    shouldFindFrameWithoutNoiseInTheMiddleOfStream()
    shouldFindFrameWithSnr10AtTheBeginningOfStream()
    shouldFindFrameWithSnr10InTheMiddleOfStream()
    shouldFindFrameWithSmallPhaseError()
    shouldFindFrameWithLargePhaseError()
    shouldFindFrameWithSmallFreqError()
    shouldFindFrameWithLargeFreqAndPhaseError()
    shouldProperlyDemodulateSignalWithGivenBerWhenFrameAndHigherSamplingRate()
    shouldProperlyDemodulateSignalWithGivenBerWhenFrameAndLowerSamplingRate()
