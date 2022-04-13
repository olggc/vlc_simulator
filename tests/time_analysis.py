import json
from math import floor, log, ceil, sqrt
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fftfreq, rfft, rfftfreq
from scipy.fft import fft
from sensor import Filter
from scipy.signal import butter, lfilter, sosfilt, sosfreqz, find_peaks


def get_nearest_point(result_dict, point):
    def calc_dist(xa, ya, xb, yb):
        return sqrt(((xa - xb) ** 2) + ((ya - yb) ** 2))

    xp, yp = point
    xs = [float(xj) for xj in result_dict.keys()]
    ys = [float(yj) for yj in result_dict[str(xs[0])].keys()]
    all_points = [(xu, yu) for xu in xs for yu in ys]
    all_points = set(all_points)
    dists = [(calc_dist(xi, yi, xp, yp), xi, yi) for xi, yi in all_points]
    d, x_nearest, y_nearest = min(dists, key=lambda dist: dist[0])
    return str(x_nearest), str(y_nearest)


if __name__ == "__main__":

    from scipy.signal import freqz

    plt.rcParams.update({'font.size': 8})
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
    lum_position = [(4 * 0.24, 4 * 0.74),
                    (4 * 0.49, 4 * 0.24),
                    (4 * 0.74, 4 * 0.74)]
    sob_plot_pos = [(321, 322),
                    (323, 324),
                    (325, 326)]
    fig, ax = plt.subplots()
    for l, lum_pos in enumerate(lum_position):
        x, y = get_nearest_point(sinal, lum_pos)
        pos_a, pos_b = sob_plot_pos[l]
        raw_signal = sinal[x][y][:]
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
        plt.subplot(pos_a)
        plt.plot(t[two_thirds:], raw_signal[two_thirds:], 'b')
        plt.title(f'Forma de Onda - Ponto {l + 1}')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Lux',horizontalalignment='right', rotation=0)
        plt.grid(True)
        # plt.axis('tight')

        plt.subplot(pos_b)
        yss = raw_signal[:]
        mean_yss = np.mean(yss)
        yf = (1.0 / len(yss)) * rfft(yss)
        xf = rfftfreq(len(yss), T)
        stop_at = len(xf) // 10
        plt.stem(xf[:stop_at], np.abs(yf[:stop_at]), 'r', markerfmt=" ")
        plt.xlabel('Frequência [Hz]')
        # plt.ylabel('Amplitude [Amp]')
        plt.title(f'Conteúdo Espectral - Ponto {l + 1}')
        plt.grid(True)
    fig.tight_layout()
    plt.show()
    # plt.axis('tight')
    # plt.title('FFT da forma de onda')
    # Plot the frequency response for a few different orders.
    # nsamples = len(raw_signal)
    # K = log(nsamples, 2)
    # if abs((2 ** ceil(K)) - nsamples) > abs((2 ** floor(K)) - nsamples):
    #     K = 2 ** floor(K)
    # else:
    #     K = 2 ** ceil(K)
    # pos = [(423, 424), (425, 426), (427, 428)]
    # position = {filt.filter_id: pos[i] for i, filt in enumerate(filters)}
    # for f in filters:
    #     data_dict = {}
    #     filter_name = filters_names[f.filter_id]
    #     pos_a, pos_b = position[f.filter_id]
    #     sos = f.filter
    #     w, h = sosfreqz(sos, worN=K)
    #     # stop_at = len(w) // 10
    #     # l2 = plt.plot((fs * 0.5 / np.pi) * w[:stop_at + 1],
    #     #               abs(h[:stop_at + 1]),
    #     #               label="Filtro Ordem 6")
    #     # l4 = plt.plot([0, (fs * 0.5 / np.pi) * w[stop_at]], [np.sqrt(0.5), np.sqrt(0.5)],
    #     #               '--', label='sqrt(1/2)')
    #     # plt.xlabel(f'Frequência ({filter_name})')
    #     # plt.ylabel('Amplitude')
    #     # plt.grid(True)
    #     # plt.legend(loc='best')
    #     # plt.show()
    #     # Filtered signal.
    #     y = f.filter_data(raw_signal)
    #     plt.subplot(pos_a)
    #     plt.plot(t[two_thirds:], y[two_thirds:], 'b', label=f'{filter_name}')
    #     # plt.title('Forma de onda e FFT da iluminância')
    #     plt.xlabel('Tempo [s]')
    #     # plt.ylabel('Iluminância [lux]')
    #     plt.grid(True)
    #     plt.legend(loc='upper right')
    #     # plt.axis('tight')
    #
    #     plt.subplot(pos_b)
    #     half = len(y) // 2
    #     yss = y[half:]
    #     yf = (2.0 / len(yss)) * rfft(yss)
    #     xf = rfftfreq(len(yss), T)
    #     stop_at = len(xf) // 10
    #     yfft = np.abs(yf[:stop_at])
    #     yfft[yfft < 0.1 * np.max(yfft)] = 0
    #     plt.stem(xf[:stop_at], yfft, 'r', markerfmt=" ")
    #     plt.xlabel('Frequência [Hz]')
    #     # plt.ylabel('Amplitude [Amp]')
    #     plt.grid(True)
    #     # plt.axis('tight')
    #     # plt.title('FFT da forma de onda')
    #     plt.subplots_adjust(wspace=0.3,
    #                         hspace=1.2)
    # fig.tight_layout()
    # plt.show()
