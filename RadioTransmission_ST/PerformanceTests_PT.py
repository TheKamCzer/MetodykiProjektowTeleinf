from Synchronization.FrameSynchronization import FrameSynchronization
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
from Synchronization.TimingRecovery import TimingRecovery
import numpy as np
import time

########################################################################################################################
#       CONSTANTS
########################################################################################################################

__HEADER = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
__END_HEADER = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
__SEED = np.random.seed(283319)
__BITS = np.random.randint(2, size=4000).tolist()
__FRAME = __HEADER + __BITS
__SYMBOL_LENGTH_IN_BITS = 8
__CARRIER_FREQ = 50000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __transmitSignal(samplingError, offset, snr, attenuation, freqErr, phaseErr):
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE)
    channel = RadioChannel(__SAMPLING_RATE)
    frameSync = FrameSynchronization(modulator.modulate(__HEADER), modulator.modulate(__END_HEADER),
                                     __SYMBOL_LENGTH_IN_BITS, __SAMPLING_RATE)
    timeRecover = TimingRecovery(__SYMBOL_LENGTH_IN_BITS)

    modulationStart = time.time()

    modulatedSignal = modulator.modulate(__FRAME)

    assert(time.time() - modulationStart < 1 / 20)

    transmittedSignal = channel.transmit(modulatedSignal, signalOffset=offset, adcSamplingErr=samplingError, snr=snr,
                                         channelAttenuation=attenuation, freqErr=freqErr, phaseErr=phaseErr)

    synchronizationStart = time.time()

    dataPosition = frameSync.synchronizeStartHeader(transmittedSignal)
    transmittedSignal = frameSync.correctFreqAndPhase(transmittedSignal[dataPosition:])
    transmittedSignal = timeRecover.synchronizeTiming(transmittedSignal)

    demodulatedBits = demodulator.demodulate(transmittedSignal)

    assert (time.time() - synchronizationStart < 1 / 20)
    return demodulatedBits

def __assertBerLessThan(signal, maxBer):
    corruptedBits = 0
    for i in range(int(len(__BITS))):
        if signal[i] != __BITS[i]:
            corruptedBits += 1
    print(corruptedBits / int(len(__BITS)))
    assert(corruptedBits / int(len(__BITS)) <= maxBer)


########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldDemodulateSignalProperly():
    demodulatedBits = __transmitSignal(offset=131, attenuation=10, samplingError=3*10e-6, freqErr=10e-4*__CARRIER_FREQ,
                                       phaseErr=np.pi/17, snr=40)
    assert(demodulatedBits == __BITS)

def shouldDemodulateSignalProperly2():
    demodulatedBits = __transmitSignal(offset=93, attenuation=20, samplingError=-3 * 10e-6,
                                       freqErr=-3*10e-4 * __CARRIER_FREQ, phaseErr=np.pi / 3, snr=20)
    assert(demodulatedBits == __BITS)

########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldDemodulateSignalProperly()
    shouldDemodulateSignalProperly2()
