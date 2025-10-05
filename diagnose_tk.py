#!/usr/bin/env python3
# Quick tkinter diagnostic
import sys, traceback
print("Python:", sys.version)
try:
    import tkinter as tk, tkinter.ttk as ttk
    root = tk.Tk()
    root.withdraw()
    print("tkinter OK. Tk version:", tk.TkVersion)
    root.destroy()
    sys.exit(0)
except Exception as e:
    print("tkinter FAILED")
    traceback.print_exc()
    sys.exit(2)
