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
def resolve_order(selected=None):
    seeder_map = get_seeder_map()

    # full run
    if not selected:
        seeders = list(seeder_map.values())
    else:
        expanded = expand_dependencies(selected, seeder_map)
        seeders = [seeder_map[n] for n in expanded]

    # validate dependencies exist
    for s in seeders:
        for dep in s.depends_on:
            if dep not in seeder_map:
                raise Exception(
                    f"[Seeder Error] '{s.app_label}' depends on missing seeder '{dep}'"
                )

    return topo_sort(seeders)


# -------------------------
# Runner
# -------------------------
def run_all(**options):
    selected = options.get("only")

    seeders = resolve_order(selected)

    for s in seeders:
        print(f"→ Running {s.app_label}")
        s.run(**options)