#!/bin/sh
# Запуск без параметров: значения по умолчанию
cd "$(dirname "$0")/.."
echo "conf-dump" | python3 src/main.py
