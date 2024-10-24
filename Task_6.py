import tkinter as tk
from tkinter import filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from tkinter import messagebox
import numpy as np


def execute_task_6():
    def Req1():
        def smoothing(input_signal, input_window_size):
            avr = input_window_size // 2
            out_samples = []
            count = 0

            for i in range(avr, len(input_signal) - avr):
                window_sum = sum(input_signal[count: count + input_window_size])
                result = window_sum / input_window_size
                out_samples.append(result)
                count += 1

            return out_samples

        def browse_file():
            nonlocal file_path
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if file_path:
                entry_window_size.config(state='normal')  # Enable entry for window size

        def plot_graphs():
            if file_path:
                with open(file_path, 'r') as file:
                    input_signal = [float(value) for line in file.readlines() for value in line.split() if
                                    value.strip()]

                    window_size = int(entry_window_size.get()) if entry_window_size.get() else 3  # Default window size
                    smoothed_signal = smoothing(input_signal, window_size)

                    plot_window = tk.Toplevel(root)
                    plot_window.title("Signal Plots")

                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

                    ax1.plot(input_signal, label='Original Signal')
                    ax1.legend()
                    ax1.set_title('Original Signal')

                    ax2.plot(smoothed_signal, label='Smoothed Signal', color='orange')
                    ax2.legend()
                    ax2.set_title('Smoothed Signal')

                    canvas = FigureCanvasTkAgg(fig, master=plot_window)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root = tk.Tk()
        root.title("Signal Smoothing")

        file_path = None

        browse_button = tk.Button(root, text="Load Signal Data", command=browse_file)
        browse_button.pack()

        label_window_size = tk.Label(root, text="Input Window Size (optional):")
        label_window_size.pack()

        entry_window_size = tk.Entry(root, state='disabled')
        entry_window_size.pack()

        plot_button = tk.Button(root, text="Plot Graphs", command=plot_graphs)
        plot_button.pack()

        root.mainloop()

    def Req2():
        def DerivativeSignal():
            InputSignal = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0,
                           18.0,
                           19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0,
                           34.0,
                           35.0,
                           36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0,
                           51.0,
                           52.0,
                           53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0,
                           68.0,
                           69.0,
                           70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0,
                           85.0,
                           86.0,
                           87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0,
                           100.0]  # InputSignal truncated for brevity

            expectedOutput_first = [1] * (len(InputSignal) - 1)  # Expected output for the first derivative

            expectedOutput_second = [0] * (len(InputSignal) - 2)  # Expected output for the second derivative

            # Compute first derivative using finite differences
            FirstDrev = [InputSignal[i + 1] - InputSignal[i] for i in range(len(InputSignal) - 1)]

            # Compute second derivative using finite differences
            SecondDrev = [FirstDrev[i + 1] - FirstDrev[i] for i in range(len(FirstDrev) - 1)]

            """
            Testing your Code
            """
            if (len(FirstDrev) != len(expectedOutput_first)) or (len(SecondDrev) != len(expectedOutput_second)):
                return "Mismatch in length"

            for i in range(len(expectedOutput_first)):
                if abs(FirstDrev[i] - expectedOutput_first[i]) >= 0.01:
                    return "1st derivative is wrong"

            for i in range(len(expectedOutput_second)):
                if abs(SecondDrev[i] - expectedOutput_second[i]) >= 0.01:
                    return "2nd derivative is wrong"

            return "Derivative test case passed successfully"

        def show_result():
            result = DerivativeSignal()
            messagebox.showinfo("Result", result)

        root = tk.Tk()
        root.title("Derivative Test")

        btn = tk.Button(root, text="Derivative Test", command=show_result, height=1, width=10, font=("Arial", 12))
        btn.pack(pady=20)

        root.mainloop()

    def Req3():
        def shift_indices(indices, shift_amount):
            shifted_indices = []
            for index in indices:
                shifted_index = index + shift_amount
                shifted_indices.append(shifted_index)
            return shifted_indices

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

        def browse_file():
            nonlocal file_path
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if file_path:
                entry_shift_steps.config(state='normal')  # Enable entry for shift steps

        def plot_graphs():
            if file_path:
                x_values, y_values = read_file(file_path)

                shift_steps = int(entry_shift_steps.get()) if entry_shift_steps.get() else 0  # Default shift steps
                shifted_indices = shift_indices(x_values, shift_steps)

                plot_window = tk.Toplevel(root)
                plot_window.title("Signal Plots")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

                ax1.plot(x_values, y_values, label='Original Signal')
                ax1.legend()
                ax1.set_title('Original Signal')

                ax2.plot(shifted_indices, y_values, label=f'Shifted Signal by {shift_steps} steps', color='green')
                ax2.legend()
                ax2.set_title('Shifted Signal')

                canvas = FigureCanvasTkAgg(fig, master=plot_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root = tk.Tk()
        root.title("Signal Shifting")

        file_path = None

        browse_button = tk.Button(root, text="Load Signal Data", command=browse_file)
        browse_button.pack()

        label_shift_steps = tk.Label(root, text="Shift Steps:")
        label_shift_steps.pack()

        entry_shift_steps = tk.Entry(root, state='disabled')
        entry_shift_steps.pack()

        plot_button = tk.Button(root, text="Plot Graphs", command=plot_graphs)
        plot_button.pack()

        root.mainloop()

    def Req4():
        def fold_signal(input_signal):
            folded_signal = list(reversed(input_signal))
            return folded_signal

        def browse_file():
            nonlocal file_path
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if file_path:
                plot_graphs()

        def plot_graphs():
            if file_path:
                with open(file_path, 'r') as file:
                    lines = file.readlines()[3:]  # Skip the first 3 lines
                    input_signal = [float(value) for line in lines for value in line.split() if value.strip()]

                    folded_signal = fold_signal(input_signal)

                    plot_window = tk.Toplevel(root)
                    plot_window.title("Signal Plots")

                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

                    ax1.plot(input_signal, label='Original Signal')
                    ax1.legend()
                    ax1.set_title('Original Signal')

                    ax2.plot(folded_signal, label='Folded Signal', color='green')
                    ax2.legend()
                    ax2.set_title('Folded Signal')

                    canvas = FigureCanvasTkAgg(fig, master=plot_window)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    # Show the plot window
                    plot_window.mainloop()

        root = tk.Tk()
        root.title("Signal Folding")

        file_path = None

        browse_button = tk.Button(root, text="Load Signal Data", command=browse_file)
        browse_button.pack()

        plot_button = tk.Button(root, text="Plot Graphs", command=plot_graphs)
        plot_button.pack()

        root.mainloop()

    def Req5():
        def shift_indices(indices, shift_amount):
            shifted_indices = []
            for index in indices:
                shifted_index = index + shift_amount
                shifted_indices.append(shifted_index)
            return shifted_indices

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

        def fold_signal(signal):
            return signal[::-1]

        def Shift_Fold_Signal(file_name, Your_indices, Your_samples):
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
                print("Shift_Fold_Signal Test case failed, your signal has a different length from the expected one")
                return False
            for i in range(len(Your_indices)):
                if Your_indices[i] != expected_indices[i]:
                    print("Shift_Fold_Signal Test case failed, your signal has different indices from the expected one")
                    return False
            for i in range(len(expected_samples)):
                if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                    continue
                else:
                    print("Shift_Fold_Signal Test case failed, your signal has different values from the expected one")
                    return False
            print("Shift_Fold_Signal Test case passed successfully")
            return True

        # Function to handle file processing and shifting
        def process_file():
            def load_files():
                file_path1 = filedialog.askopenfilename(title="Load Input Data", filetypes=[("Text files", "*.txt")])
                if not file_path1:
                    return
                data1 = read_file(file_path1)

                file_path2 = filedialog.askopenfilename(title="Load Expected Output Data",
                                                        filetypes=[("Text files", "*.txt")])
                if not file_path2:
                    return
                data2 = read_file(file_path2)

                if data1 is not None and data2 is not None:
                    x1, y1 = data1
                    x2, y2 = data2

                    num_steps = simpledialog.askinteger("Step Number", "Enter the number of steps to shift:")
                    if num_steps is None:
                        return

                    shifted_indices = shift_indices(x1, num_steps)

                    # Fold the values
                    folded_values = fold_signal(y1)

                    # Compare results with the expected output file
                    success = Shift_Fold_Signal(file_path2, shifted_indices, folded_values)
                    if success:
                        tk.messagebox.showinfo("Test Result", "Shift and fold test passed successfully!")
                    else:
                        tk.messagebox.showwarning("Test Result", "Shift and fold test failed!")

            root = tk.Tk()
            root.title("Signal Shifting and Folding")
            root.geometry("200x50")

            load_button = tk.Button(root, text="Load Data", command=load_files)
            load_button.pack()

            root.mainloop()

        process_file()

    def Req6():
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

        # Define functions for DFT, removing DC component, and IDFT
        def calculate_dft(signal):
            N = len(signal)
            amplitudes = []
            phases = []

            for k in range(N):
                real_sum = sum(signal[n] * np.cos(-2 * np.pi * k * n / N) for n in range(N))
                imag_sum = sum(signal[n] * np.sin(-2 * np.pi * k * n / N) for n in range(N))

                amplitude = np.sqrt(real_sum ** 2 + imag_sum ** 2)
                phase = np.arctan2(imag_sum, real_sum)

                amplitudes.append(amplitude)
                phases.append(phase)

            return amplitudes, phases

        def remove_dc_component(amplitudes):
            amplitudes[0] = 0  # DC component corresponds to index 0, setting it to 0
            return amplitudes

        def calculate_idft(amplitudes, phases):
            N = len(amplitudes)
            reconstructed_signal = []

            for n in range(N):
                real_sum = sum(amplitudes[k] * np.cos(2 * np.pi * k * n / N + phases[k]) for k in range(N))
                reconstructed_signal.append(real_sum / N)

            return reconstructed_signal

        # Function to load data and perform DFT, remove DC component, and IDFT
        def process_signal():
            file_path = filedialog.askopenfilename(title="Load Signal Data")
            if not file_path:
                return

            data = read_file(file_path)
            if data is not None:
                x, signal = data
                amplitudes, phases = calculate_dft(signal)
                amplitudes_no_dc = remove_dc_component(amplitudes)
                reconstructed_signal = calculate_idft(amplitudes_no_dc, phases)

                result_window = tk.Toplevel()
                result_window.title("Reconstructed Signal")

                # Display reconstructed signal in a text widget
                text_widget = tk.Text(result_window)
                text_widget.pack()

                # Insert reconstructed signal values into the text widget
                for idx, value in enumerate(reconstructed_signal):
                    text_widget.insert(tk.END, f"{idx} {value}\n")

        # Rest of the code for the tkinter GUI setup
        root = tk.Tk()
        root.title("Req6")
        root.geometry("200x50")
        process_button = tk.Button(root, text="Remove DC Component", command=process_signal)
        process_button.pack()

        root.mainloop()

    # Call the function to run the application
    def Req7():
        def convolve_signals(indices1, samples1, indices2, samples2):
            result_indices = []
            result_samples = []

            # Perform the convolution by iterating through all possible combinations
            for i in range(len(indices1)):
                for j in range(len(indices2)):
                    index = indices1[i] + indices2[j]
                    sample = samples1[i] * samples2[j]

                    # Check if the index already exists in the result
                    if index in result_indices:
                        result_samples[result_indices.index(index)] += sample
                    else:
                        result_indices.append(index)
                        result_samples.append(sample)

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

            if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
                return False, "Conv Test case failed, your signal has different length from the expected one"

            for i in range(len(Your_indices)):
                if Your_indices[i] != expected_indices[i]:
                    return False, "Conv Test case failed, your signal has different indices from the expected one"

            for i in range(len(expected_samples)):
                if abs(Your_samples[i] - expected_samples[i]) >= 0.01:
                    return False, "Conv Test case failed, your signal has different values from the expected one"

            return True, "Conv Test case passed successfully"

        def load_files():
            file_path1 = filedialog.askopenfilename(title="Load Input Signal 1", filetypes=[("Text files", "*.txt")])
            if not file_path1:
                return
            indices1, samples1 = load_signal(file_path1)

            file_path2 = filedialog.askopenfilename(title="Load Input Signal 2", filetypes=[("Text files", "*.txt")])
            if not file_path2:
                return
            indices2, samples2 = load_signal(file_path2)

            convolved_indices, convolved_samples = convolve_signals(indices1, samples1, indices2, samples2)

            # Validate convolution result using ConvTest function
            success, message = ConvTest(convolved_indices, convolved_samples)
            if success:
                messagebox.showinfo("Convolution Result", "Conv Test case passed successfully")
            else:
                messagebox.showerror("Convolution Result", message)

        root = tk.Tk()
        root.title("Signal Convolution")
        root.geometry("200x50")
        load_button = tk.Button(root, text="Load Signals", command=load_files)
        load_button.pack()

        root.mainloop()

    root = tk.Tk()
    root.geometry("220x200")
    root.title("Task 6")

    menu_frame = tk.Frame(root)
    menu_frame.pack()
    task_1_button = tk.Button(menu_frame, text="Smoothing", command=Req1)
    task_1_button.pack()

    task_2_button = tk.Button(menu_frame, text="Sharpening", command=Req2)
    task_2_button.pack()

    task_3_button = tk.Button(menu_frame, text="Shifting", command=Req3)
    task_3_button.pack()

    task_4_button = tk.Button(menu_frame, text="Folding", command=Req4)
    task_4_button.pack()

    task_5_button = tk.Button(menu_frame, text="Shifting And Folding", command=Req5)
    task_5_button.pack()

    task_6_button = tk.Button(menu_frame, text="Remove DC Component", command=Req6)
    task_6_button.pack()

    task_7_button = tk.Button(menu_frame, text="Conv", command=Req7)
    task_7_button.pack()

    root.mainloop()
