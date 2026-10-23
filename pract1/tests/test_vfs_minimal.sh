#!/bin/sh
# Загрузка VFS: минимальная VFS (один файл)
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
printf 'vfs-info\nls\nexit\n' | python3 src/main.py --vfs data/minimal.zip
