#!/bin/sh
# Оба параметра
cd "$(dirname "$0")/.."
echo "exit" | python3 src/main.py --vfs data/myfs.zip --script scripts/start.txt
