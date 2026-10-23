#!/bin/sh
# Оба параметра
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
echo "exit" | python3 src/main.py --vfs data/multi.zip --script scripts/start.txt
