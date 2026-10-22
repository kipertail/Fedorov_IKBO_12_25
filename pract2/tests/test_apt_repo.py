import pytest

from apt_repo import (AptIndex, RepoError, find_package, packages_url,
                      parse_depends, parse_packages, parse_stanza,
                      stanza_dependencies)

SAMPLE = """\
Package: curl
Version: 8.5.0-2ubuntu10
Depends: libc6 (>= 2.34), libcurl4t64 (= 8.5.0-2ubuntu10)
Description: command line tool
 second line of description

Package: curl
Version: 8.5.0-2ubuntu10.6
Pre-Depends: init-system-helpers
Depends: libc6, perl:any, sssd | winbind

Package: base-files
Version: 13ubuntu10
"""


def test_packages_url():
    url = packages_url("http://archive.ubuntu.com/ubuntu/")
    assert url == ("http://archive.ubuntu.com/ubuntu/dists/noble/"
                   "main/binary-amd64/Packages.gz")


def test_parse_stanza_continuation():
    fields = parse_stanza("Package: x\nDescription: a\n b\n c")
    assert fields["Package"] == "x"
    assert fields["Description"] == "a\nb\nc"


def test_parse_packages_count():
    assert len(parse_packages(SAMPLE)) == 3


def test_find_package_by_version():
    stanza = find_package(parse_packages(SAMPLE), "curl", "8.5.0-2ubuntu10.6")
    assert stanza["Version"] == "8.5.0-2ubuntu10.6"


def test_find_package_not_found():
    with pytest.raises(RepoError, match="не найден"):
        find_package(parse_packages(SAMPLE), "wget", "1.0")


def test_find_package_wrong_version():
    with pytest.raises(RepoError, match="доступные версии"):
        find_package(parse_packages(SAMPLE), "curl", "1.0")


def test_parse_depends_with_versions():
    groups = parse_depends("libc6 (>= 2.34), zlib1g (>= 1:1.1.4)")
    assert groups == [[("libc6", ">=", "2.34")],
                      [("zlib1g", ">=", "1:1.1.4")]]


def test_parse_depends_alternatives_and_arch():
    groups = parse_depends("perl:any, sssd | winbind")
    assert groups == [[("perl", "", "")],
                      [("sssd", "", ""), ("winbind", "", "")]]


def test_parse_depends_empty():
    assert parse_depends("") == []


def test_stanza_dependencies_includes_pre_depends():
    stanza = find_package(parse_packages(SAMPLE), "curl", "8.5.0-2ubuntu10.6")
    names = [group[0][0] for group in stanza_dependencies(stanza)]
    assert names == ["init-system-helpers", "libc6", "perl", "sssd"]


INDEX_SAMPLE = """\
Package: base-files
Version: 13ubuntu10
Pre-Depends: awk
Depends: libc6 (>= 2.34)

Package: mawk
Version: 1.3.4
Provides: awk

Package: libc6
Version: 2.39

Package: app
Version: 1.0
Depends: missing-pkg | libc6, ghost, libc6
"""


def make_index():
    return AptIndex(parse_packages(INDEX_SAMPLE))


def test_resolve_real_and_virtual():
    index = make_index()
    assert index.resolve("libc6") == "libc6"
    assert index.resolve("awk") == "mawk"
    assert index.resolve("ghost") is None


def test_dependency_names_virtual():
    index = make_index()
    stanza = index.packages["base-files"]
    assert index.dependency_names(stanza) == ["mawk", "libc6"]


def test_dependency_names_alternatives_and_duplicates():
    index = make_index()
    stanza = index.packages["app"]
    assert index.dependency_names(stanza) == ["libc6", "ghost"]
