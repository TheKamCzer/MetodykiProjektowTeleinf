"""
Script used to transmission data.

It consist of following submodules(threads):
- data acqusition
- frame creatoin
- frame transmission
"""
import time
from queue import Queue
import numpy as np
import commpy as cp
from scipy import signal
import sys
import pyaudio


class Transmission:

    def __init__(self, lo_frequency=1.5e9, sampling_rate=1e6, upsamplingFactor=2, input_device_index=1):
        # sys.path.append('/usr/lib/python2.7/site-packages/')
        import adi

        # Constructor data #
        self.lo_frequency = lo_frequency
        self.sampling_rate = sampling_rate
        self.upsamplingFactor = upsamplingFactor
        self.input_device_index = input_device_index

        # Gathering samples #
        self.p = pyaudio.PyAudio()
        for i in range(self.p.get_device_count()):
            print(self.p.get_device_info_by_index(i))
        self.audioQueue = Queue(10000)
        self.stream = self.p.open(
            format=pyaudio.paInt8,
            input_device_index=self.input_device_index,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
            stream_callback=self.mic_callback)


        # frame modulation #
        # Gold sequence #1, 32
        # TOTAL SIZE: 64 bits
        self.packet_header = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        # Pseudo random binary sequence
        # TOTAL SIZE: 88 bits
        self.packet_footer = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                              1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
        self._MAPPING_TABLE_QAM4 = {
            (0, 0): -1 - 1j,
            (0, 1): 1 - 1j,
            (1, 0): -1 + 1j,
            (1, 1): +1 + 1j
        }
        self.psfFilter = cp.rrcosfilter(int(self.upsamplingFactor) * 10, 0.35, self.upsamplingFactor / self.sampling_rate, self.sampling_rate)[1]


        # Initializing PLuto #
        self.sdr_pluto = adi.Pluto()
        self.sdr_pluto.tx_lo = int(self.lo_frequency)
        self.sdr_pluto.sample_rate = int(self.sampling_rate)
        self.sdr_pluto.tx_cyclic_buffer = False

    def mic_callback(self, in_data, frame_count, time_info, status):
        self.audioQueue.put(in_data)
        return (in_data, pyaudio.paContinue)

    def create_frame(self, data_to_send):

        # QAM4 has 2 bits per symbol thus we divide by 2
        Bits_per_symbol = 2
        symbol_length = int(len(data_to_send)/Bits_per_symbol)

        # grouping data into chunks of 2
        data_groupped = np.array(data_to_send).reshape(
            symbol_length, Bits_per_symbol)

        # using dictionary to convert input data array to symbols
        symbols_QAM4 = np.array(
            [self._MAPPING_TABLE_QAM4[tuple(b)] for b in data_groupped])

        # Upsample the data
        signalIus = signal.upfirdn([1], np.real(symbols_QAM4), self.upsamplingFactor)
        signalQus = signal.upfirdn([1], np.imag(symbols_QAM4), self.upsamplingFactor)

        # Filter and remove spurious samples added by convolution
        filteredI = np.convolve(signalIus, self.psfFilter)
        filteredQ = np.convolve(signalQus, self.psfFilter)

        signalI = filteredI[int(self.upsamplingFactor * 5): - int(self.upsamplingFactor * 5) + 1]
        signalQ = filteredQ[int(self.upsamplingFactor * 5): - int(self.upsamplingFactor * 5) + 1]

        return signalI + 1j*signalQ



tr = Transmission()
tr.create_frame(tr.packet_footer)


time.sleep(1)

print(tr.audioQueue.get())
