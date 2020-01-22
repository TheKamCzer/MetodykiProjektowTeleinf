import pyaudio
import queue


class Recorder:
    def __init__(self, input_device_index=0, frames_per_buffer=1024,
                 sample_format=pyaudio.paInt16, channels=1, bit_rate=44100):
        # TODO: automagically select proper mic input
        self.queue = queue.Queue(64)
        self.p = pyaudio.PyAudio()
        self.input_device_index = input_device_index
        self.frames_per_buffer = frames_per_buffer
        self.sample_format = sample_format
        self.channels = channels
        self.bit_rate = bit_rate

    def get_mic_info(self):
        """
        Function prints avaliable input devices (microphones) and
        its indices.
        """
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def start(self):
        """
        Starting mic stream in non-blocking mode
        """
        print("Starting pyAudio mic")
        self.stream = self.p.open(
            format=self.sample_format,
            input_device_index=self.input_device_index,
            channels=self.channels,
            rate=self.bit_rate,
            frames_per_buffer=self.frames_per_buffer,
            input=True,
            output=False,
            stream_callback=self.callback)

    def callback(self, in_data, frame_count, time_info, status):
        """
        Function which is invoked every time new data frame
        from audio subsystem arrives
        """
        if not self.queue.full():
            self.queue.put(in_data)
        else:
            pass
            # print("Mic buffer Overrun!")
            # TODO: uncomment assertion or at least print statement
            # raise ValueError("Microphone buffer overrun")
            # print("New data: " + str(in_data[1:10]))
        return (in_data, pyaudio.paContinue)

    def isEmpty(self):
        """
        Checks whether queue is empty
        """
        return self.queue.qsize == 0

    def get_data(self):
        """
        Retives data from queue. Queue has to be non-empy, 
        otherwise exception will be thrown

        Check it in logic by using isEmpty() method.
        """
        # assert self.isEmpty(), "You can't get data from empty queue"
        if self.isEmpty():
            return None
        else:
            data = self.queue.get()
            self.queue.task_done()
            return data

    def exit(self):
        print("Exiting pyAudio microphone stream")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
