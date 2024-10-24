from All_Func import *
from tkinter import filedialog
import tkinter as tk


def Req1():
    def load_files():
        file_path1 = filedialog.askopenfilename(title="Load Coff", filetypes=[("Text files", "*.txt")])
        if not file_path1:
            return

        file_path2 = filedialog.askopenfilename(title="Load Filter Specifications", filetypes=[("Text files", "*.txt")])
        if not file_path2:
            return

        filter_type, fs, stop_band_attenuation, fc, transition_band = read_filter_specificationsLH(
            file_path2)

        if filter_type == "High pass":
            indices, coefficients = calc_HFF_coff(fs, stop_band_attenuation, fc, transition_band)
            print("Test 3")
            Compare_Signals(file_path1, indices, coefficients)
            return
        elif filter_type == "Low pass":
            indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
            print("Test 1")
            Compare_Signals(file_path1, indices, coefficients)
            return

    root = tk.Tk()
    root.title("FIR")
    root.geometry("200x50")
    load_button = tk.Button(root, text="Load Signals", command=load_files)
    load_button.pack()

    root.mainloop()


def Req2():
    def load_files():
        file_path2 = filedialog.askopenfilename(title="Load Filter Specifications", filetypes=[("Text files", "*.txt")])
        if not file_path2:
            return

        file_path3 = filedialog.askopenfilename(title="Load ECG Signal", filetypes=[("Text files", "*.txt")])
        if not file_path3:
            return

        file_path1 = filedialog.askopenfilename(title="Load Output", filetypes=[("Text files", "*.txt")])
        if not file_path1:
            return

        ECG_indices, ECG_samples = load_signal(file_path3)
        filter_type, fs, stop_band_attenuation, fc, transition_band = read_filter_specificationsLH(file_path2)

        if filter_type == "High pass":
            indices, coefficients = calc_HFF_coff(fs, stop_band_attenuation, fc, transition_band)
            resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_samples)
            print("Test 4")
            Compare_Signals(file_path1, resultsInd, resultsSam)
            save_results(resultsInd, resultsSam)
            plot_signal_in_tkinter(resultsInd, resultsSam)

            return
        elif filter_type == "Low pass":
            indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
            resultsInd, resultsSam = convolve_signals(ECG_indices, ECG_samples, indices, coefficients)
            print("Test 2")
            Compare_Signals(file_path1, resultsInd, resultsSam)
            save_results(resultsInd, resultsSam)
            plot_signal_in_tkinter(resultsInd, resultsSam)
            return

    root = tk.Tk()
    root.title("FIR")
    root.geometry("200x50")
    load_button = tk.Button(root, text="Load Signals", command=load_files)
    load_button.pack()

    root.mainloop()


def Req3():
    def load_files():
        file_path1 = filedialog.askopenfilename(title="Load Coff", filetypes=[("Text files", "*.txt")])
        if not file_path1:
            return

        file_path2 = filedialog.askopenfilename(title="Load Filter Specifications", filetypes=[("Text files", "*.txt")])
        if not file_path2:
            return

        filter_type, fs, stop_band_attenuation, fc1, fc2, transition_band = read_filter_specificationsB(
            file_path2)

        if filter_type == "Band pass":
            indices, coefficients = calc_BPF_coff(fs, stop_band_attenuation, fc1, fc2, transition_band)
            print("Test 5")
            Compare_Signals(file_path1, indices, coefficients)
            return
        elif filter_type == "Band stop":
            indices, coefficients = calc_BSF_coff(fs, stop_band_attenuation, fc1, fc2, transition_band)
            print("Test 7")
            Compare_Signals(file_path1, indices, coefficients)
            return

    root = tk.Tk()
    root.title("BPF Or BSF")
    root.geometry("200x50")
    load_button = tk.Button(root, text="Load Signals", command=load_files)
    load_button.pack()

    root.mainloop()


def Req4():
    def load_files():
        file_path2 = filedialog.askopenfilename(title="Load Filter Specifications", filetypes=[("Text files", "*.txt")])
        if not file_path2:
            return

        file_path3 = filedialog.askopenfilename(title="Load ECG Signal", filetypes=[("Text files", "*.txt")])
        if not file_path3:
            return

        file_path1 = filedialog.askopenfilename(title="Load Output", filetypes=[("Text files", "*.txt")])
        if not file_path1:
            return

        ECG_indices, ECG_samples = load_signal(file_path3)
        filter_type, fs, stop_band_attenuation, fc1, fc2, transition_band = read_filter_specificationsB(
            file_path2)

        if filter_type == "Band pass":
            indices, coefficients = calc_BPF_coff(fs, stop_band_attenuation, fc1, fc2, transition_band)
            resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_samples)
            print("Test 6")
            Compare_Signals(file_path1, resultsInd, resultsSam)
            save_results(resultsInd, resultsSam)
            plot_signal_in_tkinter(resultsInd, resultsSam)
            return
        elif filter_type == "Band stop":
            indices, coefficients = calc_BSF_coff(fs, stop_band_attenuation, fc1, fc2, transition_band)
            resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_samples)
            print("Test 8")
            Compare_Signals(file_path1, resultsInd, resultsSam)
            save_results(resultsInd, resultsSam)
            plot_signal_in_tkinter(resultsInd, resultsSam)
            return

    root = tk.Tk()
    root.title("BPF Or BSF")
    root.geometry("200x50")
    load_button = tk.Button(root, text="Load Signals", command=load_files)
    load_button.pack()

    root.mainloop()
