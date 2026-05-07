from data import Hub, Drone


class Simulator:
    """Simulates turn-by-turn drone movement along computed paths."""

    def __init__(
            self,
            paths: list[list[str]],
            total_drones: int,
            hub_class: list[Hub],
            adjacency: dict[str, list[tuple[str, int]]]) -> None:

        self._paths = paths
        self._total_drones = total_drones
        self._start: str = paths[0][0]
        self._end: str = paths[0][-1]
        self._max_link_capacity: dict[tuple[str, str], int] = {}
        self._max_drones: dict[str, int] = {}
        self._control_zone: dict[str, str] = {}

        for path in paths:
            for p in path:
                for h in hub_class:
                    if h.name == p and p not in self._max_drones:
                        self._max_drones[h.name] = h.max_drones

        for zone, neighbors in adjacency.items():
            for v in neighbors:
                self._max_link_capacity[(zone, v[0])] = v[1]

        for hub in hub_class:
            self._control_zone[hub.name] = hub.zone

    def run(self) -> list[list[tuple[str, str, bool, str]]]:
        """Run the simulation, print turn output, and return per-turn drone snapshots."""
        drones: list[Drone] = []

        for idx in range(self._total_drones):
            assigned_path = self._paths[idx % len(self._paths)]
            drone = Drone(f"D{idx + 1}", self._start, 0, False, False, assigned_path)
            drones.append(drone)

        snapshots: list[list[tuple[str, str, bool, str]]] = []

        def snapshot() -> list[tuple[str, str, bool, str]]:
            result: list[tuple[str, str, bool, str]] = []

            for d in drones:
                next_zone = d.path[d.path_idx + 1] if d.in_transit else ""
                result.append((d.id, d.pos, d.in_transit, next_zone))

            return result

        snapshots.append(snapshot())

        tours: int = 0
        while not all(drone.arrived for drone in drones):

            zone_occupancy: dict[str, int] = {}

            for drone in drones:
                if not drone.arrived and not drone.in_transit:
                    zone_occupancy[drone.pos] = zone_occupancy.get(drone.pos, 0) + 1

            max_drones_cp: dict[str, int] = {
                zone: cap - zone_occupancy.get(zone, 0)
                for zone, cap in self._max_drones.items()
            }

            max_link_capacity_cp = self._max_link_capacity.copy()
            turn_output: list[str] = []

            for drone in drones:
                if not drone.arrived and drone.in_transit:
                    next_zone = drone.path[drone.path_idx + 1]
                    cur_zone = drone.path[drone.path_idx]

                    if next_zone in max_drones_cp:
                        max_drones_cp[next_zone] -= 1

                    if (cur_zone, next_zone) in max_link_capacity_cp:
                        max_link_capacity_cp[(cur_zone, next_zone)] -= 1

            for drone in drones:
                if not drone.arrived:
                    cur_zone = drone.path[drone.path_idx]
                    next_zone = drone.path[drone.path_idx + 1]
                    moved = False
                    started_transit = False

                    if next_zone != self._end:
                        if drone.in_transit:
                            drone.pos = next_zone
                            drone.path_idx += 1
                            drone.in_transit = False
                            moved = True

                        elif self._control_zone.get(next_zone) == 'restricted':
                            if (max_drones_cp[next_zone] > 0
                                    and max_link_capacity_cp[cur_zone, next_zone] > 0):

                                if cur_zone in max_drones_cp:
                                    max_drones_cp[cur_zone] += 1
                                max_drones_cp[next_zone] -= 1
                                max_link_capacity_cp[cur_zone, next_zone] -= 1
                                drone.in_transit = True
                                started_transit = True

                        elif (max_drones_cp[next_zone] > 0
                                and max_link_capacity_cp[cur_zone, next_zone] > 0):
                            if cur_zone in max_drones_cp:
                                max_drones_cp[cur_zone] += 1
                            max_drones_cp[next_zone] -= 1
                            max_link_capacity_cp[cur_zone, next_zone] -= 1
                            drone.pos = next_zone
                            drone.path_idx += 1
                            moved = True

                    else:
                        if cur_zone in max_drones_cp:
                            max_drones_cp[cur_zone] += 1
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

            snapshots.append(snapshot())
            tours += 1

        print(tours)

        return snapshots
