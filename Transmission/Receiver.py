from rtlsdr import RtlSdr
from queue import Queue
import threading
from Synchronization.FrameSynchronization import FrameSynchronization
from QPSK.Modulator import Modulator
from QPSK.Demodulator import Demodulator
from Synchronization.TimingRecovery import TimingRecovery

class Receiver:
    def __init__(self, sampleRate, carrierFreq, symbolLength, frameSize):
        self.sampleRate = sampleRate
        self.carrierFreq = carrierFreq
        self.symbolLength = symbolLength
        self.frameSize = frameSize
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
        self.data = Queue()

        self.threads = []
        self.threads.append(threading.Thread(target=self.receive))
        #self.threads.append( threading.Thread(target=self.findFrame, args=(self.queueRfIQ, self.queueAudio, )) )
        #self.threads.append( threading.Thread(target=self.processData, args=(self.queueAudio, self.queueCommandsSpeaker, )) )
        #self.threads.append( threading.Thread(target=self.playSound))

    def receive(self):
        def rtl_callback(samples, rtlsdr_obj):
            self.rtlSamples.put(samples)

        self.rtl.read_samples_async(rtl_callback, self.sampleRate/10)

