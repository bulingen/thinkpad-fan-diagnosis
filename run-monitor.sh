#!/usr/bin/env bash
# Run the temp+fan monitor from this folder (double-click or: ./run-monitor.sh)
cd "$(dirname "$0")"
exec python3 thinkpad-temp-fan-monitor.py
