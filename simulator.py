from data import Hub, Drone


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

    drones: list[Drone] = []
    i: int = 1
    start: str = path[0]
    end: str = path[-1]
    tours: int = 0
    for _ in range(total_drones):
        drone = Drone(f"D{i}", start, 0, False, False, 0, None)
        drones.append(drone)
        i += 1

    while not all(drone.arrived for drone in drones):
        max_drones_copy = max_drones.copy()
        max_link_capacity_copy = max_link_capacity.copy()
        for drone in drones:
            if not drone.arrived:
                cur_zone = path[drone.path_idx]
                next_zone = path[drone.path_idx + 1]
                if next_zone != end:
                    if (
                        max_drones_copy[next_zone] > 0
                            and max_link_capacity_copy[cur_zone, next_zone] > 0
                    ):
                        max_drones_copy[next_zone] -= 1
                        max_link_capacity_copy[cur_zone, next_zone] -= 1
                        drone.pos = path[drone.path_idx + 1]
                        drone.path_idx += 1
                else:
                    drone.pos = path[drone.path_idx + 1]
                    drone.path_idx += 1
                    drone.arrived = True

            print(f"{drone.id}-{drone.pos}")
        tours += 1

    print(tours)
