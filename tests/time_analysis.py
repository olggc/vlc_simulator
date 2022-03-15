import json
from math import floor, log, ceil

from numpy.fft import fftfreq, rfft, rfftfreq
from scipy.fft import fft
from sensor import Filter
from scipy.signal import butter, lfilter, sosfilt, sosfreqz, find_peaks

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    filter_settings = {'filter_1': {'low_cut': 1750.0,
                                    'high_cut': 2250.0,
                                    'order': 6},
                       'filter_2': {'low_cut': 2750.0,
                                    'high_cut': 3250.0,
                                    'order': 6},
                       'filter_3': {'low_cut': 3750.0,
                                    'high_cut': 4250.0,
                                    'order': 6}
                       }
    with open('data/temporal_results.json') as fp:
        sinal = json.load(fp)
    # Sample rate and desired cutoff frequencies (in Hz).
    raw_signal = sinal['0.0']['0.0'][:]
    mean_raw_signal = np.mean(raw_signal)
    fs = 120000.0
    filters = []
    for filter_id in filter_settings.keys():
        filters.append(Filter(filter_parameters=filter_settings[filter_id],
                              sample_rate=fs,
                              filter_id=filter_id))
    filters_names = {'filter_1': '2KHz',
                     'filter_2': '3KHz',
                     'filter_3': '4KHz'}
    # Raw Signal
    T = 1 / fs
    two_thirds = 5 * len(raw_signal) // 6
    nsamples = len(raw_signal)
    t = np.linspace(0, nsamples * T, nsamples, endpoint=False)
    fig, ax = plt.subplots()
    plt.subplot(211)
    plt.plot(t[two_thirds:], raw_signal[two_thirds:], 'b', label='Forma de Onda')
    plt.title('Forma de onda e FFT da iluminância')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Iluminância [lux]')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper right')

    plt.subplot(212)
    yss = raw_signal[:]
    yf = (2.0 / len(yss)) * rfft(yss)
    xf = rfftfreq(len(yss), T)
    stop_at = len(xf) // 10
    plt.stem(xf[:stop_at], np.abs(yf[:stop_at]), 'r', markerfmt=" ", label='FFT')
    plt.xlabel('Frequência [Hz]')
    plt.ylabel('Amplitude [Amp]')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper right')
    # plt.title('FFT da forma de onda')
    plt.subplots_adjust(wspace=0.3,
                        hspace=0.3)
    plt.show()
    # Plot the frequency response for a few different orders.
    nsamples = len(raw_signal)
    K = log(nsamples, 2)
    if abs((2 ** ceil(K)) - nsamples) > abs((2 ** floor(K)) - nsamples):
        K = 2 ** floor(K)
    else:
        K = 2 ** ceil(K)
    for f in filters:
        plt.figure(1)
        plt.clf()
        data_dict = {}
        filter_name = filters_names[f.filter_id]

        sos = f.filter
        w, h = sosfreqz(sos, worN=K)
        # stop_at = len(w) // 10
        # l2 = plt.plot((fs * 0.5 / np.pi) * w[:stop_at + 1],
        #               abs(h[:stop_at + 1]),
        #               label="Filtro Ordem 6")
        # l4 = plt.plot([0, (fs * 0.5 / np.pi) * w[stop_at]], [np.sqrt(0.5), np.sqrt(0.5)],
        #               '--', label='sqrt(1/2)')
        # plt.xlabel(f'Frequência ({filter_name})')
        # plt.ylabel('Amplitude')
        # plt.grid(True)
        # plt.legend(loc='best')
        # plt.show()
        # Filtered signal.
        y = f.filter_data(raw_signal)
        fig1, ax1 = plt.subplots()
        plt.subplot(211)
        plt.plot(t[two_thirds:], y[two_thirds:], 'b', label=f'Sinal de Filtrado - {filter_name}')
        plt.title('Forma de onda e FFT da iluminância')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Iluminância [lux]')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc='upper right')

        plt.subplot(212)
        half = len(y) // 2
        yss = y[half:]
        yf = (2.0 / len(yss)) * rfft(yss)
        xf = rfftfreq(len(yss), T)
        stop_at = len(xf) // 10
        yfft = np.abs(yf[:stop_at])
        yfft[yfft < 0.1 * np.max(yfft)] = 0
        plt.stem(xf[:stop_at], yfft, 'r', markerfmt=" ", label='FFT')
        plt.xlabel('Frequência [Hz]')
        plt.ylabel('Amplitude [Amp]')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc='upper right')
        # plt.title('FFT da forma de onda')
        plt.subplots_adjust(wspace=0.3,
                            hspace=0.3)
        plt.show()
