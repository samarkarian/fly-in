from data import StartHub, Hub, EndHub
import heapq


def djikstra(
        start: StartHub,
        end: EndHub,
        adjacency: dict[str, list[tuple[str, int]]],
        hub_map: dict[str, Hub],
        zone: dict[str, int | None],
        cost: dict[str, float],
        parents: dict[str, str | None],
        penalties: dict[str, int] = {}) -> list[str]:

    data = []
    heapq.heappush(data, (0, start.name))

    while data:
        mini = heapq.heappop(data)
        neighbors = adjacency[mini[1]]
        for n in neighbors:
            if hub_map[n[0]].zone != "blocked":
                tot_cost = mini[0] + zone[hub_map[n[0]].zone] + penalties.get(n[0], 0)
                if tot_cost < cost[hub_map[n[0]].name]:
                    cost[hub_map[n[0]].name] = tot_cost
                    parents[n[0]] = mini[1]
                    heapq.heappush(data, (tot_cost, hub_map[n[0]].name))

    if parents[end.name] is None:
        return None

    current = parents[end.name]
    path = []
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    path.append(end.name)

    return path


def main_djikstra(
        start: StartHub,
        hub_class: list[Hub],
        end: EndHub,
        adjacency: dict[str, list[tuple[str, int]]]) -> tuple[list, int]:

    zone: dict[str, int | None] = {
        'normal': 1,
        'priority': 1,
        'restricted': 2,
    }

    hub_map: dict[str, Hub] = {
        start.name: start,
        end.name: end,
    }

    for hub in hub_class:
        hub_map.update({hub.name: hub})

    total_drones: int = start.max_drones
    paths: list[list[str]] = []
    penalties: dict[str, int] = {}
    for _ in range(2):
        cost = {x: float('inf') for x in adjacency}
        parents = {x: None for x in adjacency}
        cost[start.name] = 0
        path = djikstra(
                start, end, adjacency, hub_map, zone, cost, parents, penalties
            )
        if path is None or path in paths:
            break
        paths.append(path)
        for node in path[1:-1]:
            penalties[node] = penalties.get(node, 0) + 100

    return paths, total_drones
