import tkinter as tk
from tkinter import filedialog
import numpy as np


def execute_task_8():
    def Req1():
        def cyclic(signal):
            NewSignal = []
            N = len(signal)
            for i in range(N):
                permuted = np.roll(signal, -i)
                NewSignal.append(permuted)
            return NewSignal

        def normalized_cross_correlation(signal1, signal2):
            N = len(signal1)
            if len(signal2) != N:
                raise ValueError("Both signals must be of equal length")

            normalized_corr = np.zeros(N)
            signal2_cyclic = cyclic(signal2)

            for i, cyclic_signal in enumerate(signal2_cyclic):
                cross_corr = np.sum(np.multiply(signal1, cyclic_signal))
                normalization_factor = np.sqrt(np.sum(np.square(signal1)) * np.sum(np.square(cyclic_signal)))
                normalized_corr[i] = cross_corr / normalization_factor

            return normalized_corr

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

            corr_samples = normalized_cross_correlation(samples1, samples2)

            # Validate convolution result using ConvTest function
            file_path3 = filedialog.askopenfilename(title="Load Output", filetypes=[("Text files", "*.txt")])
            if not file_path2:
                return
            Compare_Signals(file_path3, indices2, corr_samples)
            # print("Indices Result: ", convolved_indices)
            # print("Normalized Correlation: ", convolved_samples)

        root = tk.Tk()
        root.title("Direct Method Cross-Correlation")
        root.geometry("200x50")
        load_button = tk.Button(root, text="Load Signals", command=load_files)
        load_button.pack()

        root.mainloop()

    def Req2():
        def custom_dft(signal):
            N = len(signal)
            n = np.arange(N)
            k = n.reshape((N, 1))
            factor = np.exp(-2j * np.pi * k * n / N)
            return np.dot(factor, signal)

        def custom_idft(signal):
            N = len(signal)
            n = np.arange(N)
            k = n.reshape((N, 1))
            factor = np.exp(2j * np.pi * k * n / N)
            return np.dot(factor, signal) / N

        def zero_pad(signal, length):
            signal_padded = np.zeros(length)
            signal_padded[:len(signal)] = signal
            return signal_padded

        def fast_convolution(signal1_indices, signal1_samples, signal2_indices, signal2_samples):
            # Combine indices and samples into a single complex array
            combined_indices = np.array(signal1_indices + signal2_indices)
            combined_samples = np.array(signal1_samples + signal2_samples)

            # Calculate the size of the resulting convolved array
            conv_size = len(signal1_indices) + len(signal2_indices) - 1

            # Zero-pad both signals to match convolution size
            signal1_padded = zero_pad(signal1_samples, conv_size)
            signal2_padded = zero_pad(signal2_samples, conv_size)

            # Perform DFT for both input signals
            dft_signal1 = custom_dft(signal1_padded)
            dft_signal2 = custom_dft(signal2_padded)

            # Multiply the DFTs point-wise
            convolution_result = dft_signal1 * dft_signal2

            # Perform IDFT
            inverse_convolution = custom_idft(convolution_result)

            # Create the expected indices list
            expected_indices = np.arange(min(combined_indices), max(combined_indices) + 2)

            # Extracting indices and samples of the resulting convolution
            result_indices = expected_indices
            result_samples = np.round(np.real(inverse_convolution)).astype(int).tolist()

            return result_indices, result_samples

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

        def ConvTest(Your_indices, Your_samples):
            """
            Test inputs
            InputIndicesSignal1 =[-2, -1, 0, 1]
            InputSamplesSignal1 = [1, 2, 1, 1 ]

            InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
            InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
            """

            expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
            expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]
            print(Your_indices)
            print(Your_samples)
            if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
                print("Conv Test case failed, your signal have different length from the expected one")
                return
            for i in range(len(Your_indices)):
                if Your_indices[i] != expected_indices[i]:
                    print("Conv Test case failed, your signal have different indicies from the expected one")
                    return
            for i in range(len(expected_samples)):
                if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                    continue
                else:
                    print("Conv Test case failed, your signal have different values from the expected one")
                    return
            print("Conv Test case passed successfully")

        def load_files():
            file_path1 = filedialog.askopenfilename(title="Load Input Signal 1", filetypes=[("Text files", "*.txt")])
            if not file_path1:
                return
            indices1, samples1 = load_signal(file_path1)

            file_path2 = filedialog.askopenfilename(title="Load Input Signal 2", filetypes=[("Text files", "*.txt")])
            if not file_path2:
                return
            indices2, samples2 = load_signal(file_path2)

            conv_ind, conv_samples = fast_convolution(indices1, samples1, indices2, samples2)

            ConvTest(conv_ind, conv_samples)

        root = tk.Tk()
        root.title("Fast Convolution.")
        root.geometry("200x50")
        load_button = tk.Button(root, text="Load Signals", command=load_files)
        load_button.pack()

        root.mainloop()

    root = tk.Tk()
    root.geometry("170x110")
    root.title("Task 8")

    menu_frame = tk.Frame(root)
    menu_frame.pack()
    task_1_button = tk.Button(menu_frame, text="Correlation", command=Req1)
    task_1_button.pack()

    task_2_button = tk.Button(menu_frame, text="Convolution", command=Req2)
    task_2_button.pack()

    root.mainloop()

