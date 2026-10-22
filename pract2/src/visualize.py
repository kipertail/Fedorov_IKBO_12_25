import os
import subprocess

DOT_EXT = ".dot"
ROOT_STYLE = 'style="rounded,filled", fillcolor="lightblue"'
MISSING_STYLE = 'style="rounded,dashed", color="red"'
CYCLE_STYLE = 'color="red", penwidth=2'


class VisualizationError(Exception):
    pass


def quote(name):
    return '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cycle_edges(graph, reverse):
    edges = set()
    for cycle in graph.cycles:
        for start, end in zip(cycle, cycle[1:]):
            edges.add((end, start) if reverse else (start, end))
    return edges


def graph_edges(graph, reverse):
    for name, deps in graph.edges.items():
        for dep in deps:
            yield (dep, name) if reverse else (name, dep)


def node_line(name, root, graph):
    if name == root:
        return f"    {quote(name)} [{ROOT_STYLE}];"
    if name in graph.missing:
        return f"    {quote(name)} [{MISSING_STYLE}];"
    return f"    {quote(name)};"


def to_dot(graph, root, reverse=False):
    lines = [
        "digraph dependencies {",
        "    rankdir=LR;",
        '    node [shape=box, style=rounded, fontname="Helvetica"];',
    ]
    lines.extend(node_line(name, root, graph) for name in graph.nodes())
    in_cycle = cycle_edges(graph, reverse)
    for start, end in graph_edges(graph, reverse):
        attrs = f" [{CYCLE_STYLE}]" if (start, end) in in_cycle else ""
        lines.append(f"    {quote(start)} -> {quote(end)}{attrs};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def dot_path(output):
    return os.path.splitext(output)[0] + DOT_EXT


def render_svg(dot_text, output):
    try:
        subprocess.run(["dot", "-Tsvg", "-o", output], input=dot_text,
                       text=True, capture_output=True, check=True)
    except FileNotFoundError as err:
        raise VisualizationError(
            "программа dot (Graphviz) не найдена, установите graphviz"
        ) from err
    except subprocess.CalledProcessError as err:
        raise VisualizationError(
            f"dot завершился с ошибкой: {err.stderr.strip()}") from err


def save(graph, root, output, reverse=False):
    dot_text = to_dot(graph, root, reverse)
    with open(dot_path(output), "w", encoding="utf-8") as file:
        file.write(dot_text)
    render_svg(dot_text, output)
    return dot_path(output)
