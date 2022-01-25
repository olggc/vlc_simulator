import json

from numpy.fft import fftfreq, rfft, rfftfreq
from scipy.fft import fft
from sensor import Filter
from scipy.signal import butter, lfilter, sosfilt, sosfreqz, find_peaks

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    filter_settings = {'filter_1': {'low_cut': 1500.0,
                                    'high_cut': 2500.0,
                                    'order': 6},
                       'filter_2': {'low_cut': 2500.0,
                                    'high_cut': 3500.0,
                                    'order': 6},
                       'filter_3': {'low_cut': 3500.0,
                                    'high_cut': 4500.0,
                                    'order': 6}}
    with open('temporal_results.json') as fp:
        sinal = json.load(fp)
    # Sample rate and desired cutoff frequencies (in Hz).
    raw_signal = sinal[str(0.0)][str(0.0)][:-1]
    fs = 100000.0
    filters = []
    for filter_id in filter_settings.keys():
        filters.append(Filter(filter_parameters=filter_settings[filter_id],
                              sample_rate=fs,
                              filter_id=filter_id))

    # Plot the frequency response for a few different orders.
    for f in filters:
        plt.figure(1)
        plt.clf()
        for order in [3, 6, 9]:
            sos = f.filter
            w, h = sosfreqz(sos, worN=2000)
            plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

        plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
                 '--', label='sqrt(0.5)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.grid(True)
        plt.legend(loc='best')

        # Filter a noisy signal.
        T = 0.005
        nsamples = len(raw_signal)
        t = np.linspace(0, T, nsamples, endpoint=False)
        plt.figure(2)
        plt.clf()
        plt.plot(t, raw_signal, label='Noisy signal')

        y = f.filter_data(raw_signal)
        plt.plot(t, y, label='Filtered signal (Hz)')
        plt.xlabel('time (seconds)')
        # plt.hlines([-a, a], 0, T, linestyles='--')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc='upper left')

        plt.show()
        half = len(y) // 2
        yss = y[half:]
        yf = 2.0 / len(yss) * rfft(yss)
        dt = 1 / fs
        xf = rfftfreq(len(yss), dt)
        plt.plot(xf, np.abs(yf))
        amp = abs(yss)
        peaks, _ = find_peaks(amp)
        amp = sum([abs(yss[peak]) for peak in peaks]) / len(peaks)
        amp2 = max(yss)
        amp3 = max(abs(yf))
        plt.grid()

        plt.show()
