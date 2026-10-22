import shutil
import subprocess

import pytest

import visualize
from graph import DependencyGraph, reverse_graph


def build(edges, root="A", max_depth=10):
    return DependencyGraph(edges.get, max_depth).build(root)


def test_dot_structure():
    dot = visualize.to_dot(build({"A": ["B"], "B": []}), "A")
    assert dot.startswith("digraph dependencies {")
    assert dot.rstrip().endswith("}")
    assert '"A" -> "B";' in dot


def test_root_highlighted():
    dot = visualize.to_dot(build({"A": ["B"], "B": []}), "A")
    assert '"A" [style="rounded,filled"' in dot


def test_missing_node_dashed():
    dot = visualize.to_dot(build({"A": ["X"]}), "A")
    assert '"X" [style="rounded,dashed"' in dot


def test_cycle_edges_red():
    dot = visualize.to_dot(build({"A": ["B"], "B": ["A"]}), "A")
    assert '"A" -> "B" [color="red"' in dot
    assert '"B" -> "A" [color="red"' in dot


def test_reverse_keeps_dependency_direction():
    reverse = reverse_graph({"A": ["B"], "B": []})
    graph = DependencyGraph(reverse.get, 10).build("B")
    dot = visualize.to_dot(graph, "B", reverse=True)
    assert '"A" -> "B";' in dot


def test_quote_special_names():
    assert visualize.quote('g++"x') == '"g++\\"x"'


def test_dot_path():
    assert visualize.dot_path("out/graph.svg") == "out/graph.dot"


def test_dot_not_installed(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError("dot")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(visualize.VisualizationError, match="Graphviz"):
        visualize.render_svg("digraph {}", "graph.svg")


@pytest.mark.skipif(shutil.which("dot") is None,
                    reason="Graphviz не установлен")
def test_save_creates_svg_and_dot(tmp_path):
    output = tmp_path / "graph.svg"
    graph = build({"A": ["B"], "B": []})
    dot_file = visualize.save(graph, "A", str(output))
    assert output.read_text(encoding="utf-8").lstrip().startswith("<?xml")
    assert "digraph" in open(dot_file, encoding="utf-8").read()
