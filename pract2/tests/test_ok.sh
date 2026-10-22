#!/bin/sh
# Корректный запуск с реальным репозиторием
cd "$(dirname "$0")/.."
python3 src/main.py --package curl --repo http://archive.ubuntu.com/ubuntu \
    --version 8.5.0-2ubuntu10 --output graph.svg --max-depth 2
