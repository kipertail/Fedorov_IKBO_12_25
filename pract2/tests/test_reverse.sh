#!/bin/sh
# Обратные зависимости: кто зависит от заданного пакета
cd "$(dirname "$0")/.."

run() {
    echo "===== $1"
    shift
    python3 src/main.py --reverse "$@"
    echo
}

run "Тест: обратные зависимости E" --test-mode --package E \
    --repo tests/graphs/reverse.txt --max-depth 10
run "Тест: обратные зависимости E, глубина 1" --test-mode --package E \
    --repo tests/graphs/reverse.txt --max-depth 1
run "Тест: от A никто не зависит" --test-mode --package A \
    --repo tests/graphs/reverse.txt
run "Тест: цикл" --test-mode --package A --repo tests/graphs/cycle.txt
run "Тест: неописанный пакет X" --test-mode --package X \
    --repo tests/graphs/missing.txt
run "Тест: пакет не найден" --test-mode --package Z \
    --repo tests/graphs/reverse.txt
run "Ubuntu: кто зависит от libcurl4t64" \
    --package libcurl4t64 --version 8.5.0-2ubuntu10 \
    --repo http://archive.ubuntu.com/ubuntu --max-depth 2
