#!/bin/sh
# Граф зависимостей пакетов из реального репозитория Ubuntu
cd "$(dirname "$0")/.."
URL=http://archive.ubuntu.com/ubuntu

python3 src/main.py --package curl --repo $URL --version 8.5.0-2ubuntu10 \
    --max-depth 2
echo
python3 src/main.py --package base-files --repo $URL --version 13ubuntu10 \
    --max-depth 3
