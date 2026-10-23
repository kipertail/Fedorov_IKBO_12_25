#!/bin/sh
# Ошибки загрузки VFS: файл не найден, неверный формат
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
echo "vfs-info" | python3 src/main.py --vfs data/missing.zip
echo "vfs-info" | python3 src/main.py --vfs data/broken.zip
