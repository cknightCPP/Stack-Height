import tkinter as tk
from tkinter import filedialog
import os
def browse():
    app = tk.Tk()
    app.withdraw()
    my_filetypes = [('all files', '.*'), ('CSV', '.csv')]
    CondPath = filedialog.askopenfilename(parent=app,
                                    initialdir=os.getcwd(),
                                    title="Please select the Conditions file:",
                                    filetypes=my_filetypes)
    GeomPath = filedialog.askopenfilename(parent=app,
                                    initialdir=os.getcwd(),
                                    title="Please select the Geometry file:",
                                    filetypes=my_filetypes)
    StackPath = filedialog.askopenfilename(parent=app,
                                        initialdir=os.getcwd(),
                                        title="Please select the Stack file:",
                                        filetypes=my_filetypes)
    RecPath = filedialog.askopenfilename(parent=app,
                                    initialdir=os.getcwd(),
                                    title="Please select the Receptor file:",
                                    filetypes=my_filetypes)
    return CondPath, GeomPath, StackPath, RecPath
def dig():
    cwd = f"{os.getcwd()}"
    print(cwd)
    StackPath = cwd + r"\csv\StackSH.csv"
    CondPath = cwd + r"\csv\CondSH.csv"
    GeomPath = cwd + r"\csv\BuildingSH.csv"
    RecPath = cwd + r"\csv\RecSH.csv"
    return CondPath,GeomPath,StackPath,RecPath
def imp(a):
    if a > 2:
        CondPath,GeomPath,StackPath,RecPath = browse()
        return CondPath,GeomPath,StackPath,RecPath
    else:
        CondPath,GeomPath,StackPath,RecPath = dig()
        return CondPath,GeomPath,StackPath,RecPath