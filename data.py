class StartHub:

    def __init__(
            self, start_hub: str, start_coords: tuple[int, int]) -> None:
        self.start_hub = start_hub
        self.start_coords = start_coords


class EndHub:

    def __init__(
            self, end_hub: str, end_coords: tuple[int, int]) -> None:
        self.end_hub = end_hub
        self.end_coords = end_coords


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
            start_coords: tuple[int, int], end_coords: tuple[int, int]
            ) -> None:
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.start_coords = start_coords
        self.end_coords = end_coords
