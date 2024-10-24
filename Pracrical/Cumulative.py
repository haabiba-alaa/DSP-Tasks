import tkinter as tk
from Task_1 import execute_task_1
from Task_2 import execute_task_2
from Task_3 import execute_task_3
from Task_4 import execute_task_4
from Task_5 import execute_task_5
from Task_6 import execute_task_6
from Task_7 import execute_task_7
from Task_8 import execute_task_8


def run_task_1():
    execute_task_1()


def run_task_2():
    execute_task_2()


def run_task_3():
    execute_task_3()


def run_task_4():
    execute_task_4()


def run_task_5():
    execute_task_5()


def run_task_6():
    execute_task_6()


def run_task_7():
    execute_task_7()


def run_task_8():
    execute_task_8()


root = tk.Tk()
root.geometry("220x230")
root.title("DSP Tasks")

menu_frame = tk.Frame(root)
menu_frame.pack()
task_1_button = tk.Button(menu_frame, text="Task 1", command=run_task_1)
task_1_button.pack()

task_2_button = tk.Button(menu_frame, text="Task 2", command=run_task_2)
task_2_button.pack()

task_3_button = tk.Button(menu_frame, text="Task 3", command=run_task_3)
task_3_button.pack()

task_4_button = tk.Button(menu_frame, text="Task 4", command=run_task_4)
task_4_button.pack()

task_5_button = tk.Button(menu_frame, text="Task 5", command=run_task_5)
task_5_button.pack()

task_6_button = tk.Button(menu_frame, text="Task 6", command=run_task_6)
task_6_button.pack()

task_7_button = tk.Button(menu_frame, text="Task 7", command=run_task_7)
task_7_button.pack()

task_8_button = tk.Button(menu_frame, text="Task 8", command=run_task_8)
task_8_button.pack()

root.mainloop()
