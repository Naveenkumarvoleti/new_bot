try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk
from time import sleep
import time

def progress(finalTime):
    #start progress bar
##    root = tk.Toplevel()
    root=tk.Tk()
    runTime=range(finalTime)
    remainingTime=str(finalTime)
    tk.Label(root, text=" progress running").grid(row=0,column=0)
    tk.Label(root, text=" Remaining Time: ").grid(row=1,column=0)
    tk.Label(root,text='  ').grid(row=1,column=1)
    tk.Label(root,text="sec").grid(row=1,column=2)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.grid(row=2, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    root.pack_slaves()

    progress_step = float(100.0/len(runTime))
    for team in runTime:
        root.update()
        sleep(1) # lauch task
        progress += progress_step
        remainingTime=int(remainingTime)-1
        tk.Label(root,text=remainingTime).grid(row=1,column=1)
        progress_var.set(progress)
    return 0

##root = tk.Tk()
##root.mainloop()
