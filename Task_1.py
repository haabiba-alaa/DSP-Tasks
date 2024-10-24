import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Create the tkinter window
def execute_task_1():
    # Create the tkinter window
    window = tk.Tk()
    window.title("Signal Generator and Plotter")

    # Create a Notebook for tabs
    tab_parent = ttk.Notebook(window)

    # Task 1 - First tab
    tab1 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Task 1")

    # Create a figure for the plot with two subplots for Task 1
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 4))
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.get_tk_widget().pack()

    # Function to browse a file for Task 1
    def browse_file_task1():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            selected_file.set(file_path)
            x, y = read_file(selected_file.get())
            plot_continuous_and_discrete(x, y, ax1, ax2, canvas1)

    selected_file = tk.StringVar()

    frame1 = tk.Frame(tab1)
    frame1.pack()

    browse_button1 = tk.Button(frame1, text="Browse", command=browse_file_task1)
    browse_button1.pack()

    # Function to read a file and return data
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

    # Function to plot continuous and discrete data
    def plot_continuous_and_discrete(x, y, ax1, ax2, canvas):
        ax1.clear()
        ax2.clear()

        ax1.plot(x, y)
        ax1.set_xlabel("X-axis")
        ax1.set_ylabel("Y-axis")
        ax1.set_title("Continuous Plot")

        # Plot the discrete data as a sampled signal
        for i in range(len(x)):
            ax2.plot([x[i], x[i]], [0, y[i]], color='b', marker='o')

        ax2.set_xlabel("X-axis")
        ax2.set_ylabel("Y-axis")
        ax2.set_title("Discrete Plot")

        canvas.draw()

    # Task 2 - Second tab
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab2, text="Task 2")

    # Create a figure for the plot with three subplots for Task 2
    fig2, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(15, 4))
    canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
    canvas2.get_tk_widget().pack()

    # Frequency input for Task 2
    frequency_label2 = tk.Label(tab2, text="Frequency (Hz):")
    frequency_label2.pack()
    frequency_entry2 = tk.Entry(tab2)
    frequency_entry2.pack()

    # Amplitude input for Task 2
    amplitude_label2 = tk.Label(tab2, text="Amplitude:")
    amplitude_label2.pack()
    amplitude_entry2 = tk.Entry(tab2)
    amplitude_entry2.pack()

    # Phase shift input for Task 2
    phase_shift_label2 = tk.Label(tab2, text="Phase Shift (radians):")
    phase_shift_label2.pack()
    phase_shift_entry2 = tk.Entry(tab2)
    phase_shift_entry2.pack()

    # Sampling frequency input for Task 2
    sampling_frequency_label2 = tk.Label(tab2, text="Sampling Frequency (Hz):")
    sampling_frequency_label2.pack()
    sampling_frequency_entry2 = tk.Entry(tab2)
    sampling_frequency_entry2.pack()

    # Radio buttons for signal type for Task 2
    signal_type2 = tk.StringVar()
    signal_type2.set("Sine")
    sine_button2 = tk.Radiobutton(tab2, text="Sine", variable=signal_type2, value="Sine")
    cosine_button2 = tk.Radiobutton(tab2, text="Cosine", variable=signal_type2, value="Cosine")
    sine_button2.pack()
    cosine_button2.pack()

    # Function to calculate and plot a signal for Task 2
    def calculate_and_plot_signal_task2():
        try:
            # Clear the previous plots
            ax3.clear()
            ax4.clear()
            ax5.clear()

            # Get user input values
            frequency = float(frequency_entry2.get())
            amplitude = float(amplitude_entry2.get())
            phase_shift = float(phase_shift_entry2.get())
            sampling_frequency = float(sampling_frequency_entry2.get())

            # Check if the sampling frequency meets the Nyquist-Shannon condition
            if sampling_frequency < 2 * frequency:
                result_label2.config(text="Sampling frequency should be at least twice the signal frequency.")
                return

            # Create a time array with respect to the sampling frequency
            time = np.arange(0, 1, 1 / sampling_frequency)

            if signal_type2.get() == "Sine":
                # Calculate the sine wave signal
                sine_signal = amplitude * np.sin(2 * np.pi * frequency * time + phase_shift)
                cosine_signal = np.zeros_like(sine_signal)  # Generate a zero cosine signal
            else:
                # Calculate the cosine wave signal
                cosine_signal = amplitude * np.cos(2 * np.pi * frequency * time + phase_shift)
                sine_signal = np.zeros_like(cosine_signal)  # Generate a zero sine signal

            # Plot the new signals
            ax3.plot(time, sine_signal, label='Sine Signal')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Amplitude')
            ax3.set_title('Sine Wave Signal')
            ax3.legend()
            ax3.grid(True)

            ax4.plot(time, cosine_signal, label='Cosine Signal', color='orange')
            ax4.set_xlabel('Time')
            ax4.set_ylabel('Amplitude')
            ax4.set_title('Cosine Wave Signal')
            ax4.legend()
            ax4.grid(True)

            # Sample the signal
            sampling_period = 1 / sampling_frequency
            sampled_time = np.arange(0, 1, sampling_period)
            sampled_sine_signal = amplitude * np.sin(2 * np.pi * frequency * sampled_time + phase_shift)
            sampled_cosine_signal = amplitude * np.cos(2 * np.pi * frequency * sampled_time + phase_shift)

            # Plot the sampled signals
            ax5.stem(sampled_time, sampled_sine_signal, label='Sampled Sine Signal', basefmt=' ')
            ax5.stem(sampled_time, sampled_cosine_signal, markerfmt='ro', linefmt='r-', label='Sampled Cosine Signal',
                     basefmt=' ')
            ax5.set_xlabel('Sampled Time')
            ax5.set_ylabel('Amplitude')
            ax5.set_title('Sampled Signals')
            ax5.legend()
            ax5.grid(True)

            # Display the updated plots in the tkinter window
            canvas2.draw()
            result_label2.config(text="Signal generated and sampled successfully.")

        except ValueError:
            result_label2.config(text="Invalid input. Please enter numeric values.")

    # Calculate button for Task 2
    calculate_button2 = tk.Button(tab2, text="Calculate", command=calculate_and_plot_signal_task2)
    calculate_button2.pack()

    # Result label for Task 2
    result_label2 = tk.Label(tab2, text="")
    result_label2.pack()

    # Display the tabs
    tab_parent.pack(fill='both', expand=1)

    # Start the main event loop
    window.mainloop()
