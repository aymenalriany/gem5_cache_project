#!/bin/bash
# ============================================================
# run_all.sh - Automated Simulation Runner
# Project: Evaluation of Cache Utilization for Different
#          Cache Associativities
# ============================================================
# Usage: bash run_all.sh [GEM5_PATH]
#   GEM5_PATH: Path to gem5 build directory
#              Default: ~/gem5/build/X86/gem5.opt
# ============================================================

set -e

# Configuration
GEM5_BIN="${1:-$HOME/gem5/build/X86/gem5.opt}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIGS_DIR="$PROJECT_DIR/configs"
PROGRAM_DIR="$PROJECT_DIR/program"
RESULTS_DIR="$PROJECT_DIR/results"
SOURCE_FILE="$PROGRAM_DIR/array_access.cpp"
BINARY_FILE="$PROGRAM_DIR/array_access"

echo "============================================================"
echo "  Cache Associativity Evaluation - Automated Runner"
echo "============================================================"
echo ""
echo "gem5 binary: $GEM5_BIN"
echo "Project dir: $PROJECT_DIR"
echo ""

# ====== Step 1: Verify gem5 exists ======
if [ ! -f "$GEM5_BIN" ]; then
    echo "[ERROR] gem5 binary not found at: $GEM5_BIN"
    echo "  Usage: bash run_all.sh /path/to/gem5.opt"
    exit 1
fi

# ====== Step 2: Compile the benchmark ======
echo "[Step 1] Compiling benchmark program..."
g++ -O1 -static -o "$BINARY_FILE" "$SOURCE_FILE"
echo "  -> Compiled: $BINARY_FILE"
echo ""

# ====== Step 3: Create results directory ======
mkdir -p "$RESULTS_DIR"

# ====== Step 4: Run simulations ======
ASSOCIATIVITIES=("1way" "2way" "4way" "8way")

for ASSOC in "${ASSOCIATIVITIES[@]}"; do
    CONFIG="$CONFIGS_DIR/run_${ASSOC}.py"
    OUTPUT_DIR="$RESULTS_DIR/${ASSOC}"
    
    echo "------------------------------------------------------------"
    echo "[Step 2] Running simulation: ${ASSOC} associativity"
    echo "  Config: $CONFIG"
    echo "  Output: $OUTPUT_DIR"
    echo "------------------------------------------------------------"
    
    mkdir -p "$OUTPUT_DIR"
    
    $GEM5_BIN \
        --outdir="$OUTPUT_DIR" \
        "$CONFIG" \
        2>&1 | tee "$OUTPUT_DIR/simulation.log"
    
    echo ""
    echo "  -> Simulation complete for ${ASSOC}"
    echo ""
done

# ====== Step 5: Parse Results ======
echo "============================================================"
echo "[Step 3] Parsing simulation results..."
echo "============================================================"
python3 "$PROJECT_DIR/parse_results.py"

echo ""
echo "============================================================"
echo "  All simulations completed successfully!"
echo "  Results saved to: $RESULTS_DIR/"
echo "============================================================"
