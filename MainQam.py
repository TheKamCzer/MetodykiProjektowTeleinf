#!/usr/bin/env python3
"""
Code for receiver and transmitter used for QAM modulation
usage:
    python3 MainQam.py --function tx
    python3 MainQam.py --function rx
Information about other options is avaliable by:
    python3 MainQam.py -h
"""
from Record_Play.Recorder import Recorder
from QAM.ModulatorQAM import ModulatorQAM
from time import sleep
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import adi
import random
import itertools


class NieQam:

    def __init__(self, debug: bool = False, hw_used: bool = False):

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
            itertools.chain.from_iterable(__STOP_HEADER_QAMA))

        self.modulatedHeader = mod.modulateQAMA(__START_HEADER_QAMA)
        self.modulatedFooter = mod.modulateQAMA(__STOP_HEADER_QAMA)


        # asdasdasdasdasdasd
        self.__SAMPLING_RATE = 20e6
        self.__CARRIER_FREQ = 10e5

        self.debug = debug
        self.hw_used = hw_used

        self.mod = ModulatorQAM(carrierFreq=self.__CARRIER_FREQ,
                           upsamplingFactor=8, sampleRate=self.__SAMPLING_RATE)

        if self.hw_used == True:
            self.sdr = adi.Pluto()
            self.sdr.tx_lo = int(2e9)  # 2000000000
            self.sdr.tx_cyclic_buffer = False
            self.sdr.tx_hardwaregain = -10
            self.sdr.gain_control_mode = "slow_attack"
            self.fs = int(sdr.sample_rate)
            print("PLUTO sample rate: " + str(fs))

            # Recorder class is used to open input device (microphone)
            self.rec = Recorder(input_device_index=1, frames_per_buffer=1024,
                           channels=1, bit_rate=44100)
            self.rec.get_mic_info()
            self.rec.start()



    def main_qam_tx(self, mic_port: int = 0):

        if self.hw_used == True:
            try:

                print('Transmission Started!')
                while True:
                    if self.rec.isEmpty():
                        # sleep time related to acq of single voice frame
                        sleep(44100/1024)
                    else:
                        # obtaining samples from microphone
                        soundFrame = rec.get_data()

                        modulatedFrame = self.mod.modulateQAMA(
                            self.modulatedHeader + soundFrame + self.modulatedFooter, debug=True)

                        # send data to pluto
                        self.sdr.tx(modulatedFrame)

            except KeyboardInterrupt:
                print('Transmission Ended!')
                self.rec.exit()

        else:
            try:

                print("Dry run. Showing plots...")
                while True:
                    __SIMULATION_DATA = [
                        random.randint(0, 1) for x in range(1024)]
                    modulatedFrame = self.mod.modulateQAMA(
                        self.modulatedHeader + __SIMULATION_DATA + self.modulatedFooter, debug=True)

            except KeyboardInterrupt:
                print('Dry Run Ended!')
            pass

    def main_qam_rx(self, debug: bool = False):
        from Record_Play.Player import Player
        from QAM.DemodulatorQAM import DemodulatorQAM
        from time import sleep
        if debug == True:
            from scipy import signal
            import numpy as np
            import matplotlib

        print("Starting demodulator")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Transmits and receives audio data using QAM16 modulation')
    parser.add_argument('--function',  type=str, default='tx', choices=['tx', 'rx'],  # required=True,
                        help='What function this instance has to serve.')
    parser.add_argument('--mic_used', action='store_true',
                        help='This switch selects data source. Currently only micropphne and random is implemented.')
    parser.add_argument('--hw_used', action='store_true',
                        help='This switch enables PLUTO communication.')
    parser.add_argument('--dry_run', action='store_true',
                        help='OVERWRITES --mic_used. Does not atempt to connect to external world.')
    parser.add_argument('--no_debug', action='store_false',
                        help='Debug flag that plots data.')
    args = parser.parse_args()

    if vars(args)['function'] == 'tx':
        main_qam_tx(vars(args)['no_debug'], vars(args)[
                    'mic_used'], vars(args)['hw_used'])

    elif vars(args)['function'] == 'rx':
        main_qam_rx(vars(args)['debug'])
