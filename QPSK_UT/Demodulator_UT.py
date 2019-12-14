from QPSK.Demodulator import Demodulator
import numpy as np
import commpy as cp


########################################################################################################################
#       CONSTANTS
########################################################################################################################

__CARRIER_FREQ = 100
__NUM_OF_PERIODS_IN_SYMBOL = 2
__SYMBOL_LENGTH_IN_BITS = 32
__FI = 0
__SAMPLE_RATE = __CARRIER_FREQ * __SYMBOL_LENGTH_IN_BITS / __NUM_OF_PERIODS_IN_SYMBOL
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
__PSF = cp.rrcosfilter(int(__SYMBOL_LENGTH_IN_BITS)*10 , 0.35, __SYMBOL_LENGTH_IN_BITS / __SAMPLE_RATE , __SAMPLE_RATE)[1]


########################################################################################################################
#       FUNCTIONS
########################################################################################################################

def __filterSignal(inSig):
    filtered = np.convolve(__PSF, inSig)
    filtered = filtered[int(__SYMBOL_LENGTH_IN_BITS*5): -int(__SYMBOL_LENGTH_IN_BITS*5)+1]
    return filtered

def __calcSignal():
    numOfBitsPerSig = int(len(__INPUT_BITS) / 2)

    sigI = np.zeros([int(len(__INPUT_BITS) * __SYMBOL_LENGTH_IN_BITS / 2)])
    sigQ = np.zeros([int(len(__INPUT_BITS) * __SYMBOL_LENGTH_IN_BITS / 2)])

    for i in range(numOfBitsPerSig):
        sigI[int(i * __SYMBOL_LENGTH_IN_BITS)] = __INPUT_BITS[2 * i]
        sigQ[int(i * __SYMBOL_LENGTH_IN_BITS)] = __INPUT_BITS[2 * i + 1]

    sigI = __filterSignal(sigI)
    sigQ = __filterSignal(sigQ)

    t = np.linspace(0, __NUM_OF_PERIODS_IN_SYMBOL / __CARRIER_FREQ * numOfBitsPerSig, __SYMBOL_LENGTH_IN_BITS * numOfBitsPerSig)
    ang = 2 * np.pi * __CARRIER_FREQ * t + __FI

    return np.multiply(sigI, np.cos(ang)) - 1j * np.multiply(sigQ, np.sin(ang))

def __calcSignalPower(signal):
    sigPow = 0
    for i in range(int(len(signal))):
        sigPow += np.power(np.abs(signal[i]), 2)
    sigPow /= int(len(signal))
    return sigPow

########################################################################################################################
#       TEST CASES
########################################################################################################################

def shouldDemodulateInputBits():
    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLE_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()
    assert(dem.demodulate(signal) == __OUTPUT_BITS)

def shouldDemodulateMostOfInputBitsWithNoise():
    dem = Demodulator(__CARRIER_FREQ, __SYMBOL_LENGTH_IN_BITS, __FI, __SAMPLE_RATE, __NUM_OF_PERIODS_IN_SYMBOL)
    signal = __calcSignal()

    noise = np.random.normal(0, 1, int(len(signal))) * __calcSignalPower(signal) + 1j * np.random.normal(0, 1, int(len(signal))) * __calcSignalPower(signal)
    signal += noise
    demodulated = dem.demodulate(signal)
    assert(len(__INPUT_BITS) == len(demodulated))

    corruptedBits = 0
    for i in range(int(len(__INPUT_BITS))) :
        if demodulated[i] != __OUTPUT_BITS[i] :
            corruptedBits += 1
    assert(corruptedBits/int(len(__INPUT_BITS)) < 0.01)


########################################################################################################################
#       RUN ALL TESTS
########################################################################################################################

def run():
    shouldDemodulateInputBits()
    shouldDemodulateMostOfInputBitsWithNoise()
