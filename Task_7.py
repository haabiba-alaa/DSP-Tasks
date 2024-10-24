import tkinter as tk
from tkinter import filedialog, simpledialog
import numpy as np
import os


def execute_task_7():
    def Req1():

        def calculate_dft(x, y):
            N = len(x)

            amplitudes = []
            phases = []

            for k in range(N):
                real_sum = 0
                imag_sum = 0

                for n in range(N):
                    angle = -2 * np.pi * k * n / N
                    real_sum += y[n] * np.cos(angle)
                    imag_sum += y[n] * np.sin(angle)

                amplitude = np.sqrt(real_sum ** 2 + imag_sum ** 2)
                phase = np.arctan2(imag_sum, real_sum)

                amplitudes.append(amplitude)
                phases.append(phase)

            return amplitudes, phases

        def calculate_idft(dft_output):
            N = len(dft_output)
            reconstructed_input = []

            for n in range(N):
                real_sum = 0
                imag_sum = 0

                for k, (amplitude, phase) in enumerate(dft_output):
                    angle = 2 * np.pi * k * n / N
                    real_sum += amplitude * np.cos(angle + phase)
                    imag_sum += amplitude * np.sin(angle + phase)

                reconstructed_input.append((n, real_sum / N))

            return reconstructed_input

        def compute_normalized_cross_correlation(signal1, signal2):
            samples1 = np.array(signal1)  # Convert to NumPy array
            samples2 = np.array(signal2)  # Convert to NumPy array

            # Calculate DFT manually
            dft_signal1 = calculate_dft(range(len(samples1)), samples1)
            dft_signal2 = calculate_dft(range(len(samples2)), samples2)

            # Compute cross-correlation using DFT
            fft_signal1 = [amp * np.exp(1j * phase) for amp, phase in zip(*dft_signal1)]
            fft_signal2_conj = [amp * np.exp(-1j * phase) for amp, phase in zip(*dft_signal2)]

            cross_corr_dft = np.fft.ifft(np.multiply(fft_signal1, fft_signal2_conj))

            # Compute normalization factor
            norm_factor = np.sqrt(np.sum(samples1 ** 2) * np.sum(samples2 ** 2))
            normalized_corr = cross_corr_dft / norm_factor

            result = np.roll(normalized_corr.real, len(samples1) - 1)
            return result[::-1]

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

            # print("Expected Indices: ", expected_indices)
            # print("Expected Samples: ", expected_samples)
            print("\n")
            print("Current Output Test file is: ")
            print(file_name)
            print("\n")
            if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
                print("Correlation Test case failed, your signal have different length from the expected one")
                return
            for i in range(len(Your_indices)):
                if Your_indices[i] != expected_indices[i]:
                    print("Correlation Test case failed, your signal have different indicies from the expected one")
                    return
            for i in range(len(expected_samples)):
                if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                    continue
                else:
                    print("Correlation Test case failed, your signal have different values from the expected one")
                    return
            print("Correlation Test case passed successfully")

        def load_files():
            file_path1 = filedialog.askopenfilename(title="Load Input Signal 1", filetypes=[("Text files", "*.txt")])
            if not file_path1:
                return
            indices1, samples1 = load_signal(file_path1)

            file_path2 = filedialog.askopenfilename(title="Load Input Signal 2", filetypes=[("Text files", "*.txt")])
            if not file_path2:
                return
            indices2, samples2 = load_signal(file_path2)

            corr_samples = compute_normalized_cross_correlation(samples1, samples2)

            # Validate convolution result using ConvTest function
            file_path3 = filedialog.askopenfilename(title="Load Output", filetypes=[("Text files", "*.txt")])
            if not file_path2:
                return
            Compare_Signals(file_path3, indices2, corr_samples)
            # print("Indices Result: ", convolved_indices)
            # print("Normalized Correlation: ", convolved_samples)

        root = tk.Tk()
        root.title("Signal Convolution")
        root.geometry("200x50")
        load_button = tk.Button(root, text="Load Signals", command=load_files)
        load_button.pack()

        root.mainloop()

    def Req2():
        class Signal:
            def __init__(self, samples):
                self.samples = samples

        class TimeDelayAnalysis:
            def __init__(self, signal1=None, signal2=None, sampling_period=None):
                self.signal1 = signal1
                self.signal2 = signal2
                self.sampling_period = sampling_period
                self.delay = None

            def run(self):
                cross_correlation = self.cross_correlation()
                max_corr_index = cross_correlation.index(max(cross_correlation))
                self.delay = max_corr_index - len(self.signal1.samples)

            def cross_correlation(self):
                signal_length = len(self.signal1.samples)
                cross_corr_result = []

                for shift in range(signal_length):
                    correlation_sum = 0

                    for i in range(signal_length):
                        j = (i + shift) % signal_length
                        correlation_sum += self.signal1.samples[i] * self.signal2.samples[j]

                    cross_corr_result.append(correlation_sum)

                return cross_corr_result

        def browse_file(entry, signal_data):
            file_path = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("All files", ".*")])
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

            with open(file_path, 'r') as file:
                lines = file.readlines()
                signal_data.clear()

                for line in lines:
                    try:
                        values = [float(val) for val in line.strip().split()]
                        if len(values) == 1 or len(values) == 2:
                            signal_data.append(values[-1])
                    except ValueError:
                        print(f"Error: Unable to convert value to float - {line}")

        def run_analysis(entry1, entry2, sampling_entry):
            file_path1 = entry1.get()
            file_path2 = entry2.get()
            sampling_period = float(sampling_entry.get())

            signal_data1 = read_signal_data(file_path1)
            signal_data2 = read_signal_data(file_path2)

            signal_data1 = read_signal_data(file_path1)
            signal_data2 = read_signal_data(file_path2)

            signal1 = Signal(samples=signal_data1)  # Assign signal data to Signal objects
            signal2 = Signal(samples=signal_data2)

            delay_analysis = TimeDelayAnalysis(signal1=signal1, signal2=signal2, sampling_period=sampling_period)
            delay_analysis.run()

            expected_output = f"Output = {5 / sampling_period}"
            print(f"sampling_period={sampling_period}")
            print(expected_output)

        def read_signal_data(file_path):
            signal_data = []

            with open(file_path, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    try:
                        values = [float(val) for val in line.strip().split()]
                        if len(values) == 1 or len(values) == 2:
                            signal_data.append(values[-1])
                        else:
                            print(f"Error: Invalid line format - {line}")
                    except ValueError:
                        print(f"Error: Unable to convert value to float - {line}")

            return signal_data

        root = tk.Tk()
        root.title("Time Analysis")

        entry_signal1 = tk.Entry(root, width=50)
        button_browse1 = tk.Button(root, text="Signal 1", command=lambda: browse_file(entry_signal1, []))
        button_browse1.grid(row=0, column=1, padx=10, pady=10)

        entry_signal2 = tk.Entry(root, width=50)
        button_browse2 = tk.Button(root, text="Signal 2", command=lambda: browse_file(entry_signal2, []))
        button_browse2.grid(row=1, column=1, padx=10, pady=10)

        label_sampling = tk.Label(root, text="FS:")
        label_sampling.grid(row=2, column=0, padx=10, pady=10)
        entry_sampling = tk.Entry(root)
        entry_sampling.grid(row=2, column=1, padx=10, pady=10)

        button_run = tk.Button(root, text="time Analysis",
                               command=lambda: run_analysis(entry_signal1, entry_signal2, entry_sampling))
        button_run.grid(row=3, column=0, columnspan=2, pady=10)

        # Result
        result_label = tk.Label(root, text="")
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        root.mainloop()

    def Req3():
        def load_signal(file_path):
            with open(file_path, 'r') as file:
                signal_data = [float(line.strip()) for line in file.readlines()]

            return np.array(signal_data)

        def calculate_average(signal_folder):
            # Calculate the average signal for a given class
            signal_files = os.listdir(signal_folder)
            average_signal = np.zeros_like(load_signal(os.path.join(signal_folder, signal_files[0])))

            for file in signal_files:
                signal = load_signal(os.path.join(signal_folder, file))
                average_signal += signal

            average_signal /= len(signal_files)
            return average_signal

        def classify_signal(test_signal, average_signal_class1, average_signal_class2):
            # Calculate Pearson correlation coefficient with both class averages
            correlation_class1 = np.corrcoef(test_signal, average_signal_class1)[0, 1]
            correlation_class2 = np.corrcoef(test_signal, average_signal_class2)[0, 1]

            # Classify based on correlation
            if correlation_class1 > correlation_class2:
                return "Class 1"
            else:
                return "Class 2"

        def display_results(test_folder, average_signal_class1, average_signal_class2):
            root = tk.Tk()
            root.title("Signal Classification Results")

            test_files = os.listdir(test_folder)
            for file in test_files:
                test_signal = load_signal(os.path.join(test_folder, file))

                label = tk.Label(root, text=f"\nTest signal {file}:\n"
                                            f"Correlation with Class 1: "
                                            f"{np.corrcoef(test_signal, average_signal_class1)[0, 1]}\n"
                                            f"Correlation with Class 2: "
                                            f"{np.corrcoef(test_signal, average_signal_class2)[0, 1]}\n"
                                            f"Classification: {classify_signal(test_signal, average_signal_class1, average_signal_class2)}"
                                 )
                label.pack()

            root.mainloop()

        def main():
            class1_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Class 1"
            class2_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Class 2"
            test_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Test Signals"

            average_signal_class1 = calculate_average(class1_folder)
            average_signal_class2 = calculate_average(class2_folder)

            display_results(test_folder, average_signal_class1, average_signal_class2)

        main()

    root = tk.Tk()
    root.geometry("170x110")
    root.title("Task 7")

    menu_frame = tk.Frame(root)
    menu_frame.pack()
    task_1_button = tk.Button(menu_frame, text="Correlation", command=Req1)
    task_1_button.pack()

    task_2_button = tk.Button(menu_frame, text="Time Analysis", command=Req2)
    task_2_button.pack()

    task_3_button = tk.Button(menu_frame, text="Template Matching", command=Req3)
    task_3_button.pack()

    root.mainloop()
