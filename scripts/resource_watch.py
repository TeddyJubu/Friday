#!/usr/bin/env python3
"""Lightweight resource monitor.

Exit codes:
  0 = OK
  2 = Threshold exceeded

Prints one-line summary + JSON details.
"""

import json
import os
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class Thresholds:
    max_load_1: float = float(os.environ.get("RW_MAX_LOAD_1", "2.0"))
    max_mem_used_pct: float = float(os.environ.get("RW_MAX_MEM_USED_PCT", "85"))
    min_mem_avail_mb: int = int(os.environ.get("RW_MIN_MEM_AVAIL_MB", "2048"))
    max_disk_used_pct: float = float(os.environ.get("RW_MAX_DISK_USED_PCT", "80"))


def read_loadavg():
    with open("/proc/loadavg", "r", encoding="utf-8") as f:
        parts = f.read().strip().split()
    return float(parts[0]), float(parts[1]), float(parts[2])


def read_meminfo():
    mem_total_kb = None
    mem_avail_kb = None
    with open("/proc/meminfo", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                mem_total_kb = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                mem_avail_kb = int(line.split()[1])
    if mem_total_kb is None or mem_avail_kb is None:
        raise RuntimeError("Could not parse /proc/meminfo")
    used_kb = mem_total_kb - mem_avail_kb
    used_pct = (used_kb / mem_total_kb) * 100
    return {
        "total_mb": mem_total_kb / 1024,
        "avail_mb": mem_avail_kb / 1024,
        "used_pct": used_pct,
    }


def read_disk(path: str = "/"):
    du = shutil.disk_usage(path)
    used_pct = (du.used / du.total) * 100
    return {
        "path": path,
        "total_gb": du.total / (1024**3),
        "free_gb": du.free / (1024**3),
        "used_pct": used_pct,
    }


def top_procs(limit: int = 5):
    # Very small + robust: use ps
    out = subprocess.check_output([
        "bash",
        "-lc",
        f"ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n {limit+1}",
    ], text=True)
    return out.strip().splitlines()


def main():
    th = Thresholds()
    l1, l5, l15 = read_loadavg()
    mem = read_meminfo()
    disk = read_disk("/")

    breaches = []
    if l1 > th.max_load_1:
        breaches.append({"metric": "load1", "value": l1, "threshold": th.max_load_1})
    if mem["used_pct"] > th.max_mem_used_pct:
        breaches.append({"metric": "mem_used_pct", "value": mem["used_pct"], "threshold": th.max_mem_used_pct})
    if mem["avail_mb"] < th.min_mem_avail_mb:
        breaches.append({"metric": "mem_avail_mb", "value": mem["avail_mb"], "threshold": th.min_mem_avail_mb})
    if disk["used_pct"] > th.max_disk_used_pct:
        breaches.append({"metric": "disk_used_pct", "value": disk["used_pct"], "threshold": th.max_disk_used_pct})

    payload = {
        "load": {"1": l1, "5": l5, "15": l15},
        "mem": mem,
        "disk": disk,
        "breaches": breaches,
        "top_by_mem": top_procs(6),
        "thresholds": {
            "max_load_1": th.max_load_1,
            "max_mem_used_pct": th.max_mem_used_pct,
            "min_mem_avail_mb": th.min_mem_avail_mb,
            "max_disk_used_pct": th.max_disk_used_pct,
        },
    }

    summary = (
        f"load1={l1:.2f} mem_used={mem['used_pct']:.1f}% mem_avail={mem['avail_mb']:.0f}MB "
        f"disk_used={disk['used_pct']:.1f}%"
    )
    print(summary)
    print(json.dumps(payload, indent=2))

    raise SystemExit(2 if breaches else 0)


if __name__ == "__main__":
    main()
