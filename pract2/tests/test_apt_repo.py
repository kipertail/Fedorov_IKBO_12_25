import pytest

from apt_repo import (RepoError, find_package, packages_url, parse_depends,
                      parse_packages, parse_stanza, stanza_dependencies)

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
