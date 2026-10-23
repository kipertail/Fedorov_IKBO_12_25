#!/bin/sh
# Загрузка VFS: VFS с несколькими файлами
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
printf 'vfs-info\nls\nexit\n' | python3 src/main.py --vfs data/multi.zip
