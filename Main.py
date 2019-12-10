from QPSK_UT import Demodulator_UT, RadioTransmission_UT
#from Record_Play import Play_UT
from Record_Play import Recorder_UT


Demodulator_UT.shouldDemodulateInputBits()
Demodulator_UT.shouldDemodulateMostOfInputBitsWithNoise()

RadioTransmission_UT.modulateAndDemodulateBitsWithoutNoise()

Recorder_UT.shouldRecords()
#Play_UT.shouldPlay()