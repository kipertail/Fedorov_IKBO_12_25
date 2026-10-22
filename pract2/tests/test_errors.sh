#!/bin/sh
# Обработка ошибок для каждого параметра
cd "$(dirname "$0")/.."
URL=http://archive.ubuntu.com/ubuntu

run() {
    echo "===== $1"
    shift
    python3 src/main.py "$@"
    echo "код возврата: $?"
}

run "Нет обязательных параметров"
run "Недопустимое имя пакета" --package Curl! --repo $URL --version 1.0
run "Тестовый режим: имя не из заглавных букв" \
    --package curl --repo tests/graph1.txt --test-mode
run "repo не URL" --package curl --repo archive.ubuntu.com --version 1.0
run "Тестовый файл не найден" \
    --package A --repo tests/missing.txt --test-mode
run "Версия не задана" --package curl --repo $URL
run "Недопустимая версия" --package curl --repo $URL --version "1 0"
run "Неверное расширение output" \
    --package curl --repo $URL --version 1.0 --output graph.png
run "Папка output не существует" \
    --package curl --repo $URL --version 1.0 --output nodir/graph.svg
run "max-depth не число" \
    --package curl --repo $URL --version 1.0 --max-depth abc
run "max-depth меньше 1" \
    --package curl --repo $URL --version 1.0 --max-depth 0
run "Несколько ошибок сразу" \
    --package Bad! --repo ftp://x --version "" --output a.txt --max-depth -5
