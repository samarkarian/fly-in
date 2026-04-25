class StartHub:

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            color: str, nb_drones: int) -> None:

        self.name = name
        self.coords = coords
        self.color = color
        self.nb_drones = nb_drones
        self.zone = 'normal'


class Hub:

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            zone: str, color: str | None,
            max_drones: int) -> None:

        self.name = name
        self.coords = coords
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class EndHub:

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            color: str) -> None:

        self.name = name
        self.coords = coords
        self.color = color
        self.zone = 'normal'


class Connection:

    def __init__(
            self,
            zone_a: str, zone_b: str,
            max_link_capacity: int) -> None:

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
