from collections import deque, defaultdict
from typing import Dict

GraphFlow = Dict[str, Dict[str, int]]


def add_empty_edges(edges):
    ost_flow: GraphFlow = defaultdict(dict)
    nodes = set()

    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
        ost_flow[u].setdefault(v, 0)
        ost_flow[u][v] += w

    for u in list(nodes):
        ost_flow.setdefault(u, {})

    for u in list(ost_flow):
        for v in list(ost_flow[u]):
            ost_flow.setdefault(v, {})
            ost_flow[v].setdefault(u, 0)

    return ost_flow


def find_path_by_bfs(graph: GraphFlow, node_from, node_to):
    visited_nodes = dict()
    dec = deque([node_from])
    visited_nodes.setdefault(node_from, None)

    while dec:
        u = dec.popleft()
        for v, flow_amount in graph[u].items():
            if flow_amount > 0 and v not in visited_nodes:
                visited_nodes.setdefault(v, u)

                if v == node_to:
                    path = []
                    cur = node_to
                    thetas = []
                    while visited_nodes[cur] is not None:
                        prev = visited_nodes[cur]
                        path.append((prev, cur))
                        thetas.append(graph[prev][cur])
                        cur = prev
                    path.reverse()

                    return path, min(thetas) if thetas else 0

                dec.append(v)

    return [], 0


def find_max_flow(edges, node_from, node_to):
    graph_with_empty = add_empty_edges(edges)
    orig_graph = {u: dict(vs) for u, vs in graph_with_empty.items()}

    current_ost_flow = {u: dict(vs) for u, vs in graph_with_empty.items()}

    max_flow = 0

    iteration = 0
    while True:
        iteration += 1
        path, theta = find_path_by_bfs(current_ost_flow, node_from, node_to)
        if theta == 0:
            print(f"{iteration}. Путь не найден")
            break

        print(f"{iteration}. Найден путь: {path},  theta = {theta}")

        for u, v in path:
            current_ost_flow[u][v] -= theta
            current_ost_flow[v][u] = current_ost_flow.get(v, {}).get(u, 0) + theta

        max_flow += theta

    restored_flow: GraphFlow = defaultdict(dict)
    for u in orig_graph:
        for v in orig_graph[u]:
            edge_flow = max(0,  current_ost_flow[u].get(v, 0) - orig_graph[u].get(v, 0))
            restored_flow[u][v] = edge_flow

    return max_flow, dict(restored_flow)


if __name__ == "__main__":

    edges = [
        ('s', 'v1', 3),
        ('s', 'v2', 2),
        ('v1', 'v2', 2),
        ('v1', 't', 1),
        ('v2', 't', 2),
    ]
    from_node = 's'
    to_node = 't'

    max_flow_val, res_flow = find_max_flow(edges, from_node, to_node)
    print("\nМаксимальный поток:", max_flow_val)
    print("Потоки:")
    q = 1
    for u in sorted(res_flow, reverse=True):
        for v in sorted(res_flow[u]):
            # if res_flow[u][v]:
            print(f"{q}. {v} -> {u} : {res_flow[u][v]}")
            q += 1
