"""
gem5 Configuration: 1-Way (Direct-Mapped) Cache
Project: Evaluation of Cache Utilization for Different Cache Associativities
"""

import m5
from m5.objects import *
import os

# ====== System Setup ======
system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# ====== CPU ======
system.cpu = TimingSimpleCPU()

# ====== L1 Caches (1-Way = Direct-Mapped) ======
system.cpu.icache = Cache(
    size="32kB",
    assoc=1,
    tag_latency=1,
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20,
)

system.cpu.dcache = Cache(
    size="32kB",
    assoc=1,
    tag_latency=1,
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20,
)

# ====== Buses ======
system.l2bus = L2XBar()
system.membus = SystemXBar()

# ====== Cache Hierarchy Connections ======
# CPU -> L1 Caches
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# L1 Caches -> L2 Bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

# L2 Cache
system.l2cache = Cache(
    size="256kB",
    assoc=8,
    tag_latency=10,
    data_latency=10,
    response_latency=10,
    mshrs=20,
    tgts_per_mshr=12,
)
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

# System port
system.system_port = system.membus.cpu_side_ports

# ====== Memory Controller ======
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# ====== Process (SE Mode) ======
binary_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "program", "array_access"
)
binary_path = os.path.abspath(binary_path)

process = Process()
process.cmd = [binary_path]

system.cpu.workload = process
system.cpu.createThreads()

# ====== Simulation ======
root = Root(full_system=False, system=system)
m5.instantiate()

print("=" * 60)
print("Starting 1-Way (Direct-Mapped) Cache Simulation")
print("L1 ICache: 32kB, assoc=1 | L1 DCache: 32kB, assoc=1")
print("L2 Cache: 256kB, assoc=8")
print("=" * 60)

exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")