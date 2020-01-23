"""
    Single tx frame consist of ** 32920  ** symbols at:
    - QAM4
    - 8x upsampling
"""
from rtlsdr import RtlSdr
import threading
# import matplotlib.pyplot as plt
from queue import Queue
import numpy as np
import commpy as cp
from scipy import signal
import pyaudio
import asyncio
from time import sleep

class Reception:

    def __init__(self, lo_frequency=1.5e9, sampling_rate=1e6, upsamplingFactor=2, output_device_index=0):

        # Constructor data #
        self.lo_frequency = lo_frequency
        self.sampling_rate = sampling_rate
        self.upsamplingFactor = upsamplingFactor
        self.output_device_index = output_device_index

        # Queue for incoming samples
        self.inputQueue = Queue(23)

        # Queue for playing data
        self.audioQueue = Queue(22)


        # RTL
        # self.rtl = RtlSdr()
        # self.rtl.sample_rate = self.sampling_rate
        # self.rtl.center_freq = self.lo_frequency
        # self.rtl.freq_correction = 60   # PPM
        # self.rtl.gain = 'auto'

        # Player
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt8,
            channels=1,
            rate=44100,
            output=True,
            stream_callback=self.player_callback)

        
        def player_callback(self, in_data, frame_count, time_info, status):
            if self.audioQueue.empty():
                data =[0]*1024*4
            else:
                data = self.audioQueue.get()




    async def rtl_streaming(self):
        async for samples in self.rtl.stream():
            # do something with samples
            # ...
            print(samples)
            print(len(samples))
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
        pass


    async def data_player(self):
        pass









rx = Reception()

loop = asyncio.get_event_loop()
# loop.run_until_complete(rx.rtl_streaming())
loop.run_until_complete(rx.simulation_stream())


#         aaa = self.rtl.read_samples(2920)
#         print(aaa)

#         # self.packetQueue = Queue(10)
    
#     def receive(self):
#         print(self.rtl.read_samples(32920))

# rx = Reception()
# # while True:
# # rx.receive()


# from time import sleep


# import asyncio
# from rtlsdr import RtlSdr

# async def streaming():
#     sdr = RtlSdr()
#     sdr.sample_rate =1e6
#     sdr.center_freq = 1.5e9

#     async for samples in sdr.stream():
#         # do something with samples
#         # ...
#         print(samples)
#         print(len(samples))

#     # to stop streaming:
#     sleep(2)
#     await sdr.stop()

#     # done
#     sdr.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(streaming())

# print("asdas")



















