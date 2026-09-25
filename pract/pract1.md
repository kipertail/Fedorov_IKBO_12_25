# Практическое занятие №1. Введение, основы работы в командной строке

**Цель:** научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

**Система:** Arch Linux, bash. Все скрипты проверены в ShellCheck, предупреждений нет.

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

```
[kipertail@arch pract]$ grep -o '^[^:]*' /etc/passwd | sort
alpm
avahi
bin
daemon
dbus
dhcpcd
flatpak
ftp
git
http
kipertail
mail
named
nobody
nvidia-persistenced
pcscd
polkitd
postgres
qemu
root
sddm
systemd-coredump
systemd-imds
systemd-journal-remote
systemd-network
systemd-oom
systemd-resolve
systemd-timesync
tpws
tss
uuidd
zapret2
```

## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов.

```
[kipertail@arch pract]$ grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -nr | head -5
255 reserved
147 bit-emu
146 homa
145 nsh
144 aggfrag
```

## Задача 3

Написать программу banner средствами bash для вывода текстов в рамке (размер баннера должен меняться!).

Скрипт `banner`:

```bash
#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 text" >&2
    exit 1
fi

text="$*"
border=$(printf '%*s' "$(( ${#text} + 2 ))" '' | tr ' ' '-')

printf '+%s+\n' "$border"
printf '| %s |\n' "$text"
printf '+%s+\n' "$border"
```

```
[kipertail@arch pract]$ chmod +x banner
[kipertail@arch pract]$ shellcheck banner
[kipertail@arch pract]$ ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Скрипт `idents`:

```bash
#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 file" >&2
    exit 1
fi

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | tr '\n' ' '
echo
```

Тестовый файл `hello.c`:

```c
#include <stdio.h>

int main(void) {
    printf("hello world\n");
    return 0;
}
```

```
[kipertail@arch pract]$ chmod +x idents
[kipertail@arch pract]$ shellcheck idents
[kipertail@arch pract]$ ./idents hello.c
h hello include int main n printf return stdio void world
```

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Скрипт `reg`:

```bash
#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 file" >&2
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: $1 not found" >&2
    exit 1
fi

sudo install -m 755 "$1" /usr/local/bin/
echo "$1 registered in /usr/local/bin"
```

```
[kipertail@arch pract]$ chmod +x reg
[kipertail@arch pract]$ shellcheck reg
[kipertail@arch pract]$ ./reg banner
[sudo] password for kipertail:
banner registered in /usr/local/bin
```

## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

Скрипт `checkcomment`:

```bash
#!/bin/bash
dir="${1:-.}"

find "$dir" -type f \( -name '*.c' -o -name '*.js' -o -name '*.py' \) -print0 |
while IFS= read -r -d '' file; do
    first=$(head -n 1 "$file")
    case "$file" in
        *.py) pattern='^[[:space:]]*#' ;;
        *)    pattern='^[[:space:]]*(//|/\*)' ;;
    esac

    if [[ $first =~ $pattern ]]; then
        echo "$file: comment found"
    else
        echo "$file: NO comment"
    fi
done
```

```
[kipertail@arch pract]$ chmod +x checkcomment
[kipertail@arch pract]$ shellcheck checkcomment
[kipertail@arch pract]$ ./checkcomment
./hello.c: NO comment
```

## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

Скрипт `dups`:

```bash
#!/bin/bash
dir="${1:-.}"

find "$dir" -type f -exec md5sum {} + | sort | uniq -w32 --all-repeated=separate
```

```
[kipertail@arch pract]$ chmod +x dups
[kipertail@arch pract]$ shellcheck dups
[kipertail@arch pract]$ mkdir t && echo abc > t/a && echo abc > t/b && echo xyz > t/c
[kipertail@arch pract]$ ./dups t
0bee89b07a248e27c83fc3d5951213c1  t/a
0bee89b07a248e27c83fc3d5951213c1  t/b
```

## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

Скрипт `archext`:

```bash
#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 extension [dir]" >&2
    exit 1
fi

ext="$1"
dir="${2:-.}"
archive="archive_${ext}.tar"

find "$dir" -type f -name "*.${ext}" -print0 | tar -cvf "$archive" --null -T -
```

```
[kipertail@arch pract]$ chmod +x archext
[kipertail@arch pract]$ shellcheck archext
[kipertail@arch pract]$ ./archext c
./hello.c
```

## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

Скрипт `sp2tab`:

```bash
#!/bin/bash
if [ $# -ne 2 ]; then
    echo "Usage: $0 input output" >&2
    exit 1
fi

if [ "$1" = "$2" ]; then
    echo "Error: input and output must differ" >&2
    exit 1
fi

sed 's/    /\t/g' "$1" > "$2"
```

```
[kipertail@arch pract]$ chmod +x sp2tab
[kipertail@arch pract]$ shellcheck sp2tab
[kipertail@arch pract]$ ./sp2tab hello.c hello_new.c
```

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.

Скрипт `emptytxt`:

```bash
#!/bin/bash
if [ $# -ne 1 ] || [ ! -d "$1" ]; then
    echo "Usage: $0 directory" >&2
    exit 1
fi

find "$1" -maxdepth 1 -type f -name '*.txt' -empty -printf '%f\n'
```

```
[kipertail@arch pract]$ chmod +x emptytxt
[kipertail@arch pract]$ shellcheck emptytxt
[kipertail@arch pract]$ touch t/e1.txt t/e2.txt; ./emptytxt t
e2.txt
e1.txt
```

## Выводы

В ходе работы были изучены основные утилиты командной строки Linux: `grep`, `sort`, `awk`, `sed`, `tr`, `head`, `find`, `tar`, `md5sum`, `install`. Задачи решались объединением небольших утилит в конвейер через `|`, где каждая утилита выполняет одно действие и передаёт текст следующей. Были написаны bash-скрипты с проверкой аргументов, выставлением прав доступа (`chmod`, `install -m 755`) и регистрацией команды в `/usr/local/bin`, после чего она доступна из любого каталога. Все скрипты проверены статическим анализатором ShellCheck.

При сравнении с командной строкой Windows (cmd) у большинства команд есть аналоги: `dir` вместо `ls`, `type` вместо `cat`, `findstr` вместо `grep`, `copy` вместо `cp`, `certutil -hashfile` вместо `md5sum`. Однако набор стандартных утилит в Linux значительно шире, и они лучше приспособлены к совместной работе через конвейеры. В PowerShell конвейеры также есть, но по ним передаются объекты, а не текст.