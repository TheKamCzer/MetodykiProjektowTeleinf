import sys
import threading
from queue import Queue

from QPSK.Modulator import Modulator

sys.path.append('/usr/lib/python2.7/site-packages/')
import adi

headerStart = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
               1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
headerEnd = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
             1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0,
             0, 0, 1, 1]


class Transmitter:

    def __init__(self, sample_rate, carrier_freq, symbol_length):
        self.sampleRate = sample_rate
        self.carrierFreq = carrier_freq
        self.symbolLength = symbol_length
        self.modulator = Modulator(carrier_freq, self.symbolLength, self.sampleRate)
        self.modulatedStartHeader = self.modulator.modulate(headerStart)
        self.modulatedEndHeader = self.modulator.modulate(headerEnd)

        self.pluto = adi.Pluto()
        # self.pluto.tx_rf_bandwidth
        self.pluto.tx_lo = int(self.carrierFreq)
        # self.pluto.tx_enabled_channels = [0, 1]
        self.pluto.sample_rate = self.sampleRate

        self.recordedDataQueue = Queue()
        self.modulatedDataQueue = Queue()
        self.dataToTransmit = Queue()

        self.threads = []
        self.threads.append(threading.Thread(target=self.record(), name="micRecorder"))
        self.threads.append(threading.Thread(target=self.modulateData(), name="modulateData"))
        self.threads.append(threading.Thread(target=self.prepareDataToTransmit(), name="prepareDataToTransmit"))
        self.threads.append(threading.Thread(target=self.transmit(), name="transmitter"))

    def record(self):
        def callback():
            self.recordedDataQueue.put(0)
        #TODO: writeFunc of record from mic
        # data = ""
        # self.recordedDataQueue.put(data)
        pass

    def modulateData(self):
        if not self.recordedDataQueue.empty():
            data = self.recordedDataQueue.get()
            self.recordedDataQueue.task_done()
            modulatedData = self.modulator.modulate(data)
            self.modulatedDataQueue.put(modulatedData)

    def prepareDataToTransmit(self):
        if self.modulatedDataQueue.qsize() > 1024:
            data = self.modulatedDataQueue.get()
            preparedData = self.modulatedStartHeader + data + self.modulatedEndHeader
            self.dataToTransmit.put(preparedData)

    def transmit(self, data):
        self.pluto.tx(data)

    def transmit(self):
        if not self.dataToTransmit.empty():
            data = self.dataToTransmit.get()
            self.pluto.tx_destroy_buffer()
            self.pluto.tx(data)
            self.dataToTransmit.task_done()
