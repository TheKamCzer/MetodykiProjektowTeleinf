from QPSK.Demodulator import Demodulator
import numpy


########################################################################################################################
#       CONSTANTS
########################################################################################################################

__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__INPUT_BITS = [1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1,
                1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1]
__OUTPUT_BITS = [1 if x > 0 else 0 for x in __INPUT_BITS]

def __calcSignal() :
    time = numpy.linspace(0, __NUM_OF_PERIODS_IN_SYMBOL / __CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS)
    angle = 2 * numpy.pi * __CARRIER_FREQ * time + __FI

    sig = []
    for i in range(int(len(__INPUT_BITS) / 2)):
        sig.extend(__INPUT_BITS[i * 2] * numpy.cos(angle) - 1j*__INPUT_BITS[i * 2 + 1] * numpy.sin(angle))
    return sig

def __calcSignalPower(signal) :
    sigPow = 0
    for i in range(int(len(signal))):
        sigPow += numpy.power(numpy.abs(signal[i]), 2)
    sigPow /= int(len(signal))
    return sigPow

########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldDemodulateInputBits() :
    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()
    assert(dem.demodulate(signal) == __OUTPUT_BITS)

def shouldDemodulateMostOfInputBitsWithNoise() :

    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()

    noise = numpy.random.normal(0, 1, int(len(signal))) * __calcSignalPower(signal)
    signal += noise
    demodulated = dem.demodulate(signal)
    assert(len(__INPUT_BITS) == len(demodulated))

    corruptedBits = 0
    for i in range(int(len(__INPUT_BITS))) :
        if demodulated[i] != __OUTPUT_BITS[i] :
            corruptedBits += 1
    assert(corruptedBits/len(__INPUT_BITS) < 0.1)