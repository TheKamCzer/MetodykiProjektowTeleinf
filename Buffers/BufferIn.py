import sys
import numpy as np

def createBufferIn(self, data):
bufferin = np.unpackbits(data).flatten()
#Jutro dodac pętle działającą aż do opróżnienia bufforu 
datain = np.frombuffer(bufferin, dtype='S1', count=1024) #Na przykład 1024, wielkość ramki bez nagłówków
if len(datain) % 2 != 0:
            raise Exception('Data is uneven!')
            returnVal = []
            return ReturnVal
