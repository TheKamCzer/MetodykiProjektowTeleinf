## Instructions for using PLUTO SDR module

### Instalation on Ubuntu 18.04 and later
 - libiio has to be installed from the latest tag (https://github.com/analogdevicesinc/libiio/releases/tag/v0.18) 
 - add to .profile `export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/site-packages` and reboot computer


https://analogdevicesinc.github.io/pyadi-iio/guides/quick.html

### Overview of signal path

- Baseband data (microphone input) is transmitted 44.1Ksps (int16)
- Data is padded by header used in synchronisation
- Data is then modulated to IF. IF depends on maximum sampling rate of PLUTO (around 30 Msps)
- Inside PLUTO module, data is upconverted to final frequency (in range of 1-2GHz). 
    This value can be modified inside Python code

## Instructions for using RTL2 module
 - `sudo apt-get install git cmake libusb-1.0-0.dev build-essential`
 - download source code from from https://github.com/librtlsdr/librtlsdr/releases
 - `cd rtl-sdr`
 - `cmake .`
 - `make`
 - `sudo make install`
 - `sudo ldconfig`