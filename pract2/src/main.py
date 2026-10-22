import argparse
import os
import re
import sys

import apt_repo
import graph_file

MIN_DEPTH = 1
DEFAULT_DEPTH = 3
DEFAULT_OUTPUT = "graph.svg"
OUTPUT_EXT = ".svg"
URL_PREFIXES = ("http://", "https://")
PACKAGE_RE = re.compile(r"^[a-z0-9][a-z0-9+.\-]+$")
TEST_PACKAGE_RE = re.compile(r"^[A-Z]+$")
VERSION_RE = re.compile(r"^[0-9A-Za-z.+~:\-]+$")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей пакетов Ubuntu")
    parser.add_argument("--package", required=True,
                        help="имя анализируемого пакета")
    parser.add_argument("--repo", required=True,
                        help="URL репозитория или путь к тестовому файлу")
    parser.add_argument("--test-mode", action="store_true",
                        help="режим работы с тестовым репозиторием")
    parser.add_argument("--version", default="",
                        help="версия пакета")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="имя файла с изображением графа")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_DEPTH,
                        help="максимальная глубина анализа зависимостей")
    return parser.parse_args(argv)


def validate_package(package, test_mode):
    if test_mode:
        if not TEST_PACKAGE_RE.match(package):
            return (f"package: '{package}': в тестовом режиме имя "
                    "пакета состоит из заглавных латинских букв")
    elif not PACKAGE_RE.match(package):
        return f"package: '{package}': недопустимое имя пакета"
    return None


def validate_repo(repo, test_mode):
    if test_mode:
        if not os.path.isfile(repo):
            return f"repo: '{repo}': файл тестового репозитория не найден"
    elif not repo.startswith(URL_PREFIXES):
        return f"repo: '{repo}': ожидается URL (http:// или https://)"
    return None


def validate_version(version, test_mode):
    if test_mode and not version:
        return None
    if not version:
        return "version: версия пакета не задана"
    if not VERSION_RE.match(version):
        return f"version: '{version}': недопустимая версия пакета"
    return None


def validate_output(output):
    if not output.endswith(OUTPUT_EXT):
        return f"output: '{output}': ожидается файл с расширением .svg"
    folder = os.path.dirname(output)
    if folder and not os.path.isdir(folder):
        return f"output: '{output}': папка '{folder}' не существует"
    return None


def validate_depth(depth):
    if depth < MIN_DEPTH:
        return f"max-depth: {depth}: глубина должна быть >= {MIN_DEPTH}"
    return None


def validate(args):
    checks = [
        validate_package(args.package, args.test_mode),
        validate_repo(args.repo, args.test_mode),
        validate_version(args.version, args.test_mode),
        validate_output(args.output),
        validate_depth(args.max_depth),
    ]
    return [error for error in checks if error]


def get_dependencies(args):
    if args.test_mode:
        return graph_file.direct_dependencies(args.repo, args.package)
    return apt_repo.direct_dependencies(args.repo, args.package,
                                        args.version)


def format_dependency(dep):
    name, op, version = dep
    return f"{name} ({op} {version})" if op else name


def print_dependencies(args, groups):
    title = args.package if args.test_mode else \
        f"{args.package} {args.version}"
    print(f"Прямые зависимости {title}:")
    if not groups:
        print("  (нет зависимостей)")
    for group in groups:
        print("  " + " | ".join(format_dependency(dep) for dep in group))


def fail(messages):
    for message in messages:
        print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(1)


def main(argv=None):
    args = parse_args(argv)
    errors = validate(args)
    if errors:
        fail(errors)
    try:
        groups = get_dependencies(args)
    except apt_repo.RepoError as err:
        fail([str(err)])
    print_dependencies(args, groups)


if __name__ == "__main__":
    main()
