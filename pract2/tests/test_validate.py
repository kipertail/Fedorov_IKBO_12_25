import os

import pytest

from main import (validate_depth, validate_output, validate_package,
                  validate_repo, validate_version)

TEST_REPO = os.path.join(os.path.dirname(__file__), "graph1.txt")


@pytest.mark.parametrize("name", ["libc6", "g++-12", "python3.12"])
def test_package_valid(name):
    assert validate_package(name, False) is None


@pytest.mark.parametrize("name", ["Curl", "-abc", "a", "bad!"])
def test_package_invalid(name):
    assert validate_package(name, False) is not None


def test_package_test_mode():
    assert validate_package("A", True) is None
    assert validate_package("a", True) is not None


def test_repo_url():
    assert validate_repo("https://example.com", False) is None
    assert validate_repo("example.com", False) is not None


def test_repo_test_file():
    assert validate_repo(TEST_REPO, True) is None
    assert validate_repo("missing.txt", True) is not None


@pytest.mark.parametrize("version", ["1:2.3-4ubuntu1", "8.5.0-2ubuntu10"])
def test_version_valid(version):
    assert validate_version(version, False) is None


@pytest.mark.parametrize("version", ["", "1 0", "1,0"])
def test_version_invalid(version):
    assert validate_version(version, False) is not None


def test_version_optional_in_test_mode():
    assert validate_version("", True) is None


@pytest.mark.parametrize("output, ok", [
    ("graph.svg", True),
    ("graph.png", False),
    ("nodir/graph.svg", False),
])
def test_output(output, ok):
    assert (validate_output(output) is None) == ok


@pytest.mark.parametrize("depth, ok", [(1, True), (5, True),
                                       (0, False), (-5, False)])
def test_depth(depth, ok):
    assert (validate_depth(depth) is None) == ok
