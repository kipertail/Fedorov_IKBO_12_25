class DependencyGraph:

    def __init__(self, get_deps, max_depth):
        self.get_deps = get_deps
        self.max_depth = max_depth
        self.edges = {}
        self.depths = {}
        self.missing = set()
        self.cycles = []
        self.stack = []

    def build(self, root):
        self.visit(root, 0)
        return self

    def visit(self, name, depth):
        if name in self.stack:
            start = self.stack.index(name)
            cycle = self.stack[start:] + [name]
            if cycle not in self.cycles:
                self.cycles.append(cycle)
            return
        if name in self.depths and self.depths[name] <= depth:
            return
        self.depths[name] = depth
        if depth >= self.max_depth:
            return
        deps = self.get_deps(name)
        if deps is None:
            self.missing.add(name)
            return
        self.edges[name] = deps
        self.stack.append(name)
        for dep in deps:
            self.visit(dep, depth + 1)
        self.stack.pop()

    def nodes(self):
        return sorted(self.depths, key=lambda name: (self.depths[name], name))

    def edge_count(self):
        return sum(len(deps) for deps in self.edges.values())
