#!/bin/sh
# Стартовый скрипт с проверкой всех команд этапов 1-3
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
echo "exit" | python3 src/main.py --vfs data/deep.zip --script scripts/stage3.txt
