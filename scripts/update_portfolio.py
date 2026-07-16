#!/usr/bin/env python3
"""Generate the public portfolio matrix from sibling canonical metrics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- BEGIN GENERATED PORTFOLIO -->"
END = "<!-- END GENERATED PORTFOLIO -->"


def metrics(path: Path) -> dict[str, str]:
    return {row["metric"]: row["value"] for row in csv.DictReader(path.open())}


def need(values: dict[str, str], *keys: str) -> None:
    missing = [key for key in keys if key not in values]
    if missing:
        raise SystemExit(f"Missing canonical metrics: {', '.join(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chiplet", type=Path, default=ROOT.parent / "ucie_chiplet_soc")
    parser.add_argument("--cache", type=Path, default=ROOT.parent / "axi_l1_cache_dv")
    parser.add_argument("--fabric", type=Path, default=ROOT.parent / "axi4_qos_fabric_dv")
    args = parser.parse_args()
    chiplet = metrics(args.chiplet / "chiplet_extension" / "reports" / "project_metrics.csv")
    cache = metrics(args.cache / "reports" / "project_metrics.csv")
    fabric = metrics(args.fabric / "reports" / "project_metrics.csv")
    need(chiplet, "stable_runs", "firmware_soc_scenarios", "low_power_proxy_targets", "integrated_async_cdc")
    need(cache, "directed_regression", "trace_replay", "interaction_coverage", "secded_ras_coverage")
    need(fabric, "uvm_runtime", "full_model_replay", "advanced_interaction_coverage", "sustained_qos_points")
    rows = [
        ("[RISC-V Chiplet SoC](https://github.com/ed766/ucie_chiplet_soc)",
         "Firmware-driven subsystem integration, DMA, UPF, low power, CDC",
         f"`{chiplet['stable_runs']}` stable; `{chiplet['firmware_soc_scenarios']}` firmware; "
         f"`{chiplet['low_power_proxy_targets']}` power; `{chiplet['integrated_async_cdc']}` CDC",
         "[Metrics](https://github.com/ed766/ucie_chiplet_soc/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/ucie_chiplet_soc/actions) · "
         "[v1.1.1](https://github.com/ed766/ucie_chiplet_soc/releases/tag/v1.1.1)"),
        ("[AXI4 L1 Cache DV](https://github.com/ed766/AXI4-L1-Cache-DV)",
         "Cache microarchitecture, C++ replay, replacement/error checking, SECDED RAS",
         f"`{cache['directed_regression']}` directed; `{cache['trace_replay']}` replay; "
         f"`{cache['interaction_coverage']}` crosses; `{cache['secded_ras_coverage']}` RAS",
         "[Metrics](https://github.com/ed766/AXI4-L1-Cache-DV/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/AXI4-L1-Cache-DV/actions) · "
         "[v0.3.2](https://github.com/ed766/AXI4-L1-Cache-DV/releases/tag/v0.3.2)"),
        ("[AXI4 QoS Fabric DV](https://github.com/ed766/AXI4-QoS-Fabric-DV)",
         "Reusable UVM/VIP, AXI concurrency, SystemC replay, QoS/fairness",
         f"`{fabric['uvm_runtime']}` UVM; `{fabric['full_model_replay']}` replay; "
         f"`{fabric['advanced_interaction_coverage']}` advanced crosses; `{fabric['sustained_qos_points']}` QoS points",
         "[Metrics](https://github.com/ed766/AXI4-QoS-Fabric-DV/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/AXI4-QoS-Fabric-DV/actions) · "
         "[v0.3.1](https://github.com/ed766/AXI4-QoS-Fabric-DV/releases/tag/v0.3.1)"),
    ]
    block = [START,
             "| Project | Primary specialty | Selected measured evidence | Review |",
             "| --- | --- | --- | --- |"]
    block.extend("| " + " | ".join(row) + " |" for row in rows)
    block.append(END)
    text = README.read_text()
    if START not in text or END not in text:
        raise SystemExit("README generated portfolio markers are missing")
    prefix, rest = text.split(START, 1)
    _, suffix = rest.split(END, 1)
    README.write_text(prefix + "\n".join(block) + suffix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
