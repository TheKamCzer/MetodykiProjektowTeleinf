import pyaudio
import wave

from Record_Play.Player import Player

########################
# CONSTANTS
########################

#Filename
# filename = 'myfile.wav'
filename = '/Users/marcingadek/PycharmProjects/MetodykiProjektowTeleinf/Record_Play/myfile.wav'
# Set chunk size of 1024 samples per data frame
chunk = 1024

# Open the sound file
wf = wave.open(filename, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file;'output = True' indicates that the sound will be played
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
# Read data in chunks
data = wf.readframes(chunk)

def shouldPlay():
    player = Player(stream, data, p, chunk, wf)
    player.play()

