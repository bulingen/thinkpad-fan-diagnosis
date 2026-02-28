#!/usr/bin/env python3
"""Small ThinkPad temp + fan monitor. Updates every 2s from /proc. Minimal CPU."""

import tkinter as tk
import os

THERMAL = "/proc/acpi/ibm/thermal"
FAN = "/proc/acpi/ibm/fan"
INTERVAL_MS = 2000


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except (OSError, PermissionError):
        return "(need root or run as root)"


def update(label):
    if not os.path.exists(THERMAL) or not os.path.exists(FAN):
        label.config(text="ThinkPad ACPI not found.")
        label.after(INTERVAL_MS, lambda: update(label))
        return
    thermal = read(THERMAL)
    fan = read(FAN)
    text = f"{thermal}\n\n{fan}"
    label.config(text=text)
    label.after(INTERVAL_MS, lambda: update(label))


def main():
    root = tk.Tk()
    root.title("ThinkPad temp & fan")
    root.resizable(True, True)
    root.minsize(280, 120)
    label = tk.Label(root, text="...", font=("Monospace", 11), justify=tk.LEFT, padx=12, pady=12)
    label.pack(expand=True, fill=tk.BOTH)
    update(label)
    root.mainloop()


if __name__ == "__main__":
    main()
