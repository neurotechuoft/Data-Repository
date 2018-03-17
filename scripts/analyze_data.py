import csv
import numpy as np
import matplotlib.pyplot as plt
import biosppy

from sklearn.preprocessing import scale

def bandpower(data, sample_rate, low_freq, high_freq):
    calculated_freqs, power_spectrum = biosppy.tools.\
        power_spectrum(data, sampling_rate=sample_rate, decibel=False)
    return biosppy.tools.band_power(calculated_freqs,
                                    power_spectrum,
                                    [low_freq, high_freq], decibel=False)

def highpass(data, sample_rate, cutoff_freq):
    # Calculate order of filter
    order = int(0.3 * sample_rate)

    # Apply filters
    filtered_data, _, _ = biosppy.tools.filter_signal(signal=data,
                                                      ftype='FIR',
                                                      band='highpass',
                                                      order=order,
                                                      frequency=cutoff_freq,
                                                      sampling_rate=
                                                      sample_rate)

    return filtered_data


def bandpass(data, sample_rate, low_freq, high_freq):
    # Calculate order of filter
    order = int(0.3 * sample_rate)

    # Apply filters
    filtered_data, _, _ = biosppy.tools.filter_signal(signal=data,
                                                      ftype='FIR',
                                                      band='bandpass',
                                                      order=order,
                                                      frequency=[low_freq,
                                                                 high_freq],
                                                      sampling_rate=
                                                      sample_rate)

    return filtered_data


def fill_bandpower(data, time, sample_rate, low_freq, high_freq):
    mu_power_c3 = np.array([])
    c3_packet = np.array([])
    curr_gesture = gesture.item(0)
    for i in range(0, len(time)):
        # Calculate bandpower for packet, and reset packet
        if gesture.item(i) != curr_gesture or i == len(time) - 1:
            power = bandpower(c3_packet, sample_rate, low_freq, high_freq)
            for sample in c3_packet:
                mu_power_c3 = np.append(mu_power_c3, power)
            curr_gesture = gesture.item(i)
            c3_packet = np.array([data.item(i)])
        else:
            # store all vals of the same gesture
            c3_packet = np.append(c3_packet, data.item(i))
    return np.append(mu_power_c3, mu_power_c3.item(-1))

# def fill_bandpower(data, time, sample_rate):
#     mu_power_c3 = np.array([])
#     c3_packet = np.array([])
#     for i in range(0, len(time)):
#         if (i % 512 == 0 and i > 0) or i == len(time) - 1:
#             power = bandpower(c3_packet, sample_rate, 7.0, 13.0)
#             for sample in c3_packet:
#                 mu_power_c3 = np.append(mu_power_c3, power)
#             c3_packet = np.array([data.item(i)])
#         else:
#             c3_packet = np.append(c3_packet, data.item(i))
#     return np.append(mu_power_c3, mu_power_c3.item(-1))


if __name__ == '__main__':
    time = np.array([])
    index = np.array([])
    c4 = np.array([])
    c3 = np.array([])
    gesture = np.array([])

    sample_rate = 256.0

    with open("../eeg/motor-imagery/2018-03-16/karl-exp1-trial1.csv",
    # with open("../eeg/motor-imagery/karl-c3-c4-hand-ext-flex-2018-03-10-round12.csv",
              "r") as \
            data_file:
        data_reader = csv.reader(data_file, delimiter=",", quotechar="|")
        i = 0
        factor = 1
        for row in data_reader:
            # if id < max_id:
            time = np.append(time, [float(row[0])])
            # index = np.append(index, [float(row[1]) + i * 256.0])
            index = np.append(index, [i])
            c3 = np.append(c3, [float(row[4])])
            c4 = np.append(c4, [float(row[5])])
            gesture = np.append(gesture, [float(row[11]) * factor])
            i += 1

    analyze_data = c3
    # analyze_data = np.subtract(analyze_data, np.full((len(analyze_data)), analyze_data.item(0)))
    analyze_data = np.subtract(analyze_data, np.full((len(analyze_data)), np.mean(c3)))

    # cleaned_data = bandpass(highpass(analyze_data, sample_rate, 2), sample_rate, 2.0, 50.0)
    cleaned_data = bandpass(analyze_data, sample_rate, 2.0, 50.0)

    mu = bandpass(cleaned_data, 256.0, 7.0, 13.0)

    mu_power = scale(np.reshape(fill_bandpower(mu, time, sample_rate, 7.0, 13.0), (-1, 1))).ravel()

    # arr = np.array(time, mu_power)

    # print(len(mu_power_c3))
    # print(len(time))
    # print(bandpassed_c3)

    # plt.plot(time, mu_power_c3, 'r--')
    # plt.plot(time, mu_c3, 'r--', time, gesture, 'b--')
    plt.plot(time, cleaned_data, 'g--', time, gesture, 'b--')
    plt.show()
