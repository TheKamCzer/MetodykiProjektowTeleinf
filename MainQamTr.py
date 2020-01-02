"""
Code used to transmit data through PLUTO module

"""

from Record_Play.Recorder import Recorder
from QAM.ModulatorQAM import ModulatorQAM
from time import sleep

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# TODO: Create asserts that checks whether iiolib and pyadi is installed
import adi

# Create instance of PLUTO radio and configure its properties
sdr = adi.Pluto()
# sdr.tx_rf_bandwidth = 4000000
sdr.tx_lo = int(2e9) #2000000000
# TODO: remove cyclic buffer as it continously sends single packet 
sdr.tx_cyclic_buffer = True 
sdr.tx_hardwaregain = -10
sdr.gain_control_mode = "slow_attack"

fs = int(sdr.sample_rate)
print("PLUTO sample rate: " + str(fs))

# Recorder class is used to open input device (microphone)
rec = Recorder(input_device_index=9, frames_per_buffer=1024,
               channels=1, bit_rate=44100)

# Modulator class transforms microphone data into QAM modulated packets
# TODO: calculate correct sample rate which is
# sum of data rate(bit_rate) + overhead created by header and footer
mod = ModulatorQAM(carrierFreq=100e3, upsamplingFactor=8, sampleRate=fs)

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
            soundFrame, isSignalUpconverted=True, debug=False)
        print(modulatedFrame[:100])
        # plt.plot(np.real(modulatedFrame))
        # plt.show()

        # TODO: remove cyclic buffer and feed data continuously 
        sdr.tx(modulatedFrame)
        break


for _ in range(200):
    x = sdr.rx()
    f, Pxx_den = signal.periodogram(x, fs)
    plt.clf()
    plt.semilogy(f, Pxx_den)
    plt.ylim([1e-7, 1e2])
    plt.xlabel("frequency [Hz]")
    plt.ylabel("PSD [V**2/Hz]")
    plt.draw()
    plt.pause(0.05)
    sleep(0.1)

plt.show()





        
