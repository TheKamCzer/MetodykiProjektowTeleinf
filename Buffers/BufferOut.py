import sys
import numpy as np

def createBufferOut(self, data):
bufferin = np.unpackbits(data).flatten()
 dataout = np.frombuffer(bufferin, dtype='S1')
if len(dataout) % 2 != 0:
            raise Exception('Data is uneven!')
            returnVal = []
            return ReturnVal
