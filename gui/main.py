import tkinter as tk
from gui.controller import GameController


def run_gui() -> None:
    root = tk.Tk()
    GameController(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
