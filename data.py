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

    def __init__(self, hub_name, hub_coords, zone, color, max_drones) -> None:

        self.hub_name = hub_name
        self.hub_coords = hub_coords
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class Connection:

    def __init__(
            self,
            nb_drones: int, start_hub: str, end_hub: str,
            start_coords: tuple[int, int], end_coords: tuple[int, int],
            max_link_capacity: int
            ) -> None:
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.max_link_capacity = max_link_capacity
