from apt_repo import RepoError


def parse_graph_line(line, num):
    if ":" not in line:
        raise RepoError(f"строка {num}: ожидается формат 'ПАКЕТ: ЗАВИСИМОСТИ'")
    name, deps = line.split(":", 1)
    return name.strip(), deps.split()


def load_graph(path):
    graph = {}
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as err:
        raise RepoError(f"{path}: {err.strerror}") from err
    for num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, deps = parse_graph_line(line, num)
        graph[name] = deps
    return graph


def dependency_source(path, root):
    graph = load_graph(path)
    if root not in graph:
        raise RepoError(f"пакет '{root}' не найден в тестовом репозитории")
    return graph.get
