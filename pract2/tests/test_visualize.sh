#!/bin/sh
# Визуализация графов зависимостей трёх пакетов Ubuntu и тестового графа
cd "$(dirname "$0")/.."
URL=http://archive.ubuntu.com/ubuntu

python3 src/main.py --package curl --version 8.5.0-2ubuntu10 \
    --repo $URL --max-depth 2 --output examples/curl.svg
echo
python3 src/main.py --package base-files --version 13ubuntu10 \
    --repo $URL --max-depth 3 --output examples/base-files.svg
echo
python3 src/main.py --package openssh-client --version 1:9.6p1-3ubuntu13 \
    --repo $URL --max-depth 2 --output examples/openssh-client.svg
echo
python3 src/main.py --test-mode --package A --repo tests/graphs/complex.txt \
    --max-depth 10 --output examples/test-complex.svg
echo
python3 src/main.py --test-mode --reverse --package E \
    --repo tests/graphs/reverse.txt --max-depth 10 \
    --output examples/test-reverse.svg
