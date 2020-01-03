import adi


class Transmitter:

    def __init__(self, sample_rate, carrier_freq):
        self.sampleRate = sample_rate
        self.carrierFreq = carrier_freq
        self.pluto = adi.Pluto()
        self.pluto.tx_rf_bandwidth = self.carrierFreq
        # self.pluto.tx_enabled_channels = 1
        # self.pluto.sample_rate = self.sampleRate

    def transmit(self, data):
        self.pluto.tx(data)
