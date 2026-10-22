import argparse
import os
import re
import sys

import apt_repo
import graph_file
from graph import DependencyGraph

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
    parser.add_argument("--reverse", action="store_true",
                        help="вывести обратные зависимости пакета")
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


def dependency_source(args):
    if args.test_mode and args.reverse:
        return graph_file.reverse_dependency_source(args.repo, args.package)
    if args.test_mode:
        return graph_file.dependency_source(args.repo, args.package)
    if args.reverse:
        return apt_repo.reverse_dependency_source(args.repo, args.package,
                                                  args.version)
    return apt_repo.dependency_source(args.repo, args.package, args.version)


def print_graph(args, graph):
    title = args.package if args.test_mode else \
        f"{args.package} {args.version}"
    kind = "Обратные зависимости" if args.reverse else "Граф зависимостей"
    arrow = "<-" if args.reverse else "->"
    print(f"{kind} {title} (глубина {args.max_depth}):")
    for name in graph.nodes():
        if name in graph.missing:
            print(f"  {name}: не найден в репозитории")
        elif name in graph.edges:
            deps = ", ".join(graph.edges[name]) or "(нет)"
            print(f"  {name} {arrow} {deps}")
    print(f"Пакетов: {len(graph.depths)}, связей: {graph.edge_count()}")
    for cycle in graph.cycles:
        path = cycle[::-1] if args.reverse else cycle
        print("Цикл: " + " -> ".join(path))


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
        get_deps = dependency_source(args)
    except apt_repo.RepoError as err:
        fail([str(err)])
    graph = DependencyGraph(get_deps, args.max_depth).build(args.package)
    print_graph(args, graph)


if __name__ == "__main__":
    main()
