from QPSK_UT import Demodulator_UT, RadioTransmission_UT
from Record_Play import Player_UT
from Record_Play import Recorder_UT
from QPSK import Modulator, Demodulator


Demodulator_UT.shouldDemodulateInputBits()
Demodulator_UT.shouldDemodulateMostOfInputBitsWithNoise()

RadioTransmission_UT.modulateAndDemodulateBitsWithoutNoise()

bits = Recorder_UT.shouldRecords()
Player_UT.shouldPlay()
