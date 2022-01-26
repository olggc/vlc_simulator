import json

from numpy.fft import fftfreq, rfft, rfftfreq
from scipy.fft import fft
from sensor import Filter
from scipy.signal import butter, lfilter, sosfilt, sosfreqz, find_peaks

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    data_dir = 'data/'
    output_file_name = 'output.json'
    filter_settings = {'filter_1': {'low_cut': 1500.0,
                                    'high_cut': 2500.0,
                                    'order': 6},
                       'filter_2': {'low_cut': 2500.0,
                                    'high_cut': 3500.0,
                                    'order': 6},
                       'filter_3': {'low_cut': 3500.0,
                                    'high_cut': 4500.0,
                                    'order': 6}}
    with open('data/temporal_results.json') as fp:
        sinal = json.load(fp)
    # Sample rate and desired cutoff frequencies (in Hz).
    plane = [] * (len(sinal.keys()) ** 2)
    output = {f_id: plane.copy() for f_id in filter_settings.keys()}
    fs = 100000.0
    filters = []
    for fil_id in filter_settings.keys():
        filters.append(Filter(filter_parameters=filter_settings[fil_id],
                              sample_rate=fs,
                              filter_id=fil_id))

    for f in filters:
        for a in sinal.keys():
            for b in sinal[a].keys():
                raw_signal = sinal[a][b][:-1]
                y = f.filter_data(raw_signal)
                half = len(y) // 2
                yss = y[half:]
                yf = 2.0 / len(yss) * rfft(yss)
                dt = 1 / fs
                xf = rfftfreq(len(yss), dt)
                plt.plot(xf, np.abs(yf))
                amp = max(abs(yf))
                output[f.filter_id].append(amp)

    with open(data_dir + output_file_name, 'w') as f:
        json.dump(output, f)
