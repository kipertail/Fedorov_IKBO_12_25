#!/bin/sh
# Только --vfs: имя VFS в приглашении
cd "$(dirname "$0")/.."
echo "conf-dump" | python3 src/main.py --vfs data/myfs.zip
