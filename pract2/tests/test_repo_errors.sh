#!/bin/sh
# Ошибки при получении данных из репозитория
cd "$(dirname "$0")/.."
URL=http://archive.ubuntu.com/ubuntu

run() {
    echo "===== $1"
    shift
    python3 src/main.py "$@"
    echo "код возврата: $?"
}

run "Пакет не найден" --package no-such-package --repo $URL --version 1.0
run "Версия не найдена" --package curl --repo $URL --version 1.0
run "Репозиторий не найден (HTTP 404)" \
    --package curl --repo http://archive.ubuntu.com/nothing --version 1.0
run "Сервер недоступен" \
    --package curl --repo http://no-such-host.invalid --version 1.0
run "Тестовый режим: пакет не найден" \
    --package Z --repo tests/graph1.txt --test-mode
