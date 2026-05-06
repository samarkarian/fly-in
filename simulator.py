from data import Hub, Drone


def main_simulator(
        paths: list[list[str]],
        total_drones,
        hub_class: list[Hub],
        adjacency: dict[str, list[tuple[str, int]]]):

    max_link_capacity: dict[str, int] = {}
    max_drones: dict[str, int] = {}

    for path in paths:
        for p in path:
            for h in hub_class:
                if h.name == p and p not in max_drones:
                    max_drones.update({h.name: h.max_drones})

    for zone, neighbors in adjacency.items():
        for v in neighbors:
            max_link_capacity.update({(zone, v[0]): v[1]})

    drones: list[Drone] = []
    i: int = 1
    start: str = paths[0][0]
    end: str = paths[0][-1]
    tours: int = 0
    for idx in range(total_drones):
        assigned_path = paths[idx % len(paths)]
        drone = Drone(f"D{i}", start, 0, False, False, assigned_path)
        drones.append(drone)
        i += 1

    control_zone = {}

    for hub in hub_class:
        control_zone.update({hub.name: hub.zone})

    while not all(drone.arrived for drone in drones):
        max_drones_cp = max_drones.copy()
        max_link_capacity_cp = max_link_capacity.copy()
        turn_output = []

        for drone in drones:
            if not drone.arrived:
                cur_zone = drone.path[drone.path_idx]
                next_zone = drone.path[drone.path_idx + 1]
                moved = False
                started_transit = False

                if next_zone != end:
                    if control_zone[next_zone] == 'restricted' and not drone.in_transit:
                        drone.in_transit = True
                        started_transit = True
                    elif (
                        max_drones_cp[next_zone] > 0
                            and max_link_capacity_cp[cur_zone, next_zone] > 0
                    ):
                        max_drones_cp[next_zone] -= 1
                        max_link_capacity_cp[cur_zone, next_zone] -= 1
                        drone.pos = next_zone
                        drone.path_idx += 1
                        drone.in_transit = False
                        moved = True
                else:
                    drone.pos = next_zone
                    drone.path_idx += 1
                    drone.arrived = True
                    moved = True

                if moved:
                    turn_output.append(f"{drone.id}-{drone.pos}")
                elif started_transit or drone.in_transit:
                    turn_output.append(f"{drone.id}-{cur_zone}-{next_zone}")

        if turn_output:
            print(" ".join(turn_output))
        tours += 1

    print(tours)
