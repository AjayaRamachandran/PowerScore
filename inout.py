import tkinter as tk
from tkinter import filedialog
import subprocess

def importFile():
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    return filename

def showOutput(filename):
    subprocess.Popen(["notepad.exe", filename], shell=True)