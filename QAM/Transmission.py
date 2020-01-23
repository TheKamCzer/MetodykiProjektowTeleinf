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
import threading
import matplotlib.pyplot as plt


class Transmission:

    def __init__(self, lo_frequency=1.5e9, sampling_rate=1e6, upsamplingFactor=2, input_device_index=0):
        # sys.path.append('/usr/lib/python2.7/site-packages/')
        import adi

        # Constructor data #
        self.lo_frequency = lo_frequency
        self.sampling_rate = sampling_rate
        self.upsamplingFactor = upsamplingFactor
        self.input_device_index = input_device_index

        # Queues for threads
        self.audioQueue = Queue(10)
        self.packetQueue = Queue(10)

        # Gathering samples #
        self.p = pyaudio.PyAudio()
        for i in range(self.p.get_device_count()):
            print(self.p.get_device_info_by_index(i))
        self.stream = self.p.open(
            format=pyaudio.paInt8,
            input_device_index=self.input_device_index,
            channels=1,
            rate=44100,
            frames_per_buffer=1024*4,
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
        self.psfFilter = cp.rrcosfilter(int(self.upsamplingFactor) * 10, 0.35,
                                        self.upsamplingFactor / self.sampling_rate, self.sampling_rate)[1]

        # Initializing PLuto #
        self.sdr_pluto = adi.Pluto()
        self.sdr_pluto.tx_lo = int(self.lo_frequency)
        self.sdr_pluto.sample_rate = int(self.sampling_rate)
        self.sdr_pluto.tx_cyclic_buffer = False

        # Initializing threads
        self.threads = []
        # self.threads.append(threading.Thread(target=self.prepare_frame(), name="micBacground"))
        # self.threads.append(threading.Thread(target=self.send_frame(), name="plutoBackground"))

    def mic_callback(self, in_data, frame_count, time_info, status):
        # print("accessing mic callback")
        if not self.audioQueue.full():
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
        signalIus = signal.upfirdn([1], np.real(
            symbols_QAM4), self.upsamplingFactor)
        signalQus = signal.upfirdn([1], np.imag(
            symbols_QAM4), self.upsamplingFactor)

        # Filter and remove spurious samples added by convolution
        filteredI = np.convolve(signalIus, self.psfFilter)
        filteredQ = np.convolve(signalQus, self.psfFilter)

        signalI = filteredI[int(self.upsamplingFactor * 5)                            : - int(self.upsamplingFactor * 5) + 1]
        signalQ = filteredQ[int(self.upsamplingFactor * 5)                            : - int(self.upsamplingFactor * 5) + 1]

        return signalI + 1j*signalQ

    def unpackbits(self, x, num_bits):
        xshape = list(x.shape)
        x = x.reshape([-1, 1])
        to_and = 2**np.arange(num_bits).reshape([1, num_bits])
        return (x & to_and).astype(bool).astype(int).reshape(xshape + [num_bits])

    def prepare_frame(self):

        # fig,ax = plt.subplots()
        # while True:

            # time.sleep(.01)
            # if not self.audioQueue.empty():

                print("Serving audioQueue. Size: ", self.audioQueue.qsize())


                audio_frame = self.unpackbits(np.frombuffer(
                    self.audioQueue.get(),  dtype=np.int8), 8)
                flatten_audio_frame = np.ndarray.flatten(audio_frame)

                header_bytes = np.array(self.packet_header, dtype=np.int64)
                footer_bytes = np.array(self.packet_footer, dtype=np.int64)

                frame_ready_to_send = self.create_frame(np.concatenate(
                    (header_bytes, flatten_audio_frame, footer_bytes)))

                self.packetQueue.put(frame_ready_to_send)
                self.audioQueue.task_done()

                # ax.scatter(frame_ready_to_send.real,frame_ready_to_send.imag)
                # plt.show(block=False)


    def send_frame(self):
        # time.sleep(0.1)
        # print("Asdasds")
        # while True:

            # time.sleep(.001)
            # print("Serving packetQueue")


            # if not self.packetQueue.empty():

                print("Serving packetQueue. Size: ", self.packetQueue.qsize())

                data_to_tx = self.packetQueue.get()
                self.packetQueue.task_done()
                print(len(data_to_tx))
                self.sdr_pluto.tx(data_to_tx)

                fig,ax = plt.subplots()
                ax.scatter(data_to_tx.real,data_to_tx.imag)
                plt.show(block=True)

    def start(self):
        for th in self.threads:
            th.start()

    def finish(self):
        self.audioQueue.join()

        # for th in self.threads:
        #     th.join()



# import pyaudio
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#   dev = p.get_device_info_by_index(i)
#   print((i,dev['name'],dev['maxInputChannels']))


# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#         print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
try:
    tr = Transmission()

    tr.start()



    while True:
        tr.prepare_frame()
        tr.send_frame()
        # print("asdasdasdad")
        # time.sleep(0.001)

except:
    pass