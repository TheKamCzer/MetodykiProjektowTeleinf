from Synchronization.TimingRecovery import TimingRecovery
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from RadioTransmission_ST.RadioChannel import RadioChannel
import numpy as np

########################################################################################################################
#       CONSTANTS
########################################################################################################################

__BITS = np.random.randint(2, size=5000).tolist()
__SYMBOL_LENGTH_IN_BITS = 8
__BUFFER_SIZE = 1024
__CARRIER_FREQ = 20000
__NUM_OF_PERIODS_IN_SYMBOL = 2
__FI = 0
__SAMPLING_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL


########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldRemoveFirstBitFromOtherSymbol():  #TODO: Camcore fix this shit
    modulator = Modulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    demodulator = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLING_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    timeRecover = TimingRecovery(__BUFFER_SIZE, __SYMBOL_LENGTH_IN_BITS)
    channel = RadioChannel()

    signal = modulator.modulate(__BITS)
    transmittedSignal = channel.transmit(signal, snr=3, signalOffset=2)
    recoveredSignal, rest = timeRecover.recoverTime(transmittedSignal)
    recoveredSignal.extend(rest)
    demodulatedBits = demodulator.demodulate(recoveredSignal)

    properBits = __BITS
    corruptedBits = 0
    for i in range(int(len(demodulatedBits))):
        if demodulatedBits[i] != properBits[i]:
            corruptedBits += 2
            if int(len(properBits)) <= i +2 and demodulatedBits[i] == properBits[i+2]:
                del properBits[i]
                del properBits[i+1]


########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldRemoveFirstBitFromOtherSymbol()