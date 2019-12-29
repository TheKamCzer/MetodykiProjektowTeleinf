from rtlsdr import RtlSdr
from queue import Queue
import threading
from Synchronization.FrameSynchronization import FrameSynchronization
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from Synchronization.TimingRecovery import TimingRecovery
import numpy as np

class Receiver:
    def __init__(self, sampleRate, carrierFreq, symbolLength, frameSize):
        self.sampleRate = sampleRate
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.frameSizeInBits = frameSize * 8 / 2
        self.headerStart = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        self.headerEnd = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1,
                          1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1]

        self.rtl = RtlSdr()
        self.rtl.sample_rate = self.sampleRate
        self.rtl.center_freq = self.carrierFreq

        self.demodulator = Demodulator(self.carrierFreq, self.symbolLength, self.sampleRate)
        self.modulator = Modulator(self.carrierFreq, self.symbolLength, self.sampleRate)
        self.frameSync = FrameSynchronization(self.modulator.modulate(self.headerStart),
                                              self.modulator.modulate(self.headerEnd),
                                              self.symbolLength, self.sampleRate)
        self.timeRecover = TimingRecovery(self.symbolLength)

        self.rtlSamples = Queue()
        self.frames = Queue()
        self.previousData = Queue(1)
        self.previousData.put([0])
        self.data = Queue()

        self.threads = []
        self.threads.append(threading.Thread(target=self.receive))
        self.threads.append(threading.Thread(target=self.findFrame))
        self.threads.append(threading.Thread(target=self.processData))
        self.threads.append(threading.Thread(target=self.playSound))

        for th in self.threads:
            th.start()

    def receive(self):
        def rtl_callback(samples, rtlsdr_obj):
            self.rtlSamples.put(samples)

        self.rtl.read_samples_async(rtl_callback, self.sampleRate/10)

    def findFrame(self):
        currentData = self.rtlSamples.get()
        prevData = self.previousData.get()
        data = np.append(prevData, currentData)

        dataPosition = self.frameSync.synchronizeStartHeader(data)
        dataEndPosition = self.frameSync.synchronizeStopHeader(data[dataPosition:])

        if abs(dataEndPosition - self.frameSizeInBits) <= self.frameSizeInBits/10:
            print("Frame found. Size = " + str(dataEndPosition))

            self.previousData.put(data[dataPosition + dataEndPosition:])
            self.frames.put(data[dataPosition:dataPosition + dataEndPosition])
        else:
            self.previousData.put(currentData)

    def processData(self):
        data = self.frames.get()

        data = self.frameSync.correctFreqAndPhase(data)
        data = self.timeRecover.synchronizeTiming(data)
        data = self.demodulator.demodulate(data)

        self.data.put(data)

    def playSound(self):
        dataToPlay = self.data.get()
        #TODO: write func
        return
