task 1 
~~~
(.venv) [kipertail@arch pract]$ pip show matplotlib
....
Location: /home/kipertail/main/vuz/configuration management/pract/.venv/lib/python3.14/site-packages
Requires: contourpy, cycler, fonttools, kiwisolver, numpy, packaging, pillow, pyparsing, python-dateutil
Required-by: 
(.venv) [kipertail@arch pract]$ pip show -f matplotlib | head -30
Name: matplotlib
Version: 3.11.2
Summary: Python plotting package
Home-page: https://matplotlib.org
Author: John D. Hunter, Michael Droettboom
Author-email: Unknown <matplotlib-users@python.org>
License: License agreement for matplotlib versions 1.3.0 and later
 =========================================================

 1. This LICENSE AGREEMENT is between the Matplotlib Development Team
 ("MDT"), and the Individual or Organization ("Licensee") accessing and
 otherwise using matplotlib software in source or binary form and its
 associated documentation.

 2. Subject to the terms and conditions of this License Agreement, MDT
 hereby grants Licensee a nonexclusive, royalty-free, world-wide license
 to reproduce, analyze, test, perform and/or display publicly, prepare
 derivative works, distribute, and otherwise use matplotlib
 alone or in any derivative version, provided, however, that MDT's
 License Agreement and MDT's notice of copyright, i.e., "Copyright (c)
 2012- Matplotlib Development Team; All Rights Reserved" are retained in
 matplotlib  alone or in any derivative version prepared by
 Licensee.

 3. In the event Licensee prepares a derivative work that is based on or
 incorporates matplotlib or any part thereof, and wants to
 make the derivative work available to others as provided herein, then
 Licensee hereby agrees to include in any such work a brief summary of
 the changes made to matplotlib .

ERROR: Pipe to stdout was broken
(.venv) [kipertail@arch pract]$ ls .venv/lib/python3.14/site-packages/matplotlib-3.11.2.dist-info/
INSTALLER  LICENSE  METADATA  RECORD  REQUESTED  WHEEL
(.venv) [kipertail@arch pract]$ cat .venv/lib/python3.*/site-packages/matplotlib-*.dist-info/METADATA | less
(.venv) [kipertail@arch pract]$ 
~~~

|   |   |
|---|---|
|Поле|Что означает|
|`Metadata-Version`|Версия самого формата метаданных (спецификация Core Metadata)|
|`Name`, `Version`|Имя и версия пакета|
|`Summary`|Однострочное описание|
|`Author`, `Author-email`, `Maintainer`|Авторы и сопровождающие|
|`License`|Лицензия (у matplotlib своя, PSF-подобная)|
|`Project-URL`|Ссылки: сайт, документация, репозиторий, трекер задач|
|`Classifier`|Метки для каталога PyPI: стадия разработки, ОС, версии Python|
|`Requires-Python`|Какие версии Python поддерживаются|
|`Requires-Dist`|**Зависимости** с диапазонами: numpy, pillow, contourpy, cycler, fonttools, kiwisolver, packaging, pyparsing, python-dateutil|
|`Provides-Extra`|Дополнительные наборы, например `dev`; строки `Requires-Dist: ...; extra == "dev"` ставятся только при `pip install matplotlib[dev]`|
|`Description-Content-Type`|Формат описания ниже (обычно `text/markdown`)|
~~~
(.venv) [kipertail@arch pract]$ git clone --depth 1 https://github.com/matplotlib/matplotlib.git
Cloning into 'matplotlib'...
remote: Enumerating objects: 4657, done.
remote: Counting objects: 100% (4657/4657), done.
remote: Compressing objects: 100% (3811/3811), done.
remote: Total 4657 (delta 921), reused 3075 (delta 812), pack-reused 0 (from 0)
Receiving objects: 100% (4657/4657), 31.96 MiB | 9.96 MiB/s, done.
Resolving deltas: 100% (921/921), done.
(.venv) [kipertail@arch pract]$ cd matplotlib
(.venv) [kipertail@arch matplotlib]$ ls
CITATION.bib        LICENSE              ci               galleries      pyproject.toml  tox.ini
CITATION.cff        README.md            doc              lib            src
CODE_OF_CONDUCT.md  SECURITY.md          environment.yml  meson.build    subprojects
INSTALL.rst         azure-pipelines.yml  extern           meson.options  tools
(.venv) [kipertail@arch matplotlib]$ grep -A15 '^dependencies' pyproject.toml
dependencies = [
    "contourpy >= 1.2.1",
    "cycler >= 0.12.0",
    "fonttools >= 4.28.2",
    "kiwisolver >= 1.3.1",
    "numpy >= 2.0",
    "packaging >= 20.0",
    "pillow >= 9",
    "pyparsing >= 3",
    "python-dateutil >= 2.7",
]
# Also keep in sync with find_program of meson.build.
requires-python = ">=3.12"

[project.urls]
"Homepage" = "https://matplotlib.org"
(.venv) [kipertail@arch matplotlib]$  
~~~

