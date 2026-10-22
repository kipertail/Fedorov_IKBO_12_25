import pytest

from apt_repo import RepoError
from graph_file import direct_dependencies, load_graph


@pytest.fixture
def graph_path(tmp_path):
    path = tmp_path / "graph.txt"
    path.write_text("# comment\nA: B C\nB: C\n\nC:\n", encoding="utf-8")
    return str(path)


def test_load_graph(graph_path):
    assert load_graph(graph_path) == {"A": ["B", "C"], "B": ["C"], "C": []}


def test_direct_dependencies(graph_path):
    assert direct_dependencies(graph_path, "A") == [[("B", "", "")],
                                                    [("C", "", "")]]


def test_no_dependencies(graph_path):
    assert direct_dependencies(graph_path, "C") == []


def test_unknown_package(graph_path):
    with pytest.raises(RepoError, match="не найден"):
        direct_dependencies(graph_path, "Z")


def test_bad_line(tmp_path):
    path = tmp_path / "bad.txt"
    path.write_text("A B C\n", encoding="utf-8")
    with pytest.raises(RepoError, match="строка 1"):
        load_graph(str(path))


def test_missing_file(tmp_path):
    with pytest.raises(RepoError):
        load_graph(str(tmp_path / "missing.txt"))
