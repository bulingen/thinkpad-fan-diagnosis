# ThinkPad Linux fan tools (P1 Gen 8)

Small set of helpers for **thinkfan** and temperature/fan monitoring on ThinkPad P1 Gen 8 under Linux.

## What’s here

| File | Purpose |
|------|--------|
| **thinkpad-fan-control.md** | Notes and configs for thinkfan (levels, commands). Copy levels into `/etc/thinkfan.yaml` and `sudo systemctl restart thinkfan`. |
| **thinkpad-temp-fan-monitor.py** | Small GUI that shows current temps and fan status; updates every 2s. Low CPU. |
| **run-monitor.sh** | Launcher for the monitor. Run this to open the monitor window. |

## Run the temp/fan monitor

- **From terminal:**  
  `./run-monitor.sh`  
  or  
  `python3 thinkpad-temp-fan-monitor.py`

- **From file manager:**  
  Open this folder, right‑click `run-monitor.sh` → **Run** or **Execute** (or double‑click if your file manager runs executable scripts).

- **In background (close terminal, keep window):**  
  `nohup ./run-monitor.sh &`

If you see “(need root or run as root)”, run:  
`pkexec python3 thinkpad-temp-fan-monitor.py`

## Fan config

Edit `/etc/thinkfan.yaml` and paste one of the `levels:` blocks from **thinkpad-fan-control.md**. The “Level-1-friendly” config keeps the fan at level 1 for a wider temperature range. Then:

```bash
sudo systemctl restart thinkfan
```

## Version control

This folder is a git repo. Clone or pull as usual; no install step.
