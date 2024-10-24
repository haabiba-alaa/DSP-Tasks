from Sampling import Req5
from FIR import *
from pract2 import *


def run_task_1():
    Req1()


def run_task_2():
    Req2()


def run_task_3():
    Req3()


def run_task_4():
    Req4()


def run_task_5():
    Req5()


def run_task_6():
    Req6()


def run_task_7():
    Req7()


def run_task_8():
    Req8()


root = tk.Tk()
root.geometry("220x230")
root.title("Practical")

menu_frame = tk.Frame(root)
menu_frame.pack()

task_1_button = tk.Button(menu_frame, text="LPF Or HPF Coff", command=run_task_1)
task_1_button.pack()

task_2_button = tk.Button(menu_frame, text="LPF Or HPF ECG Signals", command=run_task_2)
task_2_button.pack()

task_3_button = tk.Button(menu_frame, text="BPF Or BSF Coff", command=run_task_3)
task_3_button.pack()

task_4_button = tk.Button(menu_frame, text="BPF Or BSF ECG Signals", command=run_task_4)
task_4_button.pack()

task_5_button = tk.Button(menu_frame, text="Sampling", command=run_task_5)
task_5_button.pack()

task_6_button = tk.Button(menu_frame, text="Template Matching", command=run_task_6)
task_6_button.pack()

task_8_button = tk.Button(menu_frame, text="Plot A", command=run_task_8)
task_8_button.pack()

task_7_button = tk.Button(menu_frame, text="Plot B", command=run_task_7)
task_7_button.pack()

root.mainloop()
