#!/bin/sh
# Скрипт с ошибками: ошибочные строки пропускаются
cd "$(dirname "$0")/.."
echo "exit" | python3 src/main.py --vfs data/myfs.zip --script scripts/start_errors.txt
