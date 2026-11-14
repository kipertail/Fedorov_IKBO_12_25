import gzip
import re
import urllib.error
import urllib.request

from graph import reverse_graph

DIST = "noble"
COMPONENT = "main"
ARCH = "amd64"
TIMEOUT = 60
ENCODING = "utf-8"
PACKAGE_FIELD = "Package"
VERSION_FIELD = "Version"
PROVIDES_FIELD = "Provides"
DEPENDS_FIELDS = ("Pre-Depends", "Depends")
FIELD_SEPARATOR = ":"
STANZA_SEPARATOR = "\n\n"
CONTINUATION_PREFIXES = (" ", "\t")
DEPENDENCY_SEPARATOR = ","
ALTERNATIVE_SEPARATOR = "|"
DEP_RE = re.compile(
    r"^(?P<name>[^\s(:\[]+)(?::\S+)?\s*"
    r"(?:\((?P<op>[<>=]+)\s*(?P<version>[^)]+)\))?")


class RepoError(Exception):
    pass


def packages_url(repo):
    base = repo.rstrip("/")
    return f"{base}/dists/{DIST}/{COMPONENT}/binary-{ARCH}/Packages.gz"


def download_index(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            data = response.read()
    except urllib.error.HTTPError as err:
        raise RepoError(f"{url}: сервер вернул HTTP {err.code}") from err
    except OSError as err:
        raise RepoError(f"{url}: не удалось подключиться: {err}") from err
    try:
        return gzip.decompress(data).decode(ENCODING)
    except (OSError, EOFError, UnicodeDecodeError) as err:
        raise RepoError(f"{url}: неверный формат индекса пакетов") from err


def parse_stanza(block):
    fields = {}
    key = None
    for line in block.splitlines():
        if line.startswith(CONTINUATION_PREFIXES) and key:
            fields[key] += "\n" + line.strip()
        elif FIELD_SEPARATOR in line:
            key, value = line.split(FIELD_SEPARATOR, 1)
            fields[key] = value.strip()
    return fields


def parse_packages(text):
    return [parse_stanza(block) for block in text.split(STANZA_SEPARATOR)
            if block.strip()]


def find_package(stanzas, name, version):
    versions = [s.get(VERSION_FIELD) for s in stanzas
                if s.get(PACKAGE_FIELD) == name]
    if not versions:
        raise RepoError(f"пакет '{name}' не найден в репозитории")
    for stanza in stanzas:
        if (stanza.get(PACKAGE_FIELD) == name
                and stanza.get(VERSION_FIELD) == version):
            return stanza
    raise RepoError(f"версия '{version}' пакета '{name}' не найдена, "
                    f"доступные версии: {', '.join(versions)}")


def parse_dependency(item):
    match = DEP_RE.match(item.strip())
    if not match:
        raise RepoError(f"не удалось разобрать зависимость '{item}'")
    return (match.group("name"), match.group("op") or "",
            (match.group("version") or "").strip())


def parse_depends(value):
    groups = []
    for group in value.split(DEPENDENCY_SEPARATOR):
        if group.strip():
            groups.append([parse_dependency(alt)
                           for alt in group.split(ALTERNATIVE_SEPARATOR)])
    return groups


def stanza_dependencies(stanza):
    groups = []
    for field in DEPENDS_FIELDS:
        groups.extend(parse_depends(stanza.get(field, "")))
    return groups


class AptIndex:

    def __init__(self, stanzas):
        self.stanzas = stanzas
        self.packages = {}
        self.providers = {}
        for stanza in stanzas:
            name = stanza.get(PACKAGE_FIELD)
            self.packages.setdefault(name, stanza)
            for group in parse_depends(stanza.get(PROVIDES_FIELD, "")):
                self.providers.setdefault(group[0][0], []).append(name)

    def resolve(self, name):
        if name in self.packages:
            return name
        providers = self.providers.get(name)
        return providers[0] if providers else None

    def choose(self, group):
        for dep_name, _, _ in group:
            real = self.resolve(dep_name)
            if real:
                return real
        return group[0][0]

    def dependency_names(self, stanza):
        names = []
        for group in stanza_dependencies(stanza):
            real = self.choose(group)
            if real not in names:
                names.append(real)
        return names


def load_index(repo):
    return AptIndex(parse_packages(download_index(packages_url(repo))))


def dependency_source(repo, root, version):
    index = load_index(repo)
    root_stanza = find_package(index.stanzas, root, version)

    def get_deps(name):
        if name == root:
            return index.dependency_names(root_stanza)
        stanza = index.packages.get(name)
        return index.dependency_names(stanza) if stanza else None

    return get_deps


def reverse_dependency_source(repo, root, version):
    index = load_index(repo)
    find_package(index.stanzas, root, version)
    forward = {name: index.dependency_names(stanza)
               for name, stanza in index.packages.items()}
    return reverse_graph(forward).get
