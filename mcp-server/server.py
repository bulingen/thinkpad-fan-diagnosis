#!/usr/bin/env python3
"""
MCP server for ThinkPad fan diagnosis.
Exposes read-only tools: thermal, fan, top processes, thinkfan config, curve reference.
Agents use these to reason and suggest a tailored fan curve; they never write files.
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "thinkfan-diagnosis",
)
mcp.description = "Read thermal, fan, processes and thinkfan config for diagnosis and curve suggestions."

# Paths (work when Cursor runs server from project root or from mcp-server/)
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
_THERMAL = Path("/proc/acpi/ibm/thermal")
_FAN = Path("/proc/acpi/ibm/fan")
_THINKFAN_CONFIG = Path("/etc/thinkfan.yaml")
_CURVE_REF = _PROJECT_ROOT / "thinkpad-fan-control.md"


def _read(path: Path, default: str = "(unreadable)") -> str:
    try:
        return path.read_text().strip()
    except OSError:
        return default


@mcp.tool()
def get_thermal() -> str:
    """Read current thermal readings from the ThinkPad. First three numbers are temps in °C (sensors 0,1,2); highest matters. -128 = invalid."""
    return _read(_THERMAL)


@mcp.tool()
def get_fan() -> str:
    """Read current fan status: level and speed. Use with thermal to see if fan matches temperature."""
    return _read(_FAN)


@mcp.tool()
def get_top_processes(n: int = 10) -> str:
    """Top N processes by CPU usage (default 10). Helps see if something is spiking and causing heat."""
    import subprocess
    try:
        out = subprocess.run(
            ["ps", "-eo", "pcpu,comm", "--sort=-pcpu", "--no-headers"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode != 0:
            return out.stderr or "(ps failed)"
        lines = (out.stdout or "").strip().split("\n")[: max(1, int(n))]
        return "\n".join(lines) if lines else "(no output)"
    except Exception as e:
        return str(e)


@mcp.tool()
def get_thinkfan_config() -> str:
    """Read current thinkfan config from /etc/thinkfan.yaml. Use to see current levels and suggest changes."""
    return _read(_THINKFAN_CONFIG)


@mcp.tool()
def get_curve_reference() -> str:
    """Reference doc with example level blocks (level-1-friendly, gradual ramp). Use as inspiration only; suggest a thought-through curve from live data."""
    return _read(_CURVE_REF)


if __name__ == "__main__":
    mcp.run(transport="stdio")
