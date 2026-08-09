#!/usr/bin/env python3
"""Generate the public portfolio matrix from sibling canonical metrics."""

from __future__ import annotations

import argparse
import csv
import subprocess
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


def latest_release(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "tag", "--list", "v*", "--sort=-version:refname"],
        check=True,
        text=True,
        capture_output=True,
    )
    tags = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not tags:
        raise SystemExit(f"No versioned release tag found in {repo}")
    return tags[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chiplet", type=Path, default=ROOT.parent / "ucie_chiplet_soc")
    parser.add_argument("--cache", type=Path, default=ROOT.parent / "axi_l1_cache_dv")
    parser.add_argument("--fabric", type=Path, default=ROOT.parent / "axi4_qos_fabric_dv")
    parser.add_argument("--accelerator", type=Path, default=ROOT.parent / "int8_tensor_accelerator_dv")
    args = parser.parse_args()
    chiplet = metrics(args.chiplet / "chiplet_extension" / "reports" / "project_metrics.csv")
    cache = metrics(args.cache / "reports" / "project_metrics.csv")
    fabric = metrics(args.fabric / "reports" / "project_metrics.csv")
    accelerator = metrics(args.accelerator / "reports" / "project_metrics.csv")
    need(chiplet, "stable_runs", "compiled_firmware_scenarios", "low_power_proxy_targets", "integrated_async_cdc")
    need(cache, "directed_regression", "trace_replay", "interaction_coverage", "secded_ras_coverage")
    need(fabric, "uvm_runtime", "full_model_replay", "advanced_interaction_coverage", "sustained_qos_points")
    need(accelerator, "pytorch_rtl_scenarios", "interaction_coverage", "streaming_throughput", "rtl_mutations")
    chiplet_release = latest_release(args.chiplet)
    cache_release = latest_release(args.cache)
    fabric_release = latest_release(args.fabric)
    accelerator_release = latest_release(args.accelerator)
    rows = [
        ("[RISC-V Chiplet SoC](https://github.com/ed766/ucie_chiplet_soc)",
         "Firmware-driven subsystem integration, DMA, UPF, low power, CDC",
         f"`{chiplet['stable_runs']}` stable; `{chiplet['compiled_firmware_scenarios']}` GCC/ISS; "
         f"`{chiplet['low_power_proxy_targets']}` power; `{chiplet['integrated_async_cdc']}` CDC",
         "[Metrics](https://github.com/ed766/ucie_chiplet_soc/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/ucie_chiplet_soc/actions) · "
         f"[{chiplet_release}](https://github.com/ed766/ucie_chiplet_soc/releases/tag/{chiplet_release})"),
        ("[AXI4 L1 Cache DV](https://github.com/ed766/AXI4-L1-Cache-DV)",
         "Cache microarchitecture, C++ replay, replacement/error checking, SECDED RAS",
         f"`{cache['directed_regression']}` directed; `{cache['trace_replay']}` replay; "
         f"`{cache['interaction_coverage']}` crosses; `{cache['secded_ras_coverage']}` RAS",
         "[Metrics](https://github.com/ed766/AXI4-L1-Cache-DV/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/AXI4-L1-Cache-DV/actions) · "
         f"[{cache_release}](https://github.com/ed766/AXI4-L1-Cache-DV/releases/tag/{cache_release})"),
        ("[AXI4 QoS Fabric DV](https://github.com/ed766/AXI4-QoS-Fabric-DV)",
         "Reusable UVM/VIP, AXI concurrency, SystemC replay, QoS/fairness",
         f"`{fabric['uvm_runtime']}` UVM; `{fabric['full_model_replay']}` replay; "
         f"`{fabric['advanced_interaction_coverage']}` advanced crosses; `{fabric['sustained_qos_points']}` QoS points",
         "[Metrics](https://github.com/ed766/AXI4-QoS-Fabric-DV/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/AXI4-QoS-Fabric-DV/actions) · "
         f"[{fabric_release}](https://github.com/ed766/AXI4-QoS-Fabric-DV/releases/tag/{fabric_release})"),
        ("[INT8 Tensor Accelerator DV](https://github.com/ed766/INT8-Tensor-Accelerator-DV)",
         "PyTorch-to-RTL numerical checking, quantization, assertions, mutation testing",
         f"`{accelerator['pytorch_rtl_scenarios']}` exact comparisons; "
         f"`{accelerator['interaction_coverage']}` crosses; "
         f"`{accelerator['streaming_throughput']}`; `{accelerator['rtl_mutations']}` mutations",
         "[Metrics](https://github.com/ed766/INT8-Tensor-Accelerator-DV/blob/main/docs/project_metrics.md) · "
         "[CI](https://github.com/ed766/INT8-Tensor-Accelerator-DV/actions) · "
         f"[{accelerator_release}](https://github.com/ed766/INT8-Tensor-Accelerator-DV/releases/tag/{accelerator_release})"),
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
