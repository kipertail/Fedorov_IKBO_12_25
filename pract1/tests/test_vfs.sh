#!/bin/sh
# Только --vfs: имя VFS в приглашении
cd "$(dirname "$0")/.."
sh tests/make_vfs.sh
echo "conf-dump" | python3 src/main.py --vfs data/multi.zip
