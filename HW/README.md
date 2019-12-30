# Instructions for using PLUTO SDR module

## Instalation



## Overview of signal path

- Baseband data (microphone input) is transmitted 44.1Ksps (int16)
- Data is padded by header used in synchronisation
- Data is then modulated to IF. IF depends on maximum sampling rate of PLUTO (around 30 Msps)
- Inside PLUTO module, data is upconverted to final frequency (in range of 1-2GHz). 
    This value can be modified inside Python 
