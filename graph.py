from data import Connection


class Graph:
    """Adjacency-list graph representation of the hub network."""

    def __init__(self, adjacency: dict[str, list[tuple[str, int]]]) -> None:
        """Initialize the graph with an existing adjacency dictionary.

        Args:
            adjacency (dict[str, list[tuple[str, int]]]): Adjacency
                list mapping zone names to (neighbor, capacity) pairs.
        """
        self.adjacency = adjacency

    def add_connection(self, co: Connection) -> None:
        """Add a bidirectional edge between the two zones of a connection.

        Args:
            co (Connection): Connection object defining the two
                zones and capacity.
        """
        if co.zone_a not in self.adjacency:
            self.adjacency[co.zone_a] = []
        self.adjacency[co.zone_a].append((co.zone_b, co.max_link_capacity))

        if co.zone_b not in self.adjacency:
            self.adjacency[co.zone_b] = []
        self.adjacency[co.zone_b].append((co.zone_a, co.max_link_capacity))


def main_graph(hub_connection: list[Connection]) -> Graph:
    """Build and return a Graph from a list of Connection objects.

    Args:
        hub_connection (list[Connection]): List of connections to add.

    Returns:
        Graph: Populated graph with all connections.
    """
    adjacency: dict[str, list[tuple[str, int]]] = {}
    adjacency_dict = Graph(adjacency)

    for co in hub_connection:
        adjacency_dict.add_connection(co)

    return adjacency_dict
