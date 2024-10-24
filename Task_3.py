import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


def execute_task_3():
    def create_new_window(fig):
        new_window = tk.Toplevel(root)
        new_window.title("Plots")

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def read_file(filename):
        x = []
        y = []
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    x.append(float(parts[0]))
                    y.append(float(parts[1]))
        return x, y

    def quantize_and_encode(signal, num_bits):
        min_val = min(signal)
        max_val = max(signal)
        step_size = (max_val - min_val) / (2 ** num_bits)
        encoded_signal = []
        midpoints = []

        for value in signal:
            quantized_value = int((value - min_val) / step_size)
            if quantized_value >= 2 ** num_bits:
                quantized_value = 2 ** num_bits - 1  # Set to the maximum code
            binary_code = format(quantized_value, f'0{num_bits}b')
            encoded_signal.append(binary_code)

            # Calculate and append the midpoint value
            midpoint = min_val + (quantized_value + 0.5) * step_size
            midpoints.append(round(midpoint, 2))

        return encoded_signal, midpoints

    def QuantizationTest1(file_name, Your_EncodedValues, Your_QuantizedValues):
        expectedEncodedValues = []
        expectedQuantizedValues = []
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
                    V2 = str(L[0])
                    V3 = float(L[1])
                    expectedEncodedValues.append(V2)
                    expectedQuantizedValues.append(V3)
                    line = f.readline()
                else:
                    break
        if ((len(Your_EncodedValues) != len(expectedEncodedValues)) or (
                len(Your_QuantizedValues) != len(expectedQuantizedValues))):
            print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_EncodedValues)):
            if Your_EncodedValues[i] != expectedEncodedValues[i]:
                print(
                    "QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                return
        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one")
                return
        print("QuantizationTest1 Test case passed successfully")

    def bits():
        def load_files():
            file_path1 = filedialog.askopenfilename(title="Load Input Data")
            if not file_path1:
                return
            data1 = read_file(file_path1)

            file_path2 = filedialog.askopenfilename(title="Load Expected Output Data")
            if not file_path2:
                return
            data2 = read_file(file_path2)

            if data1 is not None and data2 is not None:
                x1, y1 = data1
                x2, y2 = data2

                num_bits = simpledialog.askinteger("Number of Bits", "Enter the number of bits:")
                if num_bits is None:
                    return

                encoded_values, quantized_y = quantize_and_encode(y1, num_bits)

                QuantizationTest1(file_path2, encoded_values, quantized_y)

                fig = plt.figure(figsize=(6, 4))
                ax = fig.add_subplot(111)
                ax.plot(x1, y1, label='Input', color='blue')
                ax.plot(x1, quantized_y, label='Quantized', color='red')
                ax.set_title("Original and Quantized Signals")
                ax.legend()

                create_new_window(fig)

        load_files()

    def quantize_and_encode_y_with_index(y, num_levels):
        # Calculate the range of the signal
        signal_range = max(y) - min(y)

        # Calculate the step size for quantization
        step_size = signal_range / num_levels

        # Initialize lists to store the results
        interval_index = []
        encoded_value = []
        quantized_value = []
        error = []

        # Quantization and encoding
        for value in y:
            index = min(int((value - min(y)) / step_size), num_levels - 1)  # Limit the index to the maximum level
            encoded = format(index, f'0{int(np.log2(num_levels))}b')
            midpoint = min(y) + (index + 0.5) * step_size
            error_value = midpoint - value

            interval_index.append(index + 1)
            encoded_value.append(encoded)
            quantized_value.append(midpoint)
            error.append(round(error_value, 3))
        return interval_index, encoded_value, quantized_value, error

    def QuantizationTest2(file_name, Your_IntervalIndices, Your_EncodedValues, Your_QuantizedValues, Your_SampledError):
        expectedIntervalIndices = []
        expectedEncodedValues = []
        expectedQuantizedValues = []
        expectedSampledError = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 4:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = str(L[1])
                    V3 = float(L[2])
                    V4 = float(L[3])
                    expectedIntervalIndices.append(V1)
                    expectedEncodedValues.append(V2)
                    expectedQuantizedValues.append(V3)
                    expectedSampledError.append(V4)
                    line = f.readline()
                else:
                    break
        if (len(Your_IntervalIndices) != len(expectedIntervalIndices)
                or len(Your_EncodedValues) != len(expectedEncodedValues)
                or len(Your_QuantizedValues) != len(expectedQuantizedValues)
                or len(Your_SampledError) != len(expectedSampledError)):
            print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
            return
        for i in range(len(Your_IntervalIndices)):
            if Your_IntervalIndices[i] != expectedIntervalIndices[i]:
                print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(Your_EncodedValues)):
            if Your_EncodedValues[i] != expectedEncodedValues[i]:
                print(
                    "QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one")
                return

        for i in range(len(expectedQuantizedValues)):
            if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one")
                return
        for i in range(len(expectedSampledError)):
            if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
                continue
            else:
                print(
                    "QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
                return
        print("QuantizationTest2 Test case passed successfully")

    def levels():
        def load_files():
            file_path1 = filedialog.askopenfilename(title="Load Input Data")
            if not file_path1:
                return
            data1 = read_file(file_path1)

            file_path2 = filedialog.askopenfilename(title="Load Expected Output Data")
            if not file_path2:
                return
            data2 = read_file(file_path2)

            if data1 is not None:
                x1, y1 = data1

                num_levels = simpledialog.askinteger("Number of levels", "Enter the number of levels:")
                if num_levels is None:
                    return

                interval_index, encoded_value, quantized_value, error = quantize_and_encode_y_with_index(y1, num_levels)

                QuantizationTest2(file_path2, interval_index, encoded_value, quantized_value, error)

                fig = plt.figure(figsize=(6, 4))
                ax = fig.add_subplot(111)
                ax.plot(x1, y1, label='Input', color='blue')
                ax.plot(x1, quantized_value, label='Quantized', color='red')
                ax.set_title("Original and Quantized Signals")
                ax.legend()

                create_new_window(fig)

        load_files()

    root = tk.Tk()
    root.geometry("220x80")
    root.title("Signal Quantization")

    menu_frame = tk.Frame(root)
    menu_frame.pack()

    bits_button = tk.Button(menu_frame, text="Bits", command=bits)
    bits_button.pack()

    bits_button = tk.Button(menu_frame, text="Levels", command=levels)
    bits_button.pack()

    root.mainloop()
