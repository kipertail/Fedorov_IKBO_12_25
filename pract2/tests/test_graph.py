from graph import DependencyGraph


def build(edges, root="A", max_depth=10):
    return DependencyGraph(edges.get, max_depth).build(root)


def test_chain_full():
    graph = build({"A": ["B"], "B": ["C"], "C": []})
    assert graph.edges == {"A": ["B"], "B": ["C"], "C": []}
    assert graph.depths == {"A": 0, "B": 1, "C": 2}
    assert graph.cycles == []


def test_max_depth_limits_graph():
    graph = build({"A": ["B"], "B": ["C"], "C": ["D"], "D": []},
                  max_depth=2)
    assert set(graph.depths) == {"A", "B", "C"}
    assert "C" not in graph.edges


def test_max_depth_one():
    graph = build({"A": ["B", "C"], "B": ["D"], "C": []}, max_depth=1)
    assert graph.edges == {"A": ["B", "C"]}


def test_cycle_detected():
    graph = build({"A": ["B"], "B": ["C"], "C": ["A"]})
    assert graph.cycles == [["A", "B", "C", "A"]]
    assert graph.edge_count() == 3


def test_self_loop():
    graph = build({"A": ["A", "B"], "B": []})
    assert graph.cycles == [["A", "A"]]


def test_diamond_visited_once():
    calls = []

    def get_deps(name):
        calls.append(name)
        return {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}[name]

    DependencyGraph(get_deps, 10).build("A")
    assert calls.count("D") == 1


def test_shorter_path_reexpands():
    graph = build({"A": ["B", "C"], "B": ["C"], "C": ["D"], "D": []},
                  max_depth=2)
    assert graph.depths["C"] == 1
    assert "D" in graph.depths


def test_missing_package():
    graph = build({"A": ["B", "X"], "B": []})
    assert graph.missing == {"X"}


def test_nodes_sorted_by_depth():
    graph = build({"A": ["C", "B"], "B": [], "C": []})
    assert graph.nodes() == ["A", "B", "C"]
