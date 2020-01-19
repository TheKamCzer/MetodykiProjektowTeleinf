"""
Demodulate QAM 16 signal
"""

import numpy as np
import commpy as cp


class DemodulatorQAM:
    def __init__(self, carrierFreq: int, sampleRate: int, upsamplingFactor=8):
        self.carrierFreq = carrierFreq
        self.upsamplingFactor = upsamplingFactor
        self.sampleRate = sampleRate
        self.psfFilter = cp.rrcosfilter(int(
            self.upsamplingFactor) * 10, 0.35, self.upsamplingFactor / self.sampleRate, self.sampleRate)[1]


    def demodulateQAM16(self, symbolsToDemodulate : np.array):
        """
        demodulates complex IQ data to corresponding bits.
        implements alghorim from:
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
        pass