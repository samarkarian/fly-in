class StartHub:
    """Represents the starting hub where all drones begin their journey."""

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            color: str, nb_drones: int) -> None:
        """Initialize a StartHub with its name, position,
        color and drone count."""
        self.name = name
        self.coords = coords
        self.color = color
        self.nb_drones = nb_drones
        self.zone = 'normal'
        self.max_drones = nb_drones


class Hub:
    """Represents a regular intermediate zone in the drone network."""

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            zone: str, color: str | None,
            max_drones: int) -> None:
        """Initialize a Hub with its name, position, zone type and capacity."""
        self.name = name
        self.coords = coords
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class EndHub:
    """Represents the destination hub where all drones must arrive."""

    def __init__(
            self, name: str,
            coords: tuple[int, int],
            color: str,
            nb_drones: int) -> None:
        """Initialize an EndHub with its name, position,
        color and drone count."""
        self.name = name
        self.coords = coords
        self.color = color
        self.zone = 'normal'
        self.nb_drones = nb_drones
        self.max_drones = nb_drones


class Connection:
    """Represents a bidirectional connection between two
    hubs with a capacity."""

    def __init__(
            self,
            zone_a: str, zone_b: str,
            max_link_capacity: int) -> None:
        """Initialize a Connection between two zones
        with a maximum link capacity."""
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity


class Drone:
    """Represents a single drone navigating through the hub network."""

    def __init__(
            self, id: str,
            pos: str,
            path_idx: int,
            arrived: bool,
            in_transit: bool,
            path: list[str]) -> None:
        """Initialize a Drone with its identifier,
        current state and assigned path."""
        self.id = id
        self.pos = pos
        self.path_idx = path_idx
        self.arrived = arrived
        self.in_transit = in_transit
        self.path = path
