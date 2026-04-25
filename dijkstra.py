from data import StartHub, Hub, EndHub
import heapq


def main_djikstra(
        start: StartHub,
        hub_class: list[Hub],
        end: EndHub,
        adjacency: dict[str, list[tuple[str, int]]]) -> None:

    zone: dict[str, int | None] = {
        'normal': 1,
        'priority': 1,
        'restricted': 2,
    }

    cost: dict[str, float] = {}
    parents: dict[str, str | None] = {}

    for x in adjacency:
        cost[x] = float('inf')
        parents[x] = None
    cost['start'] = 0

    hub_map: dict[str, Hub] = {
        start.name: start,
        end.name: end,
    }

    for hub in hub_class:
        hub_map.update({hub.name: hub})

    data = []
    heapq.heappush(data, (0, start.name))

    while data:
        min = heapq.heappop(data)
        neighbors = adjacency[min[1]]
        for n in neighbors:
            if hub_map[n[0]].zone != "blocked":
                tot_cost = min[0] + zone[hub_map[n[0]].zone]
                if tot_cost < cost[hub_map[n[0]].name]:
                    cost[hub_map[n[0]].name] = tot_cost
                    parents[n[0]] = min[1]
                    heapq.heappush(data, (tot_cost, hub_map[n[0]].name))

    current = list(parents.keys())[-1]
    path = []
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
