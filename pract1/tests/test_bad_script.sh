#!/bin/sh
# Несуществующий стартовый скрипт
cd "$(dirname "$0")/.."
echo "exit" | python3 src/main.py --script scripts/missing.txt
