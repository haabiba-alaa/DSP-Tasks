import numpy as np
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os


def lowpass_filter(n, fc):
    if n == 0:
        return 2 * fc
    n_omega = n * 2 * np.pi * fc
    return 2 * fc * (np.sin(n_omega) / n_omega)


def highpass_filter(n, fc):
    if n == 0:
        return 1 - (2 * fc)
    n_omega = n * 2 * np.pi * fc
    return -2 * fc * (np.sin(n_omega) / n_omega)


def bandpass_filter(n, f1, f2):
    if n == 0:
        return 2 * (f2 - f1)
    n_omega2 = n * 2 * np.pi * f2
    n_omega1 = n * 2 * np.pi * f1
    return 2 * f2 * (np.sin(n_omega2) / n_omega2) - (2 * f1 * (np.sin(n_omega1) / n_omega1))


def bandreject_filter(n, f1, f2):
    if n == 0:
        return 1 - (2 * (f2 - f1))
    n_omega2 = n * 2 * np.pi * f2
    n_omega1 = n * 2 * np.pi * f1
    return 2 * f1 * (np.sin(n_omega1) / n_omega1) - (2 * f2 * (np.sin(n_omega2) / n_omega2))


def rectangular_window(n, N):
    return 1


def hanning_window(n, N):
    return 0.5 + 0.5 * (np.cos(2 * np.pi * n / N))


def hamming_window(n, N):
    return 0.54 + 0.46 * np.cos(2 * np.pi * n / N)


def blackman_window(n, N):
    return 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))


def get_rectangular_window_n(delta_f):
    return round(0.9 / delta_f)


def get_hanning_window_n(delta_f):
    return round(3.1 / delta_f)


def get_hamming_window_n(delta_f):
    return round(3.3 / delta_f)


def get_blackman_window_n(delta_f):
    return round(5.5 / delta_f)


def get_N_based_on_stopband_attenuation(stopband_attenuation, delta_f):
    if stopband_attenuation < 21:
        window_func = rectangular_window
        N = get_rectangular_window_n(delta_f)
    elif stopband_attenuation < 44:
        window_func = hanning_window
        N = get_hanning_window_n(delta_f)
    elif stopband_attenuation < 53:
        window_func = hamming_window
        N = get_hamming_window_n(delta_f)
    else:
        window_func = blackman_window
        N = get_blackman_window_n(delta_f)

    if N % 2 == 0:  # Ensure N is odd
        N += 1

    return N, window_func


def read_filter_specificationsLH(file_path):
    filter_type = None
    fs = None
    stop_band_attenuation = None
    fc = None
    transition_band = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    if key == 'FilterType':
                        filter_type = value
                    elif key == 'FS':
                        fs = int(value)
                    elif key == 'StopBandAttenuation':
                        stop_band_attenuation = int(value)
                    elif key == 'FC':
                        fc = int(value)
                    elif key == 'TransitionBand':
                        transition_band = int(value)
    except FileNotFoundError:
        print("File not found.")

    return filter_type, fs, stop_band_attenuation, fc, transition_band


def read_filter_specificationsB(file_path):
    filter_type = None
    fs = None
    stop_band_attenuation = None
    fc1 = None
    fc2 = None
    transition_band = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    if key == 'FilterType':
                        filter_type = value
                    elif key == 'FS':
                        fs = int(value)
                    elif key == 'StopBandAttenuation':
                        stop_band_attenuation = int(value)
                    elif key == 'F1':
                        fc1 = float(value)
                    elif key == 'F2':
                        fc2 = float(value)
                    elif key == 'TransitionBand':
                        transition_band = int(value)
    except FileNotFoundError:
        print("File not found.")

    return filter_type, fs, stop_band_attenuation, fc1, fc2, transition_band


def load_signal(file_path):
    indices = []
    samples = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                indices.append(int(parts[0]))
                samples.append(float(parts[1]))
    return indices, samples


def convolve_signals(indices1, samples1, indices2, samples2):
    result_indices = []
    result_samples = []

    # Perform the convolution by iterating through each index in the first signal
    for i in range(len(indices1)):
        # Iterate through each index in the second signal
        for j in range(len(indices2)):
            index = indices1[i] + indices2[j]
            sample = samples1[i] * samples2[j]

            # If the index already exists in the result, accumulate the sample
            if index in result_indices:
                result_samples[result_indices.index(index)] += sample
            else:
                result_indices.append(index)
                result_samples.append(sample)

    return result_indices, result_samples


def save_results(indices, samples):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for i in range(len(indices)):
                file.write(f"{indices[i]} {samples[i]}\n")


def plot_signal_in_tkinter(indices, samples):
    plt.figure(figsize=(6, 4))
    plt.plot(indices, samples)
    plt.xlabel('Indices')
    plt.ylabel('Samples')
    plt.title('Convolution Results')
    plt.grid(True)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Signal Plot")

    # Embed the plot into a Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add a button to save the plot
    def save_plot():
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            plt.savefig(file_path)
            plt.close()

    save_button = tk.Button(root, text="Save Plot", command=save_plot)
    save_button.pack()

    # Run the Tkinter main loop
    root.mainloop()


def calc_BPF_coff(sampling_freq, stopband_attenuation, fc1, fc2, transition_width):
    # Step 1: Calculate deltaF and determine the window function and N
    delta_f = transition_width / sampling_freq

    fc1 = (fc1 / sampling_freq) - (delta_f / 2)
    fc2 = (fc2 / sampling_freq) + (delta_f / 2)

    # Choosing window function based on stopband attenuation
    N, window_func = get_N_based_on_stopband_attenuation(stopband_attenuation, delta_f)

    # Generate the filter coefficients and their indices with corrected symmetry
    positive_coefficients = []

    for n in range(0, N // 2 + 1):
        hd_n = bandpass_filter(n, fc1, fc2)
        w_n = window_func(n, N)
        positive_coefficients.append(hd_n * w_n)

    symmetric_coefficients = positive_coefficients[::-1]  # Reverse positive coefficients

    # Combine symmetric coefficients and their absolute counterparts
    all_coefficients = symmetric_coefficients[:-1] + [positive_coefficients[0]] + positive_coefficients[1:]

    # Print the coefficients and their corresponding indices (-26 to 26)
    indices = []
    coefficients = []

    # Populate the lists with indices and coefficients
    for idx, coeff in enumerate(all_coefficients, start=-(N // 2)):
        indices.append(idx)
        coefficients.append(coeff)

    return indices, coefficients


def calc_BSF_coff(sampling_freq, stopband_attenuation, fc1, fc2, transition_width):
    # Step 1: Calculate deltaF and determine the window function and N
    delta_f = transition_width / sampling_freq

    fc1 = (fc1 / sampling_freq) + (delta_f / 2)
    fc2 = (fc2 / sampling_freq) - (delta_f / 2)

    # Choosing window function based on stopband attenuation
    N, window_func = get_N_based_on_stopband_attenuation(stopband_attenuation, delta_f)

    # Generate the filter coefficients and their indices with corrected symmetry
    positive_coefficients = []

    for n in range(0, N // 2 + 1):
        hd_n = bandreject_filter(n, fc1, fc2)
        w_n = window_func(n, N)
        positive_coefficients.append(hd_n * w_n)

    symmetric_coefficients = positive_coefficients[::-1]  # Reverse positive coefficients

    # Combine symmetric coefficients and their absolute counterparts
    all_coefficients = symmetric_coefficients[:-1] + [positive_coefficients[0]] + positive_coefficients[1:]

    # Print the coefficients and their corresponding indices (-26 to 26)
    indices = []
    coefficients = []

    # Populate the lists with indices and coefficients
    for idx, coeff in enumerate(all_coefficients, start=-(N // 2)):
        indices.append(idx)
        coefficients.append(coeff)  # Coefficients without modification

    return indices, coefficients


def calc_LFF_coff(sampling_freq, stopband_attenuation, passband_edge_freq, transition_width):
    delta_f = transition_width / sampling_freq

    fc = (passband_edge_freq / sampling_freq) + (delta_f / 2)

    N, window_func = get_N_based_on_stopband_attenuation(stopband_attenuation, delta_f)
    positive_coefficients = []

    for n in range(0, N // 2 + 1):
        hd_n = lowpass_filter(n, fc)
        w_n = window_func(n, N)
        positive_coefficients.append(hd_n * w_n)

    symmetric_coefficients = positive_coefficients[::-1]  # Reverse positive coefficients

    all_coefficients = symmetric_coefficients[:-1] + [positive_coefficients[0]] + positive_coefficients[1:]

    indices = []
    coefficients = []

    for idx, coeff in enumerate(all_coefficients, start=-(N // 2)):
        indices.append(idx)
        coefficients.append(coeff)

    return indices, coefficients


def calc_HFF_coff(sampling_freq, stopband_attenuation, passband_edge_freq, transition_width):
    # Step 1: Calculate deltaF and determine the window function and N
    delta_f = transition_width / sampling_freq

    fc = (passband_edge_freq / sampling_freq) - (delta_f / 2)

    N, window_func = get_N_based_on_stopband_attenuation(stopband_attenuation, delta_f)

    positive_coefficients = []

    for n in range(0, N // 2 + 1):
        hd_n = highpass_filter(n, fc)
        w_n = window_func(n, N)
        positive_coefficients.append(hd_n * w_n)

    symmetric_coefficients = positive_coefficients[::-1]  # Reverse positive coefficients

    # Combine symmetric coefficients and their absolute counterparts
    all_coefficients = symmetric_coefficients[:-1] + [positive_coefficients[0]] + positive_coefficients[1:]

    # Print the coefficients and their corresponding indices (-26 to 26)
    indices = []
    coefficients = []

    for idx, coeff in enumerate(all_coefficients, start=-(N // 2)):
        indices.append(idx)
        coefficients.append(coeff)
    return indices, coefficients


def Compare_Signals(file_name, Your_indices, Your_samples):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            print("Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one")
            return
    print("Test case passed successfully")


def down_sample(indices, values, M):
    ds_indices = indices[::M]
    ds_values = values[::M]
    new_ds_indices = []
    subtract = int((ds_indices[0] + (ds_indices[-1])) / 2)
    for i in range(ds_indices[0], subtract + 1):
        if i in ds_indices:
            new_ds_indices.append(i)
        else:
            new_ds_indices.append(i)
    return new_ds_indices, ds_values


def up_sample(indices, samples, L):
    up_sampled_indices = []
    up_sampled_samples = []
    current_index = indices[0]  # Starting index

    for i, sample in zip(indices, samples):
        up_sampled_indices.append(current_index)
        up_sampled_samples.append(sample)

        current_index += 1

        for j in range(1, L):
            up_sampled_indices.append(current_index)
            up_sampled_samples.append(0)
            current_index += 1

    return up_sampled_indices, up_sampled_samples


def load_signalTemp(file_path):
    with open(file_path, 'r') as file:
        signal_data = [float(line.strip()) for line in file.readlines()]

    return np.array(signal_data)


def up_down(L, M, resultsInd, resultsSam, fs, stop_band_attenuation, fc, transition_band):
    if M != 0 and L == 0:
        indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
        resultsInd, resultsSam = convolve_signals(resultsInd, resultsSam, indices, coefficients)
        down_sampled_indices, down_sampled_values = down_sample(resultsInd, resultsSam, M)
        return down_sampled_indices, down_sampled_values

    elif M == 0 and L != 0:
        up_sampled_indices, up_sampled_values = up_sample(resultsInd, resultsSam, L)
        indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
        resultsInd, resultsSam = convolve_signals(up_sampled_indices, up_sampled_values, indices, coefficients)
        resultsInd = resultsInd[:-2]
        resultsSam = resultsSam[:-2]
        return resultsInd, resultsSam

    elif M != 0 and L != 0:
        up_sampled_indices, up_sampled_values = up_sample(resultsInd, resultsSam, L)
        indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
        resultsInd, resultsSam = convolve_signals(up_sampled_indices, up_sampled_values, indices, coefficients)
        resultsInd = resultsInd[:-2]
        resultsSam = resultsSam[:-2]
        down_sampled_indices, down_sampled_values = down_sample(resultsInd, resultsSam, M)
        return down_sampled_indices, down_sampled_values


def remove_dc_component(sam):
    if sam:
        average = np.mean(sam)
        dc_removed_signal = [x - average for x in sam]
        return dc_removed_signal


def normalize_plot(indices, samples):
    min_val = min(samples)
    max_val = max(samples)

    normalized_samples = [((2 * (x - min_val)) / (max_val - min_val)) - 1 for x in samples]

    return indices, normalized_samples


def auto_correlation(samples):
    length_samples = len(samples)
    corr = np.zeros(length_samples)

    for shift in range(length_samples):
        for index in range(length_samples):
            corr[shift] += samples[index] * samples[(index + shift) % length_samples]

    norm_corr = corr / (np.linalg.norm(samples) * np.linalg.norm(samples))
    return norm_corr


def compute_dct(input_values):
    input_values = np.array(input_values)
    N = len(input_values)
    output = []
    sqrt = np.sqrt(2.0 / N)

    for k in range(N):
        y_k = 0
        for n in range(N):
            y_k += input_values[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))

        output.append(sqrt * y_k)

    dct_signal = np.array(output)
    return dct_signal


def load_signal_Numpy(file_path):
    return np.load(file_path)


def calculate_average(signal_folder):
    signal_files = os.listdir(signal_folder)
    # Initialize the average signal with the first signal
    average_signal = load_signal_Numpy(os.path.join(signal_folder, signal_files[0]))

    # Sum all signals
    for file in signal_files[1:]:
        signal = load_signal_Numpy(os.path.join(signal_folder, file))
        average_signal += signal

    # Calculate the average
    average_signal /= len(signal_files)
    return average_signal


def classify_signal_Temp(test_signal, average_signal_class1, average_signal_class2):
    correlation_class1 = np.corrcoef(test_signal, average_signal_class1)[0, 1]
    correlation_class2 = np.corrcoef(test_signal, average_signal_class2)[0, 1]

    if correlation_class1 > correlation_class2:
        return "Class A"
    else:
        return "Class B"


def display_results(test_folder, average_signal_class1, average_signal_class2):
    root = tk.Tk()
    root.title("Signal Classification Results")

    test_files = os.listdir(test_folder)
    for file in test_files:
        test_signal = load_signal_Numpy(os.path.join(test_folder, file))

        label = tk.Label(root, text=f"\nTest signal {file}:\n"
                                    f"Correlation with Class A: "
                                    f"{np.corrcoef(test_signal, average_signal_class1)[0, 1]}\n"
                                    f"Correlation with Class B: "
                                    f"{np.corrcoef(test_signal, average_signal_class2)[0, 1]}\n"
                                    f"Classification: {classify_signal_Temp(test_signal, average_signal_class1, average_signal_class2)}"
                         )
        label.pack()

    root.mainloop()
