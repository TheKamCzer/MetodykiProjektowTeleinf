import pyaudio
import wave


class Player:
    def __init__(self, stream, data, p, chunk, wf):
        self.stream = stream
        self.data = data
        self.p = p
        self.wf = wf
        self.chunk = chunk

    def play(self):

        while self.data != '':
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)
        # Close and terminate the stream
        print('Stopped')
        self.stream.close()
        self.p.terminate()
        return 0
