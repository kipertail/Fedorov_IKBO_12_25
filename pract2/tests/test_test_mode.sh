#!/bin/sh
# Тестовый режим: граф из файла, пакеты — заглавные буквы
cd "$(dirname "$0")/.."
python3 src/main.py --package A --repo tests/graph1.txt --test-mode
