import tkinter as tk
from view import LMSView
from controller import LMSController

if __name__ == "__main__":
    root = tk.Tk()
    controller = LMSController()
    app = LMSView(root, controller)
    root.mainloop()
