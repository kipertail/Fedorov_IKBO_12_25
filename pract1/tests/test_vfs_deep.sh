#!/bin/sh
# Загрузка VFS: VFS с 3+ уровнями файлов и папок
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
printf 'vfs-info\nls\nexit\n' | python3 src/main.py --vfs data/deep.zip
