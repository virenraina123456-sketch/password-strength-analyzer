#!/usr/bin/env python3
"""Simple Tkinter GUI with live feedback as you type."""
import tkinter as tk
from tkinter import ttk

from analyzer import analyze, generate_password

COLORS = ["#E5484D", "#E5484D", "#F5A623", "#2FB36D", "#148A55"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Analyzer")
        self.geometry("460x380")
        self.resizable(False, False)
        self.var = tk.StringVar()
        self.var.trace_add("write", lambda *_: self.update_view())

        ttk.Label(self, text="Enter a password:", font=("Segoe UI", 11)).pack(pady=(18, 4))
        self.entry = ttk.Entry(self, textvariable=self.var, show="•", width=40)
        self.entry.pack()
        self.show = tk.BooleanVar()
        ttk.Checkbutton(self, text="Show password", variable=self.show,
                        command=lambda: self.entry.config(show="" if self.show.get() else "•")).pack(pady=4)

        self.bar = ttk.Progressbar(self, length=380, maximum=4)
        self.bar.pack(pady=8)
        self.level = tk.Label(self, text="", font=("Segoe UI", 16, "bold"))
        self.level.pack()
        self.info = tk.Label(self, text="", font=("Segoe UI", 10), fg="#5B6B7F")
        self.info.pack(pady=4)
        self.tips = tk.Label(self, text="", font=("Segoe UI", 10), justify="left", wraplength=400)
        self.tips.pack(pady=6)
        ttk.Button(self, text="Generate strong password",
                   command=lambda: self.var.set(generate_password())).pack(pady=8)

    def update_view(self):
        pw = self.var.get()
        if not pw:
            self.bar["value"] = 0
            self.level.config(text="")
            self.info.config(text="")
            self.tips.config(text="")
            return
        r = analyze(pw)
        self.bar["value"] = r.score + 1 if pw else 0
        self.level.config(text=r.level, fg=COLORS[r.score])
        self.info.config(text=f"{r.entropy_bits} bits  |  crack time: {r.crack_time}")
        self.tips.config(text="\n".join("• " + t for t in r.feedback))


if __name__ == "__main__":
    App().mainloop()
