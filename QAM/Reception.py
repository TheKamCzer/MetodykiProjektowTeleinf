"""
    Single tx frame consist of ** 32920  ** symbols at:
    - QAM4
    - 8x upsampling
"""
from rtlsdr import RtlSdr
import threading
import matplotlib.pyplot as plt
from queue import Queue
import numpy as np
import commpy as cp
from scipy import signal
import pyaudio
import asyncio
from time import sleep

from Synchronization.FrameSynchronization import FrameSynchronization
from Synchronization.TimingRecovery import TimingRecovery

from Transmission import Transmitter


class Reception:

    def __init__(self, lo_frequency=1.5e9, sampling_rate=1e6, upsamplingFactor=2, output_device_index=0):

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

        # Constructor data #
        self.lo_frequency = lo_frequency
        self.sampling_rate = sampling_rate
        self.upsamplingFactor = upsamplingFactor
        self.output_device_index = output_device_index

        # Queue for incoming samples
        self.inputQueue = Queue(23)

        # Queue for playing data
        self.audioQueue = Queue(22)

        # Since maximimum number of samples that RTLSDR can return is 131072
        # we do not need concatenate more than last output buffer
        self.lastBuffer= [0]



        # RTL
        self.rtl = RtlSdr()
        self.rtl.sample_rate = self.sampling_rate
        self.rtl.center_freq = self.lo_frequency
        self.rtl.freq_correction = 60   # PPM
        self.rtl.gain = 'auto'

        # Player
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt8,
            channels=1,
            rate=44100,
            output=True,
            stream_callback=self.player_callback)

        
        # Data recovery 
        self.frameSync = FrameSynchronization(self.recreate_header_frame(self.packet_header),
                                              self.recreate_header_frame(self.packet_footer),
                                              self.upsamplingFactor, self.sampling_rate)

        self.timeRecover = TimingRecovery(self.upsamplingFactor)

        
        def player_callback(self, in_data, frame_count, time_info, status):
            if self.audioQueue.empty():
                data =[0, 1]*1024*4
            else:
                data = self.audioQueue.get()
                self.audioQueue.task_done()

            return (data, pyaudio.paContinue)




    async def rtl_streaming(self):
        dataCount= 0

        async for samples in self.rtl.stream():
            # do something with samples
            # ...
            print(samples)
            print(len(samples))
            self.inputQueue.put([dataCount, "Asdasdasdasd"])
            print("data pushed to queue", str(dataCount))
            dataCount = dataCount +1

        # to stop streaming:
        await self.rtl.stop()

        # done
        self.rtl.close()

    async def simulation_stream(self):
        dataCount= 0
        while True:
            await asyncio.sleep(1)
            self.inputQueue.put([dataCount, "Asdasdasdasd"])
            print("data pushed to queue", str(dataCount))
            dataCount = dataCount +1
        await sleep(1)

    
    async def data_processing(self):

        while True:
            if not self.inputQueue.empty():
                
                raw_input = self.inputQueue.get()
                self.inputQueue.task_done()

                samples_to_process= np.concatenate(self.lastBuffer, raw_input).ravel()
                samples_corrected_timing = self.frameSync.correctFreqAndPhase(samples_to_process)
                dataPosition = self.frameSync.synchronizeStartHeader(samples_corrected_timing)
                dataEndPosition = self.frameSync.synchronizeStopHeader(samples_corrected_timing)
                output_frame = samples_corrected_timing[dataPosition:dataEndPosition]
                data = self.timeRecover.synchronizeTiming(output_frame)

                bits = np.packbits(data.view(np.int8))
                self.audioQueue.put(bits)
                self.lastBuffer = raw_input

                print(data[:10*8])
                print(bits[:10])

                fig,ax = plt.subplots()
                ax.scatter(data.real,data.imag)
                plt.show(block=True)









    def recreate_header_frame(self, data_to_send):

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

        signalI = filteredI[int(self.upsamplingFactor * 5)  : - int(self.upsamplingFactor * 5) + 1]
        signalQ = filteredQ[int(self.upsamplingFactor * 5)  : - int(self.upsamplingFactor * 5) + 1]

        return signalI + 1j*signalQ








rx = Reception()

loop = asyncio.get_event_loop()
loop.create_task(rx.rtl_streaming())
loop.create_task(rx.data_processing())

loop.run_forever()
loop.close()




















