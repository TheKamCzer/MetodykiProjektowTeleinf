"""
Script used to transmission data.

It consist of following submodules(threads):
- data acqusition
- frame creatoin
- frame transmission
"""
from queue import Queue
import numpy as np
import sys
import pyaudio

sys.path.append('/usr/lib/python2.7/site-packages/')


class Transmission:

    def __init__(self, lo_frequency=1.5e9, sampling_rate=1e6, upsamplingFactor=2, input_device_index=0):
        import adi

        # Constructor data
        self.lo_frequency = lo_frequency
        self.sampling_rate = sampling_rate
        self.upsamplingFactor = upsamplingFactor
        self.input_device_index = input_device_index

        # Gathering samples
        self.p = pyaudio.PyAudio()
        self.audioQueue = Queue(10000)
        self.stream = self.p.open(
            format=pyaudio.paInt8,
            input_device_index=self.input_device_index,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
            stream_callback=self.mic_callback)

        # Headers for frame modulation
        # Gold sequence #1, 32
        # TOTAL SIZE: 64 bits
        self.packet_header = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        # Pseudo random binary sequence
        # TOTAL SIZE: 88 bits
        self.packet_footer = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]

        # Initializing PLuto
        self.sdr_pluto = adi.Pluto()
        self.sdr_pluto = adi.Pluto()
        self.sdr_pluto.tx_lo = int(self.lo_frequency)
        self.sdr_pluto.sample_rate = self.sampling_rate
        self.sdr_pluto.tx_cyclic_buffer = False

    def mic_callback(self, in_data, frame_count, time_info, status):
        self.audioQueue.put(in_data)
        return (in_data, pyaudio.paContinue)

    def create_frame(self, data_to_send):

        # QAM4 has 2 bits per symbol thus we divide by 2
        Bits_per_symbol =2 
        symbol_length = int(len(data_to_send)/Bits_per_symbol)

        # grouping data into chunks of 2
        data_groupped = np.array(data_to_send).reshape(
            symbol_length, Bits_per_symbol)




