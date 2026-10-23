#!/bin/sh
# Скрипт с ошибками: ошибочные строки пропускаются
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
echo "exit" | python3 src/main.py --vfs data/multi.zip --script scripts/start_errors.txt
