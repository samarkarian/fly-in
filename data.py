class StartHub:

    def __init__(
            self, start_name: str,
            start_coords: tuple[int, int],
            color: str, nb_drones: int) -> None:

        self.start_name = start_name
        self.start_coords = start_coords
        self.color = color
        self.nb_drones = nb_drones


class EndHub:

    def __init__(
            self, end_name: str,
            end_coords: tuple[int, int],
            color: str) -> None:

        self.end_name = end_name
        self.end_coords = end_coords
        self.color = color


class Hub:

    def __init__(
            self, hub_name: str,
            hub_coords: tuple[int, int],
            zone: str, color: str | None,
            max_drones: int) -> None:

        self.hub_name = hub_name
        self.hub_coords = hub_coords
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class Connection:

    def __init__(
            self,
            zone_a: str, zone_b: str,
            max_link_capacity: int) -> None:

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
