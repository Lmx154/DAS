# main.py

import tkinter as tk
from gui import SerialMonitorApp

def main():
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
