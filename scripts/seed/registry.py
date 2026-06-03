from collections import defaultdict, deque

SEEDERS = []


def register(seeder_cls):
    SEEDERS.append(seeder_cls)
    return seeder_cls


def get_seeder_map():
    return {s.app_label: s() for s in SEEDERS}

# -------------------------
# Dependency expansion
# -------------------------
def expand_dependencies(selected, seeder_map):
    """
    Returns full closure of selected seeders + dependencies.
    """
    expanded = set()

    def visit(name):
        if name not in seeder_map:
            raise Exception(f"Unknown seeder: {name}")

        if name in expanded:
            return

        expanded.add(name)

        for dep in seeder_map[name].depends_on:
            visit(dep)

    for name in selected:
        visit(name)

    return expanded


# -------------------------
# Topological sort
# -------------------------
def topo_sort(seeders):
    graph = defaultdict(list)
    indegree = defaultdict(int)
    nodes = set()

    seeder_map = {s.app_label: s for s in seeders}

    for s in seeders:
        nodes.add(s.app_label)

        for dep in s.depends_on:
            graph[dep].append(s.app_label)
            indegree[s.app_label] += 1
            nodes.add(dep)

    queue = deque([n for n in nodes if indegree[n] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(nodes):
        raise Exception("[Seeder Error] Cycle detected in dependencies")

    return [seeder_map[n] for n in order if n in seeder_map]


# -------------------------
# Resolve execution set
# -------------------------
def resolve_order(selected=None, with_deps=False):
    seeder_map = get_seeder_map()

    # ------------------------------------
    # 1. build execution set
    # ------------------------------------
    if selected:
        if with_deps:
            execution_names = set()

            def collect(name):
                if name not in seeder_map:
                    raise Exception(f"Unknown seeder: {name}")

                if name in execution_names:
                    return

                execution_names.add(name)

                for dep in seeder_map[name].depends_on:
                    collect(dep)

            for name in selected:
                collect(name)

        else:
            execution_names = set(selected)
    else:
        execution_names = set(seeder_map.keys())

    # ------------------------------------
    # 2. validate dependencies exist
    # ------------------------------------
    for name in execution_names:
        seeder = seeder_map[name]
        for dep in seeder.depends_on:
            if dep not in seeder_map:
                raise Exception(
                    f"[Seeder Error] '{name}' depends on missing seeder '{dep}'"
                )

    # ------------------------------------
    # 3. topo sort ONLY execution set
    # ------------------------------------
    return topo_sort([seeder_map[n] for n in execution_names])

# -------------------------
# Runner
# -------------------------
def run_all(**options):
    selected = options.get("only")
    with_deps = options.get("with_deps", False)

    seeders = resolve_order(selected, with_deps=with_deps)

    for s in seeders:
        print(f"→ Running {s.app_label}")
        s.run(**options)