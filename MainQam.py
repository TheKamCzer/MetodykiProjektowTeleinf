#!/usr/bin/env python3
"""
Code for receiver and transmitter used for QAM modulation
usage:
    python3 MainQam.py --function tx
    python3 MainQam.py --function rx
Information about other options is avaliable by:
    python3 MainQam.py -h
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from time import sleep
from QAM.ModulatorQAM import ModulatorQAM
from Record_Play.Recorder import Recorder
import itertools
import random
import argparse
import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
from Record_Play.Player import Player
from QAM.DemodulatorQAM import DemodulatorQAM
from scipy import signal
import numpy as np
import matplotlib

from rtlsdr import RtlSdr



class NieQam:
    import sys

    def __init__(self, debug: bool = False, hw_used: bool = False, mic_port: int = 0, play_port: int = 0):

        # asdasdasdasdasdasd
        self.__SAMPLING_RATE = 2e6
        self.__IF_FREQ = 100e3
        self.__CARRIER_FREQ = 1.5e9

        self.debug = debug
        self.hw_used = hw_used

        self.mod = ModulatorQAM(carrierFreq=self.__IF_FREQ,
                                upsamplingFactor=8, sampleRate=self.__SAMPLING_RATE)
        # Gold sequence #1, 32
        self.__START_HEADER_QAMA = [0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3,
                                    0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 3, 0, 3, 3, 0, 0, 0, 3, 3, 0]
        self.__START_HEADER_QAMA = [[0, 0] if x == 0 else [1, 1]
                                    for x in self.__START_HEADER_QAMA]
        self.__START_HEADER_QAMA = list(
            itertools.chain.from_iterable(self.__START_HEADER_QAMA))
        # Pseudo random binary sequence
        __STOP_HEADER_QAMA = [3, 3, 3, 0, 0, 0, 3, 0, 0, 3, 3, 0, 3, 0, 3, 3, 3, 0, 0,
                              0, 3, 0, 0, 3, 3, 0, 3, 0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0, 3, 3, 0, 3, 0, 3]
        self.__STOP_HEADER_QAMA = [[0, 0] if x ==
                                   0 else [1, 1] for x in __STOP_HEADER_QAMA]
        self.__STOP_HEADER_QAMA = list(
            itertools.chain.from_iterable(self.__STOP_HEADER_QAMA))

        self.modulatedHeader = self.mod.modulateQAMA(self.__START_HEADER_QAMA)
        self.modulatedFooter = self.mod.modulateQAMA(self.__STOP_HEADER_QAMA)

        self.simulationMedium =[]

        if self.hw_used == True:
            import adi
            self.sdr = adi.Pluto()
            self.sdr.tx_lo = int(2e9)  # 2000000000
            self.sdr.tx_cyclic_buffer = False
            self.sdr.tx_hardwaregain = -10
            self.sdr.gain_control_mode = "slow_attack"
            self.fs = int(self.sdr.sample_rate)
            print("PLUTO sample rate: " + str(self.fs))

            # Recorder class is used to open input device (microphone)
            self.rec = Recorder(input_device_index=mic_port, frames_per_buffer=1024,
                                channels=1, bit_rate=44100)
            self.rec.get_mic_info()
            self.rec.start()

            # Player class is used to open output device (speaker)
            self.rec = Recorder(output_device_index=play_port, frames_per_buffer=1024,
                    channels=1, bit_rate=44100)

            sdr = RtlSdr()

            # configure device
            self.sdr.sample_rate = __SAMPLING_RATE #2.048e6  # Hz
            self.sdr.center_freq = __CARRIER_FREQ #1.5e9 #70e6     # Hz
            print(sdr.get_center_freq())
            print(sdr.get_sample_rate())
            self.sdr.freq_correction = 60   # PPM
            self.sdr.gain = 'auto'


    def main_qam_tx(self):

        if self.hw_used == True:
            try:

                print('Transmission Started!')
                while True:
                    if self.rec.isEmpty():
                        # sleep time related to acq of single voice frame
                        sleep(44100/1024)
                    else:
                        # obtaining samples from microphone
                        soundFrame = self.rec.get_data()

                        modulatedFrame = self.mod.modulateQAMA(
                            self.modulatedHeader + soundFrame + self.modulatedFooter, debug=True)

                        # send data to pluto
                        self.sdr.tx(modulatedFrame)

            except KeyboardInterrupt:
                print('Transmission Ends!')
                self.rec.exit()

        else:
            try:

                print("Dry run. Showing plots...")
                while True:
                    __SIMULATION_DATA = [
                        random.randint(0, 1) for x in range(1024)]
                    modulatedFrame = self.mod.modulateQAMA( np.concatenate(
                       ( self.__START_HEADER_QAMA , __SIMULATION_DATA , self.__STOP_HEADER_QAMA)), debug=True)

                    simulationMedium.append(modulatedFrame)

            except KeyboardInterrupt:
                print('Dry Run Ended!')
            pass





    def main_qam_rx(self, debug: bool = False):
        print("Starting demodulator")

        if self.hw_used == True:
            try:
                pass





            except KeyboardInterrupt:
                print('Demodulation Ends!')
                self.rec.exit()

        else:
            try:

                print("Dry run. Showing plots...")
                while True:
                    if not simulationMedium:

                        receivedData = self.demod.demodulateQAMA(inputQueue.getData())
                        print("Data received: ")
                        print(receivedData)

            except KeyboardInterrupt:
                print('Dry Run Ended!')
            pass


            self.sdr = RtlSdr()


    def getRawSdrSamples(self):
        return self.sdr.read_samples(512)





    












if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Transmits and receives audio data using QAM16 modulation')
    parser.add_argument('--function',  type=str, default='tx', choices=['tx', 'rx'],  # required=True,
                        help='What function this instance has to serve.')
    parser.add_argument('--mic_port', type=int, default=0,
                        help='This switch selects data source. Currently only microphone and random is implemented.')
    parser.add_argument('--play_port', type=int, default=0,
                        help='This switch selects data source. Currently only microphone and random is implemented.')
    parser.add_argument('--hw_used', action='store_true',
                        help='This switch enables PLUTO communication.')
    parser.add_argument('--no_debug', action='store_false',
                        help='Debug flag that plots data.')
    args = parser.parse_args()

    print("Using following args: " + str(vars(args)))

    qam16 = NieQam(vars(args)['no_debug'], vars(args)['hw_used'], vars(
        args)['mic_port'], vars(args)['play_port'])

    if vars(args)['function'] == 'tx':
        print("Strarting TX module...")
        sleep(1)
        qam16.main_qam_tx()

    elif vars(args)['function'] == 'rx':
        print("Strarting RX module...")
        sleep(1)
        qam16.main_qam_rx()
