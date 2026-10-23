#!/bin/sh
# Сборка тестовых VFS (ZIP-архивов) из папок tests/vfs в папку data
set -e
cd "$(dirname "$0")/.."
mkdir -p data
out=$(pwd)/data
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT

for src in tests/vfs/*/; do
    name=$(basename "$src")
    cp -r "$src" "$build/$name"
done

# Двоичный файл и пустая папка создаются при сборке,
# чтобы не хранить их в репозитории
printf '\000\001\002\377\376' > "$build/deep/home/user/image.bin"
mkdir -p "$build/deep/tmp"

for dir in "$build"/*/; do
    name=$(basename "$dir")
    rm -f "data/$name.zip"
    (cd "$dir" && python3 -m zipfile -c "$out/$name.zip" ./*)
done

# Файл с неверным форматом для проверки ошибок загрузки
echo "это не zip-архив" > data/broken.zip
