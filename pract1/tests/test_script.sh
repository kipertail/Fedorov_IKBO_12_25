#!/bin/sh
# Только --script: выполнение стартового скрипта
cd "$(dirname "$0")/.."
echo "exit" | python3 src/main.py --script scripts/start.txt
