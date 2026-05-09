import heapq
from data import StartHub, Hub, EndHub


class Dijkstra:
    """Finds optimal drone paths using Dijkstra with cumulative penalties."""

    def __init__(
            self,
            start: StartHub,
            hub_class: list[Hub],
            end: EndHub,
            adjacency: dict[str, list[tuple[str, int]]]) -> None:

        self.start = start
        self.end = end
        self.adjacency = adjacency
        self.hub_map: dict[str, Hub | StartHub | EndHub] = {
            start.name: start,
            end.name: end,
        }

        for hub in hub_class:
            self.hub_map[hub.name] = hub

        self.zone: dict[str, int] = {
            'normal': 1,
            'priority': 0,
            'restricted': 2,
        }

    def run(self) -> tuple[list[list[str]], int]:
        """Compute up to nb_drones distinct paths,
        penalizing used nodes each iteration."""
        total_drones: int = self.start.max_drones
        paths: list[list[str]] = []
        penalties: dict[str, int] = {}

        for _ in range(total_drones):
            cost: dict[str, float] = {x: float('inf') for x in self.adjacency}
            parents: dict[str, str | None] = {x: None for x in self.adjacency}
            cost[self.start.name] = 0
            path = self.djikstra(cost, parents, penalties)

            if path is None or path in paths:
                break
            paths.append(path)

            for node in path[1:-1]:
                penalties[node] = penalties.get(node, 0) + 100

        return paths, total_drones

    def djikstra(
            self,
            cost: dict[str, float],
            parents: dict[str, str | None],
            penalties: dict[str, int]) -> list[str] | None:
        """Run one Dijkstra pass and return the shortest
        path, or None if unreachable."""
        if (self.start.name not in self.adjacency
                or self.end.name not in self.adjacency):
            return None

        data: list[tuple[float, str]] = []
        heapq.heappush(data, (0, self.start.name))

        while data:
            mini = heapq.heappop(data)
            neighbors = self.adjacency[mini[1]]

            for n in neighbors:
                if self.hub_map[n[0]].zone != "blocked":
                    tot_cost = (
                        mini[0]
                        + self.zone[self.hub_map[n[0]].zone]
                        + penalties.get(n[0], 0)
                    )
                    if tot_cost < cost[self.hub_map[n[0]].name]:
                        cost[self.hub_map[n[0]].name] = tot_cost
                        parents[n[0]] = mini[1]
                        heapq.heappush(
                            data,
                            (tot_cost, self.hub_map[n[0]].name)
                        )

        if parents[self.end.name] is None:
            return None

        current = parents[self.end.name]
        path: list[str] = []

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        path.append(self.end.name)

        return path
