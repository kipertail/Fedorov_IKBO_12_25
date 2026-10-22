#!/bin/sh
# Построение графа в тестовом режиме на разных тестовых репозиториях
cd "$(dirname "$0")/.."

run() {
    echo "===== $1"
    shift
    python3 src/main.py --test-mode "$@"
    echo
}

run "Цепочка, глубина 2" --package A --repo tests/graphs/chain.txt \
    --max-depth 2
run "Цепочка, глубина 10" --package A --repo tests/graphs/chain.txt \
    --max-depth 10
run "Цепочка от середины" --package C --repo tests/graphs/chain.txt
run "Цикл" --package A --repo tests/graphs/cycle.txt
run "Пакет зависит сам от себя" --package A --repo tests/graphs/self_loop.txt
run "Ромб" --package A --repo tests/graphs/diamond.txt
run "Короткий путь, глубина 2" --package A --repo tests/graphs/shortcut.txt \
    --max-depth 2
run "Неописанная зависимость" --package A --repo tests/graphs/missing.txt
run "Несколько циклов" --package A --repo tests/graphs/complex.txt \
    --max-depth 10
