import adi


class Transmitter:
    def __int__(self, sampleRate, carrierFreq):
        self.sampleRate = sampleRate
        self.carrierFreq = carrierFreq
        self.pluto = adi.Pluto(uri="ip:192.168.2.10")
        self.pluto.tx_rf_bandwidth = self.carrierFreq
        self.pluto.dds_frequencies = self.carrierFreq
        self.pluto.tx_enabled_channels = True
        self.pluto.sample_rate = self.sampleRate

    def transmit(self, data):
        self.pluto.tx(data)
