#!/bin/sh
# Сравнение со штатными инструментами Ubuntu (apt-cache, apt-rdepends,
# debtree). Запускаются в Docker-контейнере Ubuntu 24.04.
cd "$(dirname "$0")/.."
OUT=$(mktemp -d)
URL=http://archive.ubuntu.com/ubuntu

docker run --rm -v "$OUT:/out" ubuntu:24.04 sh -c '
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null
apt-get install -y -qq apt-rdepends debtree >/dev/null 2>&1
for p in curl base-files openssh-client; do
    apt-cache depends $p > /out/$p.depends
    apt-rdepends $p 2>/dev/null | grep -v "^ " | sort -u > /out/$p.rdepends
    debtree $p > /out/$p.debtree.dot 2>/dev/null
done' || exit 1

for spec in "curl 8.5.0-2ubuntu10" "base-files 13ubuntu10" \
            "openssh-client 1:9.6p1-3ubuntu13"; do
    set -- $spec
    python3 src/main.py --package "$1" --version "$2" --repo $URL \
        --max-depth 50 --output "$OUT/$1.svg" > "$OUT/$1.ours"
    grep '^  ' "$OUT/$1.ours" | grep -oE '^  [^ :]+|(->|,) [^ ,]+' \
        | sed 's/^[-> ,]*//' | grep -v '^(' | sort -u > "$OUT/$1.ours.set"
    echo "===== $1"
    echo "Наша программа: $(wc -l < "$OUT/$1.ours.set") пакетов," \
         "apt-rdepends: $(wc -l < "$OUT/$1.rdepends") пакетов"
    echo "Только у нас:" $(comm -23 "$OUT/$1.ours.set" "$OUT/$1.rdepends")
    echo "Только в apt-rdepends:" \
         $(comm -13 "$OUT/$1.ours.set" "$OUT/$1.rdepends")
    echo
done
echo "Полные результаты: $OUT"
