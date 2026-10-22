import pytest

from apt_repo import RepoError
from graph_file import (dependency_source, load_graph,
                        reverse_dependency_source)


@pytest.fixture
def graph_path(tmp_path):
    path = tmp_path / "graph.txt"
    path.write_text("# comment\nA: B C\nB: C\n\nC:\n", encoding="utf-8")
    return str(path)


def test_load_graph(graph_path):
    assert load_graph(graph_path) == {"A": ["B", "C"], "B": ["C"], "C": []}


def test_dependency_source(graph_path):
    get_deps = dependency_source(graph_path, "A")
    assert get_deps("A") == ["B", "C"]
    assert get_deps("C") == []
    assert get_deps("Z") is None


def test_unknown_root(graph_path):
    with pytest.raises(RepoError, match="не найден"):
        dependency_source(graph_path, "Z")


def test_bad_line(tmp_path):
    path = tmp_path / "bad.txt"
    path.write_text("A B C\n", encoding="utf-8")
    with pytest.raises(RepoError, match="строка 1"):
        load_graph(str(path))


def test_missing_file(tmp_path):
    with pytest.raises(RepoError):
        load_graph(str(tmp_path / "missing.txt"))


def test_reverse_dependency_source(graph_path):
    get_users = reverse_dependency_source(graph_path, "C")
    assert get_users("C") == ["A", "B"]
    assert get_users("A") == []


def test_reverse_unknown_root(graph_path):
    with pytest.raises(RepoError, match="не найден"):
        reverse_dependency_source(graph_path, "Z")
