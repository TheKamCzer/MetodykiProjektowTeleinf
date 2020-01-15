# Metodyki Projektów Teleinformatycznych
Celem projektu jest stworzenie implementacji oprogramowania w środowisku MATLAB/Python do nadawania oraz odbioru wąskopasmowego sygnału audio o modulacji QPSK w czasie rzeczywistym. Projekt ma zostać wykonany w oparciu o moduł nadawczo-odbiorczy ADALM-PLUTO oraz moduł odbiorczy RTL2832u.

## changelog
 - added raised cosine filtration at the QAM modulator
 - added demonstration file which can be executed by `python3 MainQam.py`
    - there is support for microphone and PLUTO SRD (`--mic_used` and `--hw_used` respectively)

