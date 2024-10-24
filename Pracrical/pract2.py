from All_Func import *


def Req6():
    classA_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/A"
    classB_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/B"
    test_folder = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Practical Test"

    output_folder_A = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/A"
    output_folder_B = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/B"
    output_folder_test = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/Test"

    def Req9():
        def preprocess(signal_folder):
            fs = 150
            new_fs = 100
            stop_band_attenuation = 50
            min_f = 150
            max_f = 250
            transition_band = 500
            M = new_fs / max_f
            L = max_f / new_fs

            signal_files = os.listdir(signal_folder)
            for file in signal_files:
                ECG_signal = load_signalTemp(os.path.join(signal_folder, file))
                signal_length = len(ECG_signal)
                ECG_indices = np.arange(signal_length)

                indices, coefficients = calc_BPF_coff(fs, stop_band_attenuation, min_f, max_f, transition_band)
                resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_signal)
                if new_fs >= max_f * 2:
                    resultsInd, resultsSam = up_down(L, M, resultsInd, resultsSam, fs, stop_band_attenuation, new_fs,
                                                     transition_band)
                else:
                    print("newFs is not valid")

                Remove_Samp = remove_dc_component(resultsSam)

                Norm_Ind, Norm_Samp = normalize_plot(resultsInd, Remove_Samp)

                autoCorr_samp = auto_correlation(Norm_Samp)

                length = len(autoCorr_samp)

                # Calculate the midpoint
                midpoint = length // 2  # Using integer division to get the whole number

                # Select data from the midpoint to the end
                selected_samp = autoCorr_samp[:midpoint]

                length = len(Norm_Ind)

                # Calculate the midpoint
                midpoint = length // 2  # Using integer division to get the whole number

                # Select data from the start to the midpoint
                selected_ind = Norm_Ind[:midpoint]

                dct_samp = compute_dct(selected_samp)
                # Preserve non-zero values
                non_zero_values = dct_samp[np.abs(dct_samp) > 0]

                if signal_folder == classA_folder and not os.path.exists(output_folder_A):
                    os.makedirs(output_folder_A)
                elif signal_folder == classB_folder and not os.path.exists(output_folder_B):
                    os.makedirs(output_folder_B)
                elif signal_folder == test_folder and not os.path.exists(output_folder_test):
                    os.makedirs(output_folder_test)

                if signal_folder == classA_folder:
                    output_file = os.path.join(output_folder_A, f"processed_{file}")
                    np.save(output_file, non_zero_values)

                elif signal_folder == classB_folder:
                    output_file = os.path.join(output_folder_B, f"processed_{file}")
                    np.save(output_file, non_zero_values)

                elif signal_folder == test_folder:
                    output_file = os.path.join(output_folder_test, f"processed_{file}")
                    np.save(output_file, non_zero_values)

        preprocess(classA_folder)
        preprocess(classB_folder)
        preprocess(test_folder)

    processed_ClassA = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/A"
    processed_ClassB = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/B"
    processed_test = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Processed/Test"
    average_signal_class1 = calculate_average(processed_ClassA)
    average_signal_class2 = calculate_average(processed_ClassB)

    display_results(processed_test, average_signal_class1, average_signal_class2)


def Req8():
    def preprocess_file(file_path):
        fs = 150
        new_fs = 100
        stop_band_attenuation = 50
        min_f = 150
        max_f = 250
        transition_band = 500
        M = new_fs / max_f
        L = max_f / new_fs

        root = tk.Tk()
        if file_path == ATest:
            root.title("Signal Plots A")
        else:
            root.title("Signal Plots B")

        ECG_signal = load_signalTemp(file_path)
        signal_length = len(ECG_signal)
        ECG_indices = np.arange(signal_length)

        fig, axs = plt.subplots(2, 3, figsize=(12, 6))

        # Plot Original Signal
        axs[0, 0].plot(ECG_indices, ECG_signal)
        axs[0, 0].set_title('Original Signal')

        indices, coefficients = calc_BPF_coff(fs, stop_band_attenuation, min_f, max_f, transition_band)
        resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_signal)
        if new_fs >= max_f * 2:
            resultsInd, resultsSam = up_down(L, M, resultsInd, resultsSam, fs, stop_band_attenuation, new_fs,
                                             transition_band)
        else:
            print("newFs is not valid")

        Remove_Samp = remove_dc_component(resultsSam)

        # Plot Remove Dc
        axs[0, 1].plot(resultsInd, Remove_Samp)
        axs[0, 1].set_title('Remove DC Component')

        Norm_Ind, Norm_Samp = normalize_plot(resultsInd, Remove_Samp)

        # Plot Normalized Signal
        axs[1, 0].plot(Norm_Ind, Norm_Samp)
        axs[1, 0].set_title('Normalized Signal')

        autoCorr_samp = auto_correlation(Norm_Samp)

        # Plot Auto Correlation
        axs[1, 1].plot(Norm_Ind, autoCorr_samp)
        axs[1, 1].set_title('Auto Correlation')

        length = len(autoCorr_samp)

        # Calculate the midpoint
        midpoint = length // 2  # Using integer division to get the whole number

        # Select data from the midpoint to the end
        selected_samp = autoCorr_samp[:midpoint]

        length = len(Norm_Ind)

        # Calculate the midpoint
        midpoint = length // 2  # Using integer division to get the whole number

        # Select data from the start to the midpoint
        selected_ind = Norm_Ind[:midpoint]

        axs[0, 2].plot(selected_ind, selected_samp)
        axs[0, 2].set_title('Half Auto Correlation')

        dct_samp = compute_dct(selected_samp)

        axs[1, 2].plot(selected_ind, dct_samp)
        axs[1, 2].set_title('DCT')

        fig.tight_layout()

        # Convert Matplotlib figure to Tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # Embed Matplotlib figure in Tkinter window
        canvas.get_tk_widget().pack()

        root.mainloop()

    ATest = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Practical Test/ATest1.txt"

    preprocess_file(ATest)


def Req7():
    def preprocess_file(file_path):
        fs = 150
        new_fs = 100
        stop_band_attenuation = 50
        min_f = 150
        max_f = 250
        transition_band = 500
        M = new_fs / max_f
        L = max_f / new_fs

        root = tk.Tk()
        if file_path == ATest:
            root.title("Signal Plots A")
        else:
            root.title("Signal Plots B")

        ECG_signal = load_signalTemp(file_path)
        signal_length = len(ECG_signal)
        ECG_indices = np.arange(signal_length)

        fig, axs = plt.subplots(2, 3, figsize=(12, 6))

        # Plot Original Signal
        axs[0, 0].plot(ECG_indices, ECG_signal)
        axs[0, 0].set_title('Original Signal')

        indices, coefficients = calc_BPF_coff(fs, stop_band_attenuation, min_f, max_f, transition_band)
        resultsInd, resultsSam = convolve_signals(indices, coefficients, ECG_indices, ECG_signal)
        if new_fs >= max_f * 2:
            resultsInd, resultsSam = up_down(L, M, resultsInd, resultsSam, fs, stop_band_attenuation, new_fs,
                                             transition_band)
        else:
            print("newFs is not valid")

        Remove_Samp = remove_dc_component(resultsSam)

        # Plot Remove Dc
        axs[0, 1].plot(resultsInd, Remove_Samp)
        axs[0, 1].set_title('Remove DC Component')

        Norm_Ind, Norm_Samp = normalize_plot(resultsInd, Remove_Samp)

        # Plot Normalized Signal
        axs[1, 0].plot(Norm_Ind, Norm_Samp)
        axs[1, 0].set_title('Normalized Signal')

        autoCorr_samp = auto_correlation(Norm_Samp)

        # Plot Auto Correlation
        axs[1, 1].plot(Norm_Ind, autoCorr_samp)
        axs[1, 1].set_title('Auto Correlation')

        length = len(autoCorr_samp)

        # Calculate the midpoint
        midpoint = length // 2  # Using integer division to get the whole number

        # Select data from the midpoint to the end
        selected_samp = autoCorr_samp[:midpoint]

        length = len(Norm_Ind)

        # Calculate the midpoint
        midpoint = length // 2  # Using integer division to get the whole number

        # Select data from the start to the midpoint
        selected_ind = Norm_Ind[:midpoint]

        axs[0, 2].plot(selected_ind, selected_samp)
        axs[0, 2].set_title('Half Auto Correlation')

        dct_samp = compute_dct(selected_samp)

        axs[1, 2].plot(selected_ind, dct_samp)
        axs[1, 2].set_title('DCT')

        fig.tight_layout()

        # Convert Matplotlib figure to Tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # Embed Matplotlib figure in Tkinter window
        canvas.get_tk_widget().pack()

        root.mainloop()

    ATest = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Practical Test/ATest1.txt"
    BTest = "/Users/habibaalaa/PycharmProjects/pythonProject/Dsp Tasks/Practical Test/BTest1.txt"

    preprocess_file(BTest)
