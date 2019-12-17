import pyaudio
import wave


class Recorder:
    def __init__(self, chunk, sample_format, channels, fs, seconds, p, stream, filename):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.seconds = seconds
        self.p = p
        self.stream = stream
        self.filename = filename

    def record(self):
        frames = []
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            frames.extend(data)

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        # wf = wave.open(self.filename, 'wb')
        # wf.setnchannels(self.channels)
        # wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        # wf.setframerate(self.fs)
        # wf.writeframes(b''.join(self.frames))
        # wf.close()
        return frames
