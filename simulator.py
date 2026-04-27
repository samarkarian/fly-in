from data import Hub


def main_simulator(
        path,
        total_drones,
        hub_class: list[Hub],
        adjacency: dict[str, list[tuple[str, int]]]):

    max_link_capacity: dict[str, int] = {}
    max_drones: dict[str, int] = {}

    for p in path:
        for h in hub_class:
            if h.name == p:
                max_drones.update({h.name: h.max_drones})

    for zone, neighbors in adjacency.items():
        for v in neighbors:
            max_link_capacity.update({(zone, v[0]): v[1]})
