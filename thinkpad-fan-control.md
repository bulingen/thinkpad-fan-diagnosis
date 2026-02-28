# ThinkPad P1 Gen 8 – Fan control (thinkfan)

Short reference so you don’t forget.

---

## What’s in place

- **thinkpad_acpi** fan control: `/etc/modprobe.d/thinkpad_acpi.conf` → `options thinkpad_acpi fan_control=1` (reboot after adding).
- **thinkfan** config: `/etc/thinkfan.yaml`. Service: `thinkfan` (enabled at boot).

---

## Check temperature

```bash
cat /proc/acpi/ibm/thermal
```

First three numbers (°C) are what thinkfan uses; highest one matters. `-128` = invalid, ignore.

---

## Fan level configs

### Level-1-friendly (quiet for longer at low speed)

If you like level 1 and want it for a wider range (starts earlier, stays longer):

```yaml
levels:
  - [0, 0, 46]
  - [1, 44, 66]
  - [2, 64, 70]
  - ["level auto", 68, 78]
  - ["level disengaged", 72, 255]
```

- 0–46 °C: fan at 0.
- 44–66 °C: level 1 (low; wide band).
- 64–70 °C: level 2.
- 68–78 °C: auto.
- 72+ °C: full.

### Gradual ramp (if level 1 feels too short)

```yaml
levels:
  - [0, 0, 52]
  - [1, 50, 58]
  - [2, 56, 64]
  - ["level auto", 62, 78]
  - ["level disengaged", 72, 255]
```

After editing `/etc/thinkfan.yaml`:

```bash
sudo systemctl restart thinkfan
```

---

## Useful commands

| What             | Command |
|------------------|--------|
| Fan control on?  | `cat /sys/module/thinkpad_acpi/parameters/fan_control` → `Y` |
| Temp now         | `cat /proc/acpi/ibm/thermal` |
| thinkfan status  | `sudo systemctl status thinkfan` |
| Test thinkfan    | `sudo thinkfan -n` (Ctrl+C to stop) |

---

*ThinkPad P1 Gen 8, Linux.*
