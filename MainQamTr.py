"""
Code used to transmit data through PLUTO module

"""

from Record_Play.Recorder import Recorder
from QAM.ModulatorQAM import ModulatorQAM
from time import sleep

import numpy as np
import matplotlib.pyplot as plt

# /usr/local/lib/python3.7/dist-packages
# /usr/local/lib/python3.7/site-packages
# TODO: Create asserts that checks whether iio lib is installed
import iio


# Recorder class is used to open input device (microphone)
rec = Recorder(input_device_index=9, frames_per_buffer=1024,
               channels=1, bit_rate=44100)

# Modulator class transforms microphone data into QAM modulated packets
# TODO: calculate correct sample rate which is
# sum of data rate(bit_rate) + overhead created by header and footer
mod = ModulatorQAM(carrierFreq=100e3, upsamplingFactor=8, sampleRate=20e6)

# Starting gathering samples. Data is returned by method get_data()
rec.start()

while True:
    if rec.isEmpty():
        sleep(44100/1024)
    else:
        soundFrame = rec.get_data()
        # print(soundFrame[0:22])

        # TODO: add proper header and trailer to data
        modulatedFrame = mod.modulateQAM16(
            soundFrame, isSignalUpconverted=True, debug=True)
        print(modulatedFrame[:100])
        # plt.plot(np.real(modulatedFrame))
        # plt.show()

        
