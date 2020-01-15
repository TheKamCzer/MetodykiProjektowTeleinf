#!/usr/bin/env python3
"""
Code for receiver and transmitter used for QAM modulation
usage:
    python3 MainQam.py --function tx 
    python3 MainQam.py --function rx 
Information about other options is avaliable by:
    python3 MainQam.py -h
"""
# TODO: pass those parameters from command line
__SAMPLING_RATE = 20e6
__CARRIER_FREQ = 10e5

__START_HEADER = [0,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,
                 2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1, 0]
__END_HEADER = [1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,
               2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(+15)+1,2**(+15)+1,2**(-15)-1,2**(-15)-1,2**(+15)+1, 0]

def main_qam_tx(debug: bool = False, mic_used: bool = False, hw_used: bool = False, dry_run: bool = True):
    from Record_Play.Recorder import Recorder
    from QAM.ModulatorQAM import ModulatorQAM
    from time import sleep
    if debug == True:
        from scipy import signal
        import numpy as np
        import matplotlib.pyplot as plt

    if dry_run == True:
        hw_used = False
        mic_used
    if hw_used == True:
        try:
            import adi
            if debug == True:
                print("ADI PLUTO lib successfully imported.")

            sdr = adi.Pluto()
            # TODO: Change to int as conversion introduces rounding errors
            sdr.tx_lo = int(2e9)  # 2000000000
            # TODONE: remove cyclic buffer as it continously sends single packet/framebuffer
            sdr.tx_cyclic_buffer = False
            sdr.tx_hardwaregain = -10
            sdr.gain_control_mode = "slow_attack"
            fs = int(sdr.sample_rate)
            if debug == True:
                print("PLUTO sample rate: " + str(fs))
        except:
            print('Error while importing Analog Device\'s PLUTO library\n')

    if mic_used == True:
        try:
            # Recorder class is used to open input device (microphone)
            # TODO: automatically find correct `input_device_index`
            rec = Recorder(input_device_index=1, frames_per_buffer=1024,
                           channels=1, bit_rate=44100)
            if debug == True:
                rec.get_mic_info()
            rec.start()
            # TODO: caught exception when bad index is chosen
            # INFO: for demonstration, mic is turned off
        except:
            print('Ex: error while opening input stream\n')

    # Modulator class transforms microphone data into QAM modulated packets
    # TODO: calculate correct sample rate which is
    # sum of data rate(bit_rate) + overhead created by header and footer
    mod = ModulatorQAM(carrierFreq=__CARRIER_FREQ,
                       upsamplingFactor=8, sampleRate=__SAMPLING_RATE)

    if mic_used == True and hw_used == True:
        # Starting gathering voice samples. Data is returned by method get_data()

        try:
            print('Transmission Started!')
            while True:
                if rec.isEmpty():
                    # sleep time related to acq of single voice frame
                    sleep(44100/1024)
                else:
                    # obtaining samples from microphone
                    soundFrame = rec.get_data()

                    # modulating data
                    # TODO: add proper header and trailer to data
                    modulatedFrame = mod.modulateQAM16(
                        soundFrame, isSignalUpconverted=True, debug=debug)

                    # send data to pluto
                    sdr.tx(modulatedFrame)

        except KeyboardInterrupt:
            print('Transmission Ended!')
            rec.exit()

    elif debug == True:
        try:
            from QAM_UT.ModulatorQAM_UT import __RANDOM_1024_INT16 as soundFrame
            # from Synchronization_ST.FrameSynchronization_ST import __START_HEADER
            # from Synchronization_ST.FrameSynchronization_ST import __END_HEADER

            print("Dry run. Showing plots...")
            while True:
                modulatedFrame = mod.modulateQAM16(
                    np.concatenate((np.frombuffer(np.asarray(__START_HEADER) * 2**15,  dtype=np.int16),
                                   soundFrame[:], # TODO: change number of samples by cmd option
                                   np.frombuffer(np.asarray(__END_HEADER)* 2**15,  dtype=np.int16))),
                    isSignalUpconverted=True, debug=True)
                
                break;

        except KeyboardInterrupt:
            print('Dry Run Ended!')

        # TODO: show just plots

        print(modulatedFrame[:100])
        # plt.plot(np.real(modulatedFrame))
        # plt.show()

        pass
    else:
        NameError("asdasasd")


def main_qam_rx(debug: bool = False):
    pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Transmits and receives audio data using QAM16 modulation')
    parser.add_argument('--function',  type=str, default='tx', choices=['tx', 'rx'],  # required=True,
                        help='What function this instance has to serve.')
    parser.add_argument('--mic_used', action='store_true',
                        help='This switch selects data source. Currently only micropphne and random is implemented.')
    parser.add_argument('--hw_used', action='store_true',
                        help='This switch enables PLUTO communication.')
    parser.add_argument('--dry_run', action='store_true',
                        help='OVERWRITES --mic_used. Does not atempt to connect to external world.')
    parser.add_argument('--no_debug', action='store_false',
                        help='Debug flag that plots data.')
    args = parser.parse_args()

    if vars(args)['function'] == 'tx':
        main_qam_tx(vars(args)['no_debug'], vars(args)[
                    'mic_used'], vars(args)['hw_used'],  vars(args)['dry_run'])
    elif vars(args)['function'] == 'rx':
        main_qam_rx(vars(args)['debug'])
