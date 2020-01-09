import pyaudio
import queue


class Player:
    def __init__(self, output_device_index=5, frames_per_buffer=1024,
                 sample_format=pyaudio.paInt16, channels=1, bit_rate=44100):
        self.queue = queue.Queue(64)
        self.p = pyaudio.PyAudio()
        self.output_device_index = output_device_index
        self.frames_per_buffer = frames_per_buffer
        self.sample_format = sample_format
        self.channels = channels
        self.bit_rate = bit_rate


    def get_speaker_info(self):
        """TODO"""
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      self.p.get_device_info_by_host_api_device_index(0, i).get('name'))
     
    def play(self):
        self.stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.bit_rate,
                        output=True,
                        stream_callback=self.callback)
        self.stream.start_stream()

    def callback(self):
        """get data from queue"""
        pass

    def put_data(self, data_chunk):
        """put data from external world"""
        pass

    def exit(self):
        print("Exiting pyAudio output stream")
        self.stream.close()
