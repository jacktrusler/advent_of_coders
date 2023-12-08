from time import perf_counter_ns
from networkx import Graph, shortest_path_length
from itertools import combinations, permutations
from collections import defaultdict


def create_environment(raw_input: str):
    graph = Graph()
    rates = set()
    for line in raw_input.splitlines():
        items = line.split()
        node = items[1]
        rate = int(items[4][5:-1])
        edges = [item[:2] for item in items[9:]]
        graph.add_node(node)
        graph.add_edges_from((node, edge) for edge in edges)
        if rate > 0:
            rates.add((node, rate))
    paths = {(n, m): shortest_path_length(graph, n, m) for n, m in permutations(graph.nodes, 2)}
    return paths, rates


def pressure(paths: dict, rates: set, visited: frozenset, location: str, time: int, results: dict, points: int = 0):
    if len(rates) == 0:
        return points
    best_score = points
    for target, rate in rates:
        next_time = time - paths[(location, target)] - 1
        if next_time <= 1:
            continue
        next_points = points + (rate * next_time)
        next_visited = visited | {target}
        results[next_visited] = max(results[next_visited], next_points)
        p = pressure(paths=paths, rates=rates - {(target, rate,)}, visited=next_visited, location=target,
                     time=next_time, points=next_points, results=results)
        best_score = max(best_score, p)
    return best_score


def solve(raw_input: str):
    paths, rates = create_environment(raw_input)
    a = pressure(paths=paths, rates=rates, visited=frozenset(), location='AA', time=30, results=defaultdict(int))
    results_b = defaultdict(int)
    pressure(paths=paths, rates=rates, visited=frozenset(), location='AA', time=26, results=results_b)
    b = max(results_b[c1] + results_b[c2] for c1, c2 in combinations(results_b, 2) if c1.isdisjoint(c2))
    return a, b


def main():
    with open('./day16_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
