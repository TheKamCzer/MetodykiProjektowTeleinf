"""
Demodulate QAM 16 signal
"""

import numpy as np
import commpy as cp



class DemodulatorQAM:
    def __init__(self, carrierFreq: int, sampleRate: int, upsamplingFactor=8):
        self.carrierFreq = carrierFreq
        self.upsamplingFactor = upsamplingFactor
        self.symbolLength = upsamplingFactor
        self.sampleRate = sampleRate
        self.sampleTime = 1 / self.sampleRate
        self.psfFilter = cp.rrcosfilter(int(
            self.upsamplingFactor) * 10, 0.35, self.upsamplingFactor / self.sampleRate, self.sampleRate)[1]
        self._MAPPING_TABLE_QAM16 = {
        # TODO: check corectness of the table 
            (0, 0, 0, 0): -3-3j,
            (0, 0, 0, 1): -3-1j,
            (0, 0, 1, 0): -3+3j,
            (0, 0, 1, 1): -3+1j,
            (0, 1, 0, 0): -1-3j,
            (0, 1, 0, 1): -1-1j,
            (0, 1, 1, 0): -1+3j,
            (0, 1, 1, 1): -1+1j,
            (1, 0, 0, 0):  3-3j,
            (1, 0, 0, 1):  3-1j,
            (1, 0, 1, 0):  3+3j,
            (1, 0, 1, 1):  3+1j,
            (1, 1, 0, 0):  1-3j,
            (1, 1, 0, 1):  1-1j,
            (1, 1, 1, 0):  1+3j,
            (1, 1, 1, 1):  1+1j
        }
        self._MAPPING_TABLE_QAMA = {
            (0, 0): -1 - 1j,
            (0, 1): 1 - 1j,
            (1, 0): -1 + 1j,
            (1, 1): +1 + 1j
        }
        


    

    def demodulateQAMA(self, symbolsToDemodulate ):
        """
        demodulates complex IQ data to corresponding bits.
        implements algorithm from:
        https://www.wirelessinnovation.org/assets/Proceedings/2008/sdr08-1.4-3-schreuder.pdf
        of correcponding Matlab code:

        CARRIER = 1000;
        k = 1; mu = 0.1; M = 16; Ts = 1 / 4800;
        phaseNow = 0; phaseEst = phaseNow; phaseInc = 2*pi*CARRIER * Ts;

            for s = pbSymbols(1:end) % An array of passband QAM symbols
            % Demodulate the passband symbol and store in array
            bbSymbols[k] = s .* exp(-j * phaseNow);
            % Find the nearest QAM constellation point to symbol s
            decisionSymbol = qamMatch(s, M);

            % Calculate the phase error
            decisionError = decisionSymbol - s;
            % Calculate the new phase estimate
            theta[k] = phaseEst;
            phaseEst = phaseEst + mu * (imag(conj(decisionError)*s)
                                     / (abs(decisionSymbol)*abs(s)));

            % Calculate the next demodulation phase value
            phaseNow = phaseNow + phaseInc + phaseEst;
            k = k + 1;
        end

        """
        sigLen = int(len(symbolsToDemodulate))
        t = np.arange(0, sigLen * self.sampleTime, self.sampleTime)[:sigLen]
        phase = 2 * np.pi * self.carrierFreq * t

        branchI = np.convolve(np.real(symbolsToDemodulate) * np.cos(phase), self.psfFilter)
        branchI = branchI[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]
        branchQ = np.convolve(np.imag(symbolsToDemodulate) * -np.sin(phase), self.psfFilter)
        branchQ = branchQ[int(self.symbolLength * 5): - int(self.symbolLength * 5) + 1]

        maxAmpI = np.abs(branchI)
        maxAmpMeanI = np. mean(maxAmpI)
        maxAmpQ = np.abs(branchQ)
        maxAmpMeanQ = np. mean(maxAmpQ)


        bitsI = [1 if x > 0 else 0 for x in branchI[0::self.symbolLength]]
        bitsQ = [1 if x > 0 else 0 for x in branchQ[0::self.symbolLength]]
        return [item for sublist in zip(bitsI, bitsQ) for item in sublist]
