import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def execute_task_2():
    # Global variables to store loaded data
    data1 = None
    data2 = None

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

    def add_subplots():
        # Create a sub window to load the first file
        first_file_window = tk.Toplevel(root)
        first_file_window.title("Load First File")

        def load_first_file():

            file_path1 = filedialog.askopenfilename()
            if not file_path1:
                return
            data1 = read_file(file_path1)
            first_file_window.destroy()  # Close the first file window after loading

            # Create a sub window to load the second file
            second_file_window = tk.Toplevel(root)
            second_file_window.title("Load Second File")

            def load_second_file():

                file_path2 = filedialog.askopenfilename()
                if not file_path2:
                    return
                data2 = read_file(file_path2)
                second_file_window.destroy()  # Close the second file window after loading

                if data1 is not None and data2 is not None:
                    x1, y1 = data1
                    x2, y2 = data2

                    # Add the y values of the two loaded signals
                    x = x1  # Assuming the x-values are the same for both signals
                    y_new = [y1_val + y2_val for y1_val, y2_val in zip(y1, y2)]

                    # Plot the original data
                    fig = Figure(figsize=(10, 5))
                    ax1 = fig.add_subplot(131)
                    ax1.plot(x1, y1, label='Original Data 1')

                    # Plot the second loaded data
                    ax2 = fig.add_subplot(132)
                    ax2.plot(x2, y2, label='Original Data 2')

                    # Plot the result of addition
                    ax3 = fig.add_subplot(133)
                    ax3.plot(x, y_new, label='Addition Result')

                    ax1.legend()
                    ax2.legend()
                    ax3.legend()

                    create_new_window(fig)

            load_second_file_button = tk.Button(second_file_window, text="Load Second File", command=load_second_file)
            load_second_file_button.pack()

        load_first_file_button = tk.Button(first_file_window, text="Load First File", command=load_first_file)
        load_first_file_button.pack()

    def sub_subplots():
        # Create a sub window to load the first file
        first_file_window = tk.Toplevel(root)
        first_file_window.title("Load First File")

        def load_first_file():

            file_path1 = filedialog.askopenfilename()
            if not file_path1:
                return
            data1 = read_file(file_path1)
            first_file_window.destroy()  # Close the first file window after loading

            # Create a sub window to load the second file
            second_file_window = tk.Toplevel(root)
            second_file_window.title("Load Second File")

            def load_second_file():

                file_path2 = filedialog.askopenfilename()
                if not file_path2:
                    return
                data2 = read_file(file_path2)
                second_file_window.destroy()  # Close the second file window after loading

                if data1 is not None and data2 is not None:
                    x1, y1 = data1
                    x2, y2 = data2

                    # Add the y values of the two loaded signals
                    x = x1  # Assuming the x-values are the same for both signals
                    y_new = [y1_val - y2_val for y1_val, y2_val in zip(y1, y2)]

                    # Plot the original data
                    fig = Figure(figsize=(10, 5))
                    ax1 = fig.add_subplot(131)
                    ax1.plot(x1, y1, label='Original Data 1')

                    # Plot the second loaded data
                    ax2 = fig.add_subplot(132)
                    ax2.plot(x2, y2, label='Original Data 2')

                    # Plot the result of addition
                    ax3 = fig.add_subplot(133)
                    ax3.plot(x, y_new, label='Subtraction Result')

                    ax1.legend()
                    ax2.legend()
                    ax3.legend()

                    create_new_window(fig)

            load_second_file_button = tk.Button(second_file_window, text="Load Second File", command=load_second_file)
            load_second_file_button.pack()

        load_first_file_button = tk.Button(first_file_window, text="Load First File", command=load_first_file)
        load_first_file_button.pack()

    def multiply_plot():
        # Load a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        data = read_file(file_path)

        if data is not None:
            x, y = data

            # Create a Tkinter window for the integer input
            input_window = tk.Toplevel(root)
            input_window.title("Enter an Integer")

            entry_label = tk.Label(input_window, text="Enter an integer:")
            entry_label.pack()

            entry = tk.Entry(input_window)
            entry.pack()

            def process_input():
                integer_input = int(entry.get())
                input_window.destroy()  # Close the input window

                # Multiply the y values by the integer input
                y_multiplied = [y_val * integer_input for y_val in y]

                # Create a figure
                fig = Figure(figsize=(10, 5))

                # Plot the original data
                ax1 = fig.add_subplot(131)
                ax1.plot(x, y, label='Original Data')
                ax1.set_title('Original Data')
                ax1.legend()

                # Plot the multiplied data
                ax2 = fig.add_subplot(132)
                ax2.plot(x, y_multiplied, label='Multiplied Data')
                ax2.set_title('Multiplied Data')
                ax2.legend()

                # Show the plots in the Tkinter window
                create_new_window(fig)

            process_button = tk.Button(input_window, text="Process", command=process_input)
            process_button.pack()

    def square2_plot():
        # Load a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        data = read_file(file_path)

        if data is not None:
            x, y = data

        y_multiplied = [y_val * y_val for y_val in y]

        # Create a figure
        fig = Figure(figsize=(10, 5))

        # Plot the original data
        ax1 = fig.add_subplot(131)
        ax1.plot(x, y, label='Original Data')
        ax1.set_title('Original Data')
        ax1.legend()

        # Plot the multiplied data
        ax2 = fig.add_subplot(132)
        ax2.plot(x, y_multiplied, label='Multiplied Data')
        ax2.set_title('Multiplied Data')
        ax2.legend()

        # Show the plots in the Tkinter window
        create_new_window(fig)

    def shifting_plot():
        # Load a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        data = read_file(file_path)

        if data is not None:
            x, y = data

            # Create a Tkinter window for the integer input
            input_window = tk.Toplevel(root)
            input_window.title("Enter an Integer")

            entry_label = tk.Label(input_window, text="Enter an integer:")
            entry_label.pack()

            entry = tk.Entry(input_window)
            entry.pack()

            def process_input():
                integer_input = int(entry.get())
                input_window.destroy()  # Close the input window

                # Multiply the y values by the integer input
                x_multiplied = [x_val + integer_input for x_val in x]

                # Create a figure
                fig = Figure(figsize=(10, 5))

                # Plot the original data
                ax1 = fig.add_subplot(131)
                ax1.plot(x, y, label='Original Data')
                ax1.set_title('Original Data')
                ax1.legend()

                # Plot the multiplied data
                ax2 = fig.add_subplot(132)
                ax2.plot(x_multiplied, y, label='Multiplied Data')
                ax2.set_title('Multiplied Data')
                ax2.legend()

                create_new_window(fig)

            process_button = tk.Button(input_window, text="Process", command=process_input)
            process_button.pack()

    def get_bounds():
        # Create a new tkinter window for getting upper and lower bounds
        bounds_window = tk.Toplevel(root)
        bounds_window.title("Enter Bounds")

        upper_label = tk.Label(bounds_window, text="Enter the upper bound for normalization:")
        upper_label.pack()

        upper_entry = tk.Entry(bounds_window)
        upper_entry.pack()

        lower_label = tk.Label(bounds_window, text="Enter the lower bound for normalization:")
        lower_label.pack()

        lower_entry = tk.Entry(bounds_window)
        lower_entry.pack()

        def process_bounds():
            upper_bound = float(upper_entry.get())
            lower_bound = float(lower_entry.get())
            bounds_window.destroy()  # Close the bounds input window

            normalize_plot(upper_bound, lower_bound)

        process_button = tk.Button(bounds_window, text="Process Bounds", command=process_bounds)
        process_button.pack()

    def normalize_plot(upper_bound, lower_bound):
        # Load a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        data = read_file(file_path)

        if data is not None:
            x, y = data

            # Normalize the y values
            normalized_y = [(y_val - min(y)) / (max(y) - min(y)) * (upper_bound - lower_bound) + lower_bound for y_val
                            in y]

            # Create a figure
            fig = Figure(figsize=(10, 5))

            # Plot the original data
            ax1 = fig.add_subplot(121)
            ax1.plot(x, y, label='Original Data')
            ax1.set_title('Original Data')
            ax1.legend()

            # Plot the normalized data
            ax2 = fig.add_subplot(122)
            ax2.plot(x, normalized_y, label=f'Normalized Data (upper={upper_bound}, lower={lower_bound})')
            ax2.set_title('Normalized Data')
            ax2.legend()

            # Show the plots in the Tkinter window
            create_new_window(fig)

    def accumulate_plot():
        # Load a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        data = read_file(file_path)

        if data is not None:
            x, y = data

            # Accumulate the y values
            accumulated_y = [sum(y[:i + 1]) for i in range(len(y))]

            # Create a figure
            fig = Figure(figsize=(10, 5))

            # Plot the original data
            ax1 = fig.add_subplot(121)
            ax1.plot(x, y, label='Original Data')
            ax1.set_title('Original Data')
            ax1.legend()

            # Plot the accumulated data
            ax2 = fig.add_subplot(122)
            ax2.plot(x, accumulated_y, label='Accumulated Data')
            ax2.set_title('Accumulated Data')
            ax2.legend()

            # Show the plots in the Tkinter window
            create_new_window(fig)

    # Create the main tkinter window
    root = tk.Tk()
    root.geometry("250x250")  # Set the initial window size to 10x10
    root.title("Signal Operations")

    # Create a menu of buttons
    menu_frame = tk.Frame(root)
    menu_frame.pack()

    add_button = tk.Button(menu_frame, text="Add", command=add_subplots)
    add_button.pack()

    subtract_button = tk.Button(menu_frame, text="Subtract", command=sub_subplots)
    subtract_button.pack()

    multiply_button = tk.Button(root, text="Multiply", command=multiply_plot)
    multiply_button.pack()

    square_button = tk.Button(root, text="Square", command=square2_plot)
    square_button.pack()

    shift_button = tk.Button(root, text="Shift", command=shifting_plot)
    shift_button.pack()

    normalize_button = tk.Button(root, text="Normalize", command=get_bounds)
    normalize_button.pack()

    accumulate_button = tk.Button(root, text="Accumulate", command=accumulate_plot)
    accumulate_button.pack()

    root.mainloop()
