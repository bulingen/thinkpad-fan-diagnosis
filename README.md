# ThinkPad Linux fan tools (P1 Gen 8)

Small set of helpers for **thinkfan** and temperature/fan monitoring on ThinkPad P1 Gen 8 under Linux.

## What’s here

| File | Purpose |
|------|--------|
| **thinkpad-fan-control.md** | Notes and configs for thinkfan (levels, commands). Copy levels into `/etc/thinkfan.yaml` and `sudo systemctl restart thinkfan`. |
| **thinkpad-temp-fan-monitor.py** | Small GUI that shows current temps and fan status; updates every 2s. Low CPU. |
| **run-monitor.sh** | Launcher for the monitor. Run this to open the monitor window. |
| **mcp-server/** | MCP server for agentic fan diagnosis (see below). |

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

## Fan diagnosis (MCP)

An MCP server lets any compatible agent (e.g. Cursor) read thermal, fan, processes and thinkfan config, then suggest a **thought-through** fan curve and a one-liner to apply it (you run the command yourself).

**Setup (once):**

1. Create the MCP server venv and install deps (from the project root):
   ```bash
   python3 -m venv mcp-server/venv
   mcp-server/venv/bin/pip install -r mcp-server/requirements.txt
   ```
   `.cursor/mcp.json` is already set to use `mcp-server/venv/bin/python` and `mcp-server/server.py`. For another MCP client, run the server the same way (stdio) from the project root.

3. Restart Cursor (or your client) so it picks up the MCP server.

**Use:** Open this project in Cursor and ask e.g. *“What’s up with my fans?”* or *“Fans are loud – diagnose and suggest.”* The agent will call the MCP tools, reason from the data, suggest a tailored curve (inspired by but not limited to the doc), and give you a single command to apply it, e.g.:
`echo '...' | sudo tee /etc/thinkfan.yaml && sudo systemctl restart thinkfan`

The server only exposes read-only tools; it never writes files or restarts services.

## Version control

This folder is a git repo. Clone or pull as usual; no install step.
