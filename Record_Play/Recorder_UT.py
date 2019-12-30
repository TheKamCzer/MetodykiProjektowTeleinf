
import time
from Record_Play.Recorder import Recorder
from pyaudio import paInt16

####################
# CONSTANTS
####################

# record in chunks of 1024 samples
__FRAMES_PER_BUFFER = 1024
# 16 bits per sample
__SAMPLE_FORMAT = paInt16
#
__NUM_OF_CHANNLES = 1
# Record at 44100 samples per second
__SAMPLING_RATE = 44100


rec = Recorder(input_device_index=7, frames_per_buffer=__FRAMES_PER_BUFFER,
               sample_format=__SAMPLE_FORMAT, channels=__NUM_OF_CHANNLES, bit_rate=__SAMPLING_RATE)

print('Openning stream')

print(rec.get_mic_info())

rec.start()

frame_number = 0
while not rec.isEmpty():
    print("Frame number: " + str(frame_number))
    frame_number += frame_number
    data = rec.get_data()
    print(data)

    if frame_number==32:
        break

rec.exit()
