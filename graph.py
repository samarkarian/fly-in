from data import Connection


class Graph:

    def __init__(self, adjacency: dict[str, list[tuple[str, int]]]):

        self.adjacency = adjacency

    def add_connection(self, co: Connection):

        if co.zone_a not in self.adjacency:
            self.adjacency[co.zone_a] = []
        self.adjacency[co.zone_a].append((co.zone_b, co.max_link_capacity))
        if co.zone_b not in self.adjacency:
            self.adjacency[co.zone_b] = []
        self.adjacency[co.zone_b].append((co.zone_a, co.max_link_capacity))


def main_graph(hub_connection: list[Connection]) -> Graph:

    adjacency: dict[str, list[tuple[str, int]]] = {}
    adjacency_dict = Graph(adjacency)

    for co in hub_connection:
        adjacency_dict.add_connection(co)

    return adjacency_dict
