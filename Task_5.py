import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, filedialog
from tkinter import ttk


class DCT:
    def __init__(self):
        self.input_signal = None
        self.coefficients_to_save = None
        self.output_signal = None

    def run(self):
        output = []
        N = len(self.input_signal)
        sqrt = np.sqrt(2.0 / N)

        for k in range(N):
            y_k = 0
            for n in range(N):
                y_k += self.input_signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))

            output.append(sqrt * y_k)

        self.output_signal = np.array(output)

        self.output_signal = np.array(output)

    def save_coefficients_to_file(self):
        with open("output.txt", "w") as file:
            for i in range(self.coefficients_to_save):
                file.write(f"Coefficient[{i}] = {self.output_signal[i]}\n")

        return f"First {self.coefficients_to_save} coefficients saved to output.txt."


class DCTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT & Remove DC Component ")

        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Compute DCT')
        self.tabControl.add(self.tab2, text='Remove DC Component')
        self.tabControl.pack(expand=1, fill="both")

        self.create_dct_tab()
        self.create_remove_dc_tab()

    def create_dct_tab(self):
        self.label_input = Label(self.tab1, text="Choose input file:")
        self.button_browse = Button(self.tab1, text="Browse", command=self.browse_file)
        self.label_coefficients = Label(self.tab1, text="Enter the number of coefficients to save:")
        self.entry_coefficients = Entry(self.tab1, width=10)
        self.button_compute_dct = Button(self.tab1, text="Compute DCT", command=self.run_dct)
        self.text_output = Text(self.tab1, height=10, width=50)
        self.scrollbar_output = Scrollbar(self.tab1, command=self.text_output.yview)

        self.label_input.grid(row=0, column=0, pady=10)
        self.button_browse.grid(row=0, column=1, pady=10)
        self.label_coefficients.grid(row=1, column=0, pady=5)
        self.entry_coefficients.grid(row=1, column=1, pady=5)
        self.button_compute_dct.grid(row=2, column=0, columnspan=2, pady=10)
        self.text_output.grid(row=3, column=0, columnspan=2, pady=10)
        self.scrollbar_output.grid(row=3, column=2, sticky="ns")

        self.entry_input = Entry(self.tab1, width=40)
        self.entry_input.grid(row=4, column=0, columnspan=2, pady=10)

    def create_remove_dc_tab(self):
        self.label_input_dc = Label(self.tab2, text="Choose input file:")
        self.button_browse_dc = Button(self.tab2, text="Browse", command=self.browse_file_dc)
        self.button_remove_dc = Button(self.tab2, text="Remove DC Component", command=self.remove_dc_component)
        self.text_output_dc = Text(self.tab2, height=10, width=50)
        self.scrollbar_output_dc = Scrollbar(self.tab2, command=self.text_output_dc.yview)

        self.label_input_dc.grid(row=0, column=0, pady=10)
        self.button_browse_dc.grid(row=0, column=1, pady=10)
        self.button_remove_dc.grid(row=1, column=0, columnspan=2, pady=10)
        self.text_output_dc.grid(row=2, column=0, columnspan=2, pady=10)
        self.scrollbar_output_dc.grid(row=2, column=2, sticky="ns")

        self.entry_input_dc = Entry(self.tab2, width=40)
        self.entry_input_dc.grid(row=3, column=0, columnspan=2, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.entry_input.delete(0, tk.END)
                self.entry_input.insert(0, file.read())

    def browse_file_dc(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.entry_input_dc.delete(0, tk.END)
                self.entry_input_dc.insert(0, file.read())

    def run_dct(self):
        input_values = self.entry_input.get()
        input_lines = input_values.split("\n")

        input_values = []
        for line in input_lines:
            parts = line.strip().split(" ")
            if len(parts) == 2:
                try:
                    value = float(parts[1])
                    input_values.append(value)
                except ValueError:
                    print(f"Skipping invalid value: {parts[1]}")

        dct_algorithm = DCT()
        dct_algorithm.input_signal = np.array(input_values)
        dct_algorithm.coefficients_to_save = int(self.entry_coefficients.get())
        dct_algorithm.run()

        dct_algorithm_output = dct_algorithm.save_coefficients_to_file()
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, "DCT Result:\n")
        self.text_output.insert(tk.END, f"{dct_algorithm_output}\n")
        self.text_output.insert(tk.END, "Output Signal:\n")
        for i, value in enumerate(dct_algorithm.output_signal):
            self.text_output.insert(tk.END, f"Output[{i}] = {value}\n")

    def remove_dc_component(self):
        input_values = self.entry_input_dc.get()
        input_lines = input_values.split("\n")

        input_signal = []
        for line in input_lines:
            parts = line.strip().split(" ")
            if len(parts) == 2:
                try:
                    value = float(parts[1])
                    input_signal.append(value)
                except ValueError:
                    print(f"Skipping invalid value: {parts[1]}")

        if input_signal:
            average = np.mean(input_signal)
            dc_removed_signal = [x - average for x in input_signal]

            self.text_output_dc.delete("1.0", tk.END)
            self.text_output_dc.insert(tk.END, "DC Removed Signal:\n")
            for i, value in enumerate(dc_removed_signal):
                self.text_output_dc.insert(tk.END, f"Output[{i}] = {value}\n")
        else:
            self.text_output_dc.delete("1.0", tk.END)
            self.text_output_dc.insert(tk.END, "No valid input signal found.")


def setup_task_5():
    root = tk.Tk()
    app = DCTApp(root)
    root.mainloop()


def execute_task_5():
    setup_task_5()


if __name__ == "__main__":
    setup_task_5()
