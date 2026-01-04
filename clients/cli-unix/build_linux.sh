#!/bin/bash

# Configuration
RUST_DIR="logic"
CPP_DIR="ui"
OUT_EXE="cyber_term"
# In Linux/Unix, static libs usually end in .a
RUST_LIB="$RUST_DIR/target/release/libcyber_core.a"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=================================================="
echo "    HYBRID CLIENT BUILDER (Linux/Unix)"
echo "=================================================="

# 1. Check Dependencies
if ! command -v g++ &> /dev/null; then
    echo -e "${RED}[!] Error: g++ not found.${NC}"
    exit 1
fi

if ! command -v cargo &> /dev/null; then
    echo -e "${RED}[!] Error: cargo not found.${NC}"
    exit 1
fi

# 2. Build Rust Static Library
echo -e "\n${GREEN}[1/2] Compiling Rust Logic...${NC}"
cd "$RUST_DIR" || exit

# Linux builds use the default target
cargo build --release --quiet

if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Rust build failed.${NC}"
    exit 1
fi
cd ..

# 3. Compile C++ and Link
echo -e "\n${GREEN}[2/2] Compiling C++ UI and Linking...${NC}"

# -lpthread -ldl -lm are standard libraries required by Rust on Linux
g++ "$CPP_DIR/main.cpp" -o "$OUT_EXE" \
    "$RUST_LIB" \
    -lpthread -ldl -lm

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}[SUCCESS] Created ./$OUT_EXE${NC}"
    echo "Run it with: ./$OUT_EXE"
else
    echo -e "\n${RED}[FAIL] Linking failed.${NC}"
    exit 1
fi