import sys
import numpy as np

def createBufferIn(self, data):
bufferin = np.unpackbits(data).flatten()
 datain = np.frombuffer(bufferin, dtype='S1')
if len(datain) % 2 != 0:
            raise Exception('Data is uneven!')
            returnVal = []
            return ReturnVal
