from averyutils import avery_logger
_log = avery_logger
try:
    import time, os
    import tkinter as tk
    from typing import *
except ImportError as e:
    print(e.name, "is not installed")
    _log.error(f"{e.name} not installed")

def askquestion(question: str = "do you like python?", option1: str="Yes", option2: str="No", title: Optional[str]="oh my friggin god ts title is so tuff boii lowk my 67 mangos and 41 mustards are strokin they shit"):
    """Open a small window asking a question with two button options."""
    root = tk._get_default_root()
    root.withdraw()

    result = {"answer": None}

    def choose(answer):
        result["answer"] = answer
        win.destroy()

    win = tk.Toplevel()
    win.title(title)
    win.geometry("300x150")
    win.resizable(False, False)

    tk.Label(win, text=question, wraplength=250, pady=20).pack()

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text=option1, width=10, command=lambda: choose(option1)).pack(side="left", padx=10)
    tk.Button(button_frame, text=option2, width=10, command=lambda: choose(option2)).pack(side="left", padx=10)

    # Make the window modal (wait for it to close)
    win.grab_set()
    win.wait_window()

    return result["answer"]