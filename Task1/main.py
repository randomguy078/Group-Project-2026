#main code of the system
import tkinter as tk
from login_system import Login
from gui_main import System

def start():
    main_window = tk.Tk()
    System(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    tkroot = tk.Tk()
    Login(tkroot, start)
    tkroot.mainloop()
