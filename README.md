# RTL and SoC Design Verification Portfolio

I build report-backed RTL and verification projects with SystemVerilog, UVM, Verilator, PyTorch, C/C++/SystemC reference models, assertions, formal checks, Python automation, and open-source implementation tools. The portfolio is deliberately separated by verification scope rather than repeating the same claims across projects.

<!-- BEGIN GENERATED PORTFOLIO -->
| Project | Primary specialty | Selected measured evidence | Review |
| --- | --- | --- | --- |
| [RISC-V Chiplet SoC](https://github.com/ed766/ucie_chiplet_soc) | Firmware-driven subsystem integration, DMA, UPF, low power, CDC | `70 / 70` stable; `85 / 85` GCC/ISS; `26 / 26` power; `4 / 4` CDC | [Metrics](https://github.com/ed766/ucie_chiplet_soc/blob/main/docs/project_metrics.md) · [CI](https://github.com/ed766/ucie_chiplet_soc/actions) · [v2.0.1](https://github.com/ed766/ucie_chiplet_soc/releases/tag/v2.0.1) |
| [AXI4 L1 Cache DV](https://github.com/ed766/AXI4-L1-Cache-DV) | Cache microarchitecture, C++ replay, SECDED RAS, MSI coherence, RVWMO litmus checking | `22 / 22` directed; `127 / 127` replay; `64 / 64` coherent coverage; `48 / 48` coherent crosses; `17 / 17` coherent RTL mutations | [Metrics](https://github.com/ed766/AXI4-L1-Cache-DV/blob/main/docs/project_metrics.md) · [CI](https://github.com/ed766/AXI4-L1-Cache-DV/actions) · [v0.6.0](https://github.com/ed766/AXI4-L1-Cache-DV/releases/tag/v0.6.0) |
| [AXI4 QoS Fabric DV](https://github.com/ed766/AXI4-QoS-Fabric-DV) | Reusable UVM/VIP, AXI concurrency, SystemC replay, QoS/fairness | `8 / 8` UVM; `130 / 130` replay; `24 / 24` advanced crosses; `72 / 72` QoS points | [Metrics](https://github.com/ed766/AXI4-QoS-Fabric-DV/blob/main/docs/project_metrics.md) · [CI](https://github.com/ed766/AXI4-QoS-Fabric-DV/actions) · [v0.4.1](https://github.com/ed766/AXI4-QoS-Fabric-DV/releases/tag/v0.4.1) |
| [INT8 Tensor Accelerator DV](https://github.com/ed766/INT8-Tensor-Accelerator-DV) | PyTorch-to-RTL checking, quantization, AXI integration, RV32I offload | `130 / 130` exact comparisons; `40 / 40` benchmark; `25 / 25` correctness; `5 / 5` mutations | [Metrics](https://github.com/ed766/INT8-Tensor-Accelerator-DV/blob/main/docs/project_metrics.md) · [CI](https://github.com/ed766/INT8-Tensor-Accelerator-DV/actions) · [v0.4.1](https://github.com/ed766/INT8-Tensor-Accelerator-DV/releases/tag/v0.4.1) |
<!-- END GENERATED PORTFOLIO -->

## Skills Matrix

| Area | Chiplet SoC | L1 cache | QoS fabric | INT8 accelerator |
| --- | --- | --- | --- | --- |
| System integration | RV32 firmware, APB MMIO, DMA, AES service | CPU/cache/AXI memory path plus bounded two-cache MSI | Four-initiator/four-target shared fabric | GCC RV32I, APB/AXI control, and streaming INT8 offload |
| Verification methodology | Procedural closure plus supporting UVM/RAL | C++ trace replay and mutation-driven debug | Principal real-UVM lane and reusable AXI agents | Exact integer oracle and tagged scoreboard |
| Architecture depth | UPF, retention/isolation, async CDC | Replacement, maintenance, associativity, SECDED, SRAM BIST | IDs, out-of-order responses, QoS, aging, fairness | Signed MACs, requantization, ReLU, saturation |
| Independent models | Python/C transaction and CRC models | Cycle-independent C++ cache model | SystemC/TLM arbitration and routing model | PyTorch tensor and `nn.Linear` models |
| Evidence | Firmware, power, formal, CDC, coverage | Stress, C++ replay, RAS, MSI mutations, BIST | UVM, VIP self-test, QoS dashboard, CDC, formal | PyTorch differential checks, RV32 cycle benchmark, mutations, latency |

```mermaid
flowchart LR
  SOC["RISC-V chiplet\nfirmware + low power"] --> PORT["Hardware DV portfolio"]
  L1["AXI4 L1 cache\nmicroarchitecture + RAS"] --> PORT
  FAB["AXI4 QoS fabric\nUVM/VIP + concurrency"] --> PORT
  ML["INT8 tensor accelerator\nPyTorch + numerical DV"] --> PORT
```

All headline metrics are generated from checked-in canonical reports. These projects demonstrate open-source engineering evidence, not UCIe/AXI certification or commercial UPF, CDC, timing, and formal signoff.
