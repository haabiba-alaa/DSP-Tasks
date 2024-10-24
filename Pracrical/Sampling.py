from All_Func import *
from tkinter import filedialog


def Req5():
    def load_files():
        M = int(entry_M.get())
        L = int(entry_L.get())

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
        if M != 0 and L == 0:
            indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
            resultsInd, resultsSam = convolve_signals(ECG_indices, ECG_samples, indices, coefficients)
            down_sampled_indices, down_sampled_values = down_sample(resultsInd, resultsSam, M)
            Compare_Signals(file_path1, down_sampled_indices, down_sampled_values)

        elif M == 0 and L != 0:
            up_sampled_indices, up_sampled_values = up_sample(ECG_indices, ECG_samples, L)
            indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
            resultsInd, resultsSam = convolve_signals(up_sampled_indices, up_sampled_values, indices, coefficients)
            resultsInd = resultsInd[:-2]
            resultsSam = resultsSam[:-2]
            Compare_Signals(file_path1, resultsInd, resultsSam)

        elif M != 0 and L != 0:
            up_sampled_indices, up_sampled_values = up_sample(ECG_indices, ECG_samples, L)
            indices, coefficients = calc_LFF_coff(fs, stop_band_attenuation, fc, transition_band)
            resultsInd, resultsSam = convolve_signals(up_sampled_indices, up_sampled_values, indices, coefficients)
            resultsInd = resultsInd[:-2]
            resultsSam = resultsSam[:-2]
            down_sampled_indices, down_sampled_values = down_sample(resultsInd, resultsSam, M)
            print(len(down_sampled_indices))
            print(len(down_sampled_values))
            for index, value in zip(down_sampled_indices, down_sampled_values):
                print(f" {index} {value}")
            Compare_Signals(file_path1, down_sampled_indices, down_sampled_values)

    root = tk.Tk()
    root.title("Up Or Down")
    root.geometry("300x150")

    label_M = tk.Label(root, text="Enter the value of M:")
    label_M.pack()
    entry_M = tk.Entry(root)
    entry_M.pack()

    label_L = tk.Label(root, text="Enter the value of L:")
    label_L.pack()
    entry_L = tk.Entry(root)
    entry_L.pack()

    load_button = tk.Button(root, text="Load Signals", command=load_files)
    load_button.pack()

    root.mainloop()
