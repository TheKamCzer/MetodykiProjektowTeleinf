from QPSK.Demodulator import Demodulator
import numpy as np


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
    time = np.linspace(0, __NUM_OF_PERIODS_IN_SYMBOL / __CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS)
    angle = 2 * np.pi * __CARRIER_FREQ * time + __FI

    sig = []
    for i in range(int(len(__INPUT_BITS) / 2)):
        sig.extend(__INPUT_BITS[i * 2] * np.cos(angle) - 1j*__INPUT_BITS[i * 2 + 1] * np.sin(angle))
    return sig

def __calcSignalPower(signal) :
    sigPow = 0
    for i in range(int(len(signal))):
        sigPow += np.power(np.abs(signal[i]), 2)
    sigPow /= int(len(signal))
    return sigPow

########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldDemodulateInputBits() :
    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()
    assert(dem.demodulate(signal) == __OUTPUT_BITS)

def shouldDemodulateMostOfInputBitsWithNoise() :

    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()

    noise = np.random.normal(0, 1, int(len(signal))) * __calcSignalPower(signal)
    signal += noise
    demodulated = dem.demodulate(signal)
    assert(len(__INPUT_BITS) == len(demodulated))

    corruptedBits = 0
    for i in range(int(len(__INPUT_BITS))) :
        if demodulated[i] != __OUTPUT_BITS[i] :
            corruptedBits += 1
    assert(corruptedBits/len(__INPUT_BITS) < 0.1)

def test() :
    for j in range(__SYMBOL_LENGTH_IN_BITS - 2):
        signal = __calcSignal()
        for i in range(j + 1) :
            signal.insert(0, signal.pop())

        noise = np.random.normal(0, 1, int(len(signal))) * __calcSignalPower(signal)
        signal += noise
        N = int(len(signal))
        dem = Demodulator(__CARRIER_FREQ-2, __SYMBOL_LENGTH_IN_BITS, __FI, __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL, __NUM_OF_PERIODS_IN_SYMBOL)

        FF = np.zeros([__SYMBOL_LENGTH_IN_BITS])
        FF[0] = abs(signal[0])
        for i in range(N-1) :
            FF[i % __SYMBOL_LENGTH_IN_BITS] += (abs(signal[i+1] - signal[i]))

        demodulated = dem.demodulate(signal[np.argmax(FF) :])
        corruptedBits = 0
        for i in range(int(len(__INPUT_BITS)) - 2):
            if demodulated[i] != __OUTPUT_BITS[i]:
                corruptedBits += 1
        assert (corruptedBits / len(__INPUT_BITS) <= 0.1)
