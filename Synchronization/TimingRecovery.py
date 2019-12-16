import numpy as np

class TimingRecovery:
    def __init__(self, bufferSizeInSymbols, symbolLength):
        self.bufferSizeInSymbols = bufferSizeInSymbols
        self.symbolLength = symbolLength

    def recoverTime(self, inputData):
        M = int(self.bufferSizeInSymbols * self.symbolLength)
        outputData = []
        while int(len(inputData)) >= int(M + self.bufferSizeInSymbols):
            FF = np.zeros([self.symbolLength])
            for j in range(M):
                FF[j % self.symbolLength] += (abs(inputData[j]))
            index = int(np.argmin(FF) - self.symbolLength / 2) % self.symbolLength
            print(index)
            inputData = inputData[index:]
            outputData.extend(inputData[:M])
            inputData = inputData[M:]
        return [outputData, inputData]
