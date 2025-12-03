from collections import deque


def topological_sort(nodes, edges):
    inputs = dict()
    input_deg = dict()

    for u in nodes:
        input_deg[u] = 0
        inputs[u] = []

    for u, v, w in edges:
        inputs[u].append(v)
        input_deg[v] += 1

    deq = deque([u for u in nodes if input_deg[u] == 0])
    ordered = []
    while deq:
        u = deq.popleft()
        ordered.append(u)
        for v in inputs[u]:
            input_deg[v] -= 1
            if input_deg[v] == 0:
                deq.append(v)

    return ordered


def longest_path(nodes, edges_nodes, s, t):

    edges = dict()

    for u, _, _ in edges_nodes:
        edges[u] = []

    for u, v, w in edges_nodes:
        edges[u].append((v, w))

    sorted_nodes = topological_sort(nodes, edges_nodes)
    pos = {v: i for i, v in enumerate(sorted_nodes)}

    print("Результат сортировки:")
    for i in sorted_nodes:
        print(nodes_s[i], end=' ')
    print("\n")

    if pos[s] > pos[t]:
        return None, float("-inf")

    OPT = {v: float("-inf") for v in nodes}
    x = {v: None for v in nodes}
    OPT[s] = 0.0

    for u in sorted_nodes[pos[s]:pos[t] + 1]:
        if OPT[u] == float("-inf"):
            continue
        for v, w in edges.get(u, []):
            if pos.get(v, -1) > pos[t]:
                continue
            new_len_OPT = OPT[u] + w
            if new_len_OPT > OPT[v]:
                OPT[v] = new_len_OPT
                x[v] = u

    if OPT[t] == float("-inf"):
        return None, float("-inf")

    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if cur == s:
            break
        cur = x[cur]
    path.reverse()

    if path[0] != s:
        return None, float("-inf")

    return path, OPT[t]


if __name__ == "__main__":

    nodes = [1, 2, 3, 4, 5, 6]
    nodes_s = {1: 's', 2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 't'}
    edges = [
        (1, 2, 3),
        (1, 4, 2),
        (2, 3, 4),
        (3, 5, 1),
        (3, 6, 2),
        (4, 2, 2),
        (4, 5, 2),
        (5, 6, 1)
    ]
    s = 1
    t = 6

    path, length = longest_path(nodes, edges, s, t)

    if path is None:
        print("Путь не найден")
    else:
        print("Наидлиннейший путь:",)
        for i in path:
            print(nodes_s[i], end=' ')
        print("\nДлина:", length)