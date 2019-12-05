from rtlsdr import RtlSdr

class Receiver:
    def __init__(self, sampleRate, carrierFreq, demodulator):
        self.sampleRate = sampleRate
        self.carrierFreq = carrierFreq
        self.rtl = RtlSdr()
        self.rtl.sample_rate = self.sampleRate
        self.rtl.center_freq = self.carrierFreq
        self.demodulator = demodulator

    def receive(self, numOfSamples):
        samples = self.rtl.read_samples(num_bytes=numOfSamples)
        return samples

