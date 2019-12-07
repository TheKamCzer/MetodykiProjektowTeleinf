import pyaudio
import wave


class Recorder:
    def __init__(self,chunk,sample_format,channels,fs,seconds,p,stream,frames,filename):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.seconds = seconds
        self.p = p
        self.stream = stream
        self.frames = frames
        self.filename = filename


    def record(self):
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            self.data = self.stream.read(self.chunk)
            self.frames.append(self.data)

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        return wf