#!/usr/bin/env python3
"""
parse_results.py - Cache Simulation Results Parser
Project: Evaluation of Cache Utilization for Different Cache Associativities

Parses gem5 stats.txt files to extract cache performance metrics
and generates a comparative summary table.
"""

import os
import re
import sys

# Project paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

# Associativities to analyze
CONFIGS = [
    {"name": "1-Way (Direct-Mapped)", "dir": "1way", "assoc": 1},
    {"name": "2-Way Set-Associative", "dir": "2way", "assoc": 2},
    {"name": "4-Way Set-Associative", "dir": "4way", "assoc": 4},
    {"name": "8-Way Set-Associative", "dir": "8way", "assoc": 8},
]

# Stats patterns to extract from stats.txt
STAT_PATTERNS = {
    # L1 Data Cache
    "dcache_hits":         r"system\.cpu\.dcache\.overallHits::total\s+(\d+)",
    "dcache_misses":       r"system\.cpu\.dcache\.overallMisses::total\s+(\d+)",
    "dcache_miss_rate":    r"system\.cpu\.dcache\.overallMissRate::total\s+([\d.]+)",
    "dcache_accesses":     r"system\.cpu\.dcache\.overallAccesses::total\s+(\d+)",
    # L1 Instruction Cache
    "icache_hits":         r"system\.cpu\.icache\.overallHits::total\s+(\d+)",
    "icache_misses":       r"system\.cpu\.icache\.overallMisses::total\s+(\d+)",
    "icache_miss_rate":    r"system\.cpu\.icache\.overallMissRate::total\s+([\d.]+)",
    "icache_accesses":     r"system\.cpu\.icache\.overallAccesses::total\s+(\d+)",
    # L2 Cache
    "l2cache_hits":        r"system\.l2cache\.overallHits::total\s+(\d+)",
    "l2cache_misses":      r"system\.l2cache\.overallMisses::total\s+(\d+)",
    "l2cache_miss_rate":   r"system\.l2cache\.overallMissRate::total\s+([\d.]+)",
    # Overall
    "sim_ticks":           r"simTicks\s+(\d+)",
    "sim_seconds":         r"simSeconds\s+([\d.e+-]+)",
    "num_instructions":    r"simInsts\s+(\d+)",
    "num_ops":             r"simOps\s+(\d+)",
}


def parse_stats_file(filepath):
    """Parse a gem5 stats.txt file and extract relevant metrics."""
    stats = {}
    try:
        with open(filepath, "r") as f:
            content = f.read()
        for key, pattern in STAT_PATTERNS.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1)
                try:
                    stats[key] = int(value)
                except ValueError:
                    stats[key] = float(value)
            else:
                stats[key] = None
    except FileNotFoundError:
        print(f"  [WARNING] Stats file not found: {filepath}")
        return None
    return stats


def calculate_amat(stats, l1_hit_time=1, l2_hit_time=10, mem_latency=100):
    """
    Calculate Average Memory Access Time (AMAT).
    AMAT = L1 Hit Time + L1 Miss Rate * (L2 Hit Time + L2 Miss Rate * Memory Latency)
    """
    l1_miss_rate = stats.get("dcache_miss_rate", 0) or 0
    l2_miss_rate = stats.get("l2cache_miss_rate", 0) or 0
    amat = l1_hit_time + l1_miss_rate * (l2_hit_time + l2_miss_rate * mem_latency)
    return amat


def print_separator(char="-", width=80):
    print(char * width)


def main():
    print()
    print("=" * 80)
    print("  Cache Associativity Evaluation - Results Summary")
    print("=" * 80)
    print()

    all_stats = []

    for config in CONFIGS:
        stats_path = os.path.join(RESULTS_DIR, config["dir"], "stats.txt")
        print(f"Parsing: {config['name']} ({stats_path})")

        stats = parse_stats_file(stats_path)
        if stats:
            stats["config"] = config
            stats["amat"] = calculate_amat(stats)
            all_stats.append(stats)
        else:
            print(f"  -> SKIPPED (no data)")

    if not all_stats:
        print("\n[ERROR] No simulation results found in:", RESULTS_DIR)
        print("  Run simulations first using: bash run_all.sh")
        sys.exit(1)

    # ====== Print Comparative Table ======
    print()
    print_separator("=")
    print(f"{'Metric':<35} ", end="")
    for s in all_stats:
        print(f"{'  ' + s['config']['dir']:>12}", end="")
    print()
    print_separator("=")

    # L1 DCache Metrics
    print("\n--- L1 Data Cache ---")
    for label, key in [
        ("D-Cache Accesses", "dcache_accesses"),
        ("D-Cache Hits", "dcache_hits"),
        ("D-Cache Misses", "dcache_misses"),
        ("D-Cache Miss Rate", "dcache_miss_rate"),
    ]:
        print(f"  {label:<33} ", end="")
        for s in all_stats:
            val = s.get(key)
            if val is None:
                print(f"{'N/A':>12}", end="")
            elif isinstance(val, float) and val < 1:
                print(f"{val:>11.6f}", end=" ")
            else:
                print(f"{val:>12}", end="")
        print()

    # L1 ICache Metrics
    print("\n--- L1 Instruction Cache ---")
    for label, key in [
        ("I-Cache Accesses", "icache_accesses"),
        ("I-Cache Hits", "icache_hits"),
        ("I-Cache Misses", "icache_misses"),
        ("I-Cache Miss Rate", "icache_miss_rate"),
    ]:
        print(f"  {label:<33} ", end="")
        for s in all_stats:
            val = s.get(key)
            if val is None:
                print(f"{'N/A':>12}", end="")
            elif isinstance(val, float) and val < 1:
                print(f"{val:>11.6f}", end=" ")
            else:
                print(f"{val:>12}", end="")
        print()

    # L2 Cache Metrics
    print("\n--- L2 Cache ---")
    for label, key in [
        ("L2 Hits", "l2cache_hits"),
        ("L2 Misses", "l2cache_misses"),
        ("L2 Miss Rate", "l2cache_miss_rate"),
    ]:
        print(f"  {label:<33} ", end="")
        for s in all_stats:
            val = s.get(key)
            if val is None:
                print(f"{'N/A':>12}", end="")
            elif isinstance(val, float) and val < 1:
                print(f"{val:>11.6f}", end=" ")
            else:
                print(f"{val:>12}", end="")
        print()

    # Overall Performance
    print("\n--- Overall Performance ---")
    for label, key in [
        ("Simulation Ticks", "sim_ticks"),
        ("Total Instructions", "num_instructions"),
        ("AMAT (cycles)", "amat"),
    ]:
        print(f"  {label:<33} ", end="")
        for s in all_stats:
            val = s.get(key)
            if val is None:
                print(f"{'N/A':>12}", end="")
            elif isinstance(val, float):
                print(f"{val:>12.4f}", end="")
            else:
                print(f"{val:>12}", end="")
        print()

    print()
    print_separator("=")

    # ====== Save to CSV ======
    csv_path = os.path.join(RESULTS_DIR, "comparison_results.csv")
    with open(csv_path, "w") as f:
        headers = ["Associativity",
                    "DCache_Accesses", "DCache_Hits", "DCache_Misses", "DCache_MissRate",
                    "ICache_Accesses", "ICache_Hits", "ICache_Misses", "ICache_MissRate",
                    "L2_Hits", "L2_Misses", "L2_MissRate",
                    "SimTicks", "Instructions", "AMAT"]
        f.write(",".join(headers) + "\n")

        for s in all_stats:
            row = [
                s["config"]["name"],
                s.get("dcache_accesses", ""),
                s.get("dcache_hits", ""),
                s.get("dcache_misses", ""),
                s.get("dcache_miss_rate", ""),
                s.get("icache_accesses", ""),
                s.get("icache_hits", ""),
                s.get("icache_misses", ""),
                s.get("icache_miss_rate", ""),
                s.get("l2cache_hits", ""),
                s.get("l2cache_misses", ""),
                s.get("l2cache_miss_rate", ""),
                s.get("sim_ticks", ""),
                s.get("num_instructions", ""),
                s.get("amat", ""),
            ]
            f.write(",".join(str(v) for v in row) + "\n")

    print(f"  Results saved to: {csv_path}")
    print()


if __name__ == "__main__":
    main()
