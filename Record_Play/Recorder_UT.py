import pyaudio
import wave
from Record_Play.Recorder import Recorder

####################
#CONSTANTS
####################


chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "outputfile1.wav"
p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

def shouldRecords():
    recorder = Recorder(chunk,sample_format,channels,fs,seconds,p,stream,frames,filename)
    recorder.record()


