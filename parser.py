import sys
from typing import Any
from data import StartHub, EndHub, Hub, Connection


class Parser:
    """Parses a drone network map file into typed data objects."""

    def __init__(self, fd: str) -> None:
        """Initialize the Parser with the path to the input file."""
        self.fd = fd

    def parse(self) -> tuple[StartHub, list[Hub], EndHub, list[Connection]]:
        """Parse the file and return start hub, hubs,
        end hub and connections."""
        content = self.read_fd()
        nb_drones = self.check_first_line(content)
        self.check_keywords(content)
        start_hub, hub, end_hub, connection = self.categorize_lines(content)
        name_list: list[str] = []
        start, name_list = self.parse_start_hub(
            start_hub, name_list, nb_drones
        )
        hub_class, name_list = self.parse_hubs(hub, name_list)
        end, name_list = self.parse_end_hub(end_hub, name_list, nb_drones)
        hub_connection = self.parse_connections(connection, name_list)

        return start, hub_class, end, hub_connection

    def read_fd(self) -> list[tuple[int, str]]:
        """Read the file, strip comments and blank lines,
        and return (line_num, content) pairs."""
        content: list[tuple[int, str]] = []

        try:
            with open(self.fd, "r") as f:
                for i, line in enumerate(f, 1):
                    stripped = line.strip()
                    if not stripped.startswith('#') and stripped != '':
                        content.append((i, stripped))
        except FileNotFoundError:
            print("[ERROR]: File not found.")
            sys.exit(1)
        except PermissionError:
            print("[ERROR]: Permission denied.")
            sys.exit(1)

        return content

    def check_keywords(self, content: list[tuple[int, str]]) -> None:
        """Ensure every line starts with a recognised keyword prefix."""
        prefixes = [
            "nb_drones:",
            "start_hub:",
            "end_hub:",
            "hub:",
            "connection:"
        ]

        for line_num, c in content:
            valid = any(c.startswith(prefix) for prefix in prefixes)
            if not valid:
                print(
                    f"[ERROR] line {line_num}: Each line must begin"
                    " with one of these keywords: "
                    "nb_drones:, start_hub:, end_hub:, hub:, connection:"
                )
                sys.exit(1)

    def check_first_line(self, content: list[tuple[int, str]]) -> int:
        """Validate that the first line defines nb_drones
        and return its value."""
        line_num, nb_drones = content[0]

        if not nb_drones.startswith('nb_drones:'):
            print(
                f"[ERROR] line {line_num}: The first line must start with "
                "nb_drones: <positive_integer>."
            )
            sys.exit(1)

        drones: list[str] = nb_drones.split(':', 1)

        try:
            value = int(drones[1])
            if value <= 0:
                print(
                    f"[ERROR] line {line_num}: "
                    "Number of drones must be positive."
                )
                sys.exit(1)
        except ValueError as err:
            print(
                f"[ERROR] line {line_num}: "
                "Number of drones must be an integer "
                f"with only one value. {err}"
            )
            sys.exit(1)
        except IndexError as err:
            print(f"[ERROR] line {line_num}: {err}")
            sys.exit(1)
        return value

    def categorize_lines(
            self,
            content: list[tuple[int, str]]) -> tuple[
                list[tuple[int, str]],
                list[tuple[int, str]],
                list[tuple[int, str]],
                list[tuple[int, str]]]:

        """Split content lines into four lists by their keyword prefix."""

        start_hub: list[tuple[int, str]] = []
        hub: list[tuple[int, str]] = []
        end_hub: list[tuple[int, str]] = []
        connection: list[tuple[int, str]] = []

        for line_num, c in content:
            if c.startswith("start_hub:"):
                start_hub.append((line_num, c))
            elif c.startswith("hub:"):
                hub.append((line_num, c))
            elif c.startswith("end_hub:"):
                end_hub.append((line_num, c))
            elif c.startswith("connection:"):
                connection.append((line_num, c))

        return start_hub, hub, end_hub, connection

    def strip_prefix(
            self,
            data: list[tuple[int, str]]) -> list[tuple[int, str]]:
        """Remove the keyword prefix from each line
        and return (line_num, bare_value) pairs."""
        result: list[tuple[int, str]] = [
            (line_num, d.split(':', 1)[1].strip()) for line_num, d in data
        ]

        if len(result) == 1 and result[0][1] == '':
            print(
                f"[ERROR] line {result[0][0]}: "
                "Expected a value after keyword but got nothing."
            )
            sys.exit(1)

        return result

    def check_name(self, name: str, line_num: int) -> None:
        """Raise an error if the hub name contains
        a forbidden dash character."""
        if '-' in name:
            print(f"[ERROR] line {line_num}: <name> must not contain '-'.")
            sys.exit(1)

    def parse_name_coords(
            self,
            base_data_list: list[str],
            line_num: int) -> tuple[str, tuple[int, int]]:

        """Parse a three-token list into a hub name and integer coordinates."""

        try:
            if len(base_data_list) != 3:
                print(
                    f"[ERROR] line {line_num}: "
                    "A hub must contain exactly 3 values: <name> <x> <y>."
                )
                sys.exit(1)
            name: str = base_data_list[0]
            self.check_name(name, line_num)
            coords: tuple[int, int] = (
                int(base_data_list[1]), int(base_data_list[2])
            )
        except ValueError as err:
            print(f"[ERROR] line {line_num}: {err}")
            sys.exit(1)

        return name, coords

    def check_metadata(
            self,
            metadata: list[str],
            dict_base: dict[str, Any],
            line_num: int) -> dict[str, Any]:

        """Validate metadata key-value pairs and update the base dict."""

        keys_base = ['zone', 'color', 'max_drones']
        zone_base = ['normal', 'blocked', 'restricted', 'priority']
        keys_list: list[str] = [data.split('=')[0] for data in metadata]

        if len(keys_list) != len(set(keys_list)):
            print(
                f'[ERROR] line {line_num}: '
                'Duplicate keys found in metadata.'
            )
            sys.exit(1)

        for meta in metadata:
            try:
                key, val = meta.split('=')

                if key not in keys_base:
                    print(
                        f"[ERROR] line {line_num}: "
                        "Invalid key. Valid keys are: "
                        "'zone', 'color', 'max_drones'."
                    )
                    sys.exit(1)

                if key == 'zone':
                    if val not in zone_base:
                        print(
                            f"[ERROR] line {line_num}: "
                            "Invalid value for 'zone'. "
                            "Valid values are: 'normal', 'blocked', "
                            "'restricted', 'priority'."
                        )
                        sys.exit(1)

                elif key == 'max_drones':

                    try:
                        int_val = int(val)
                        if int_val <= 0:
                            print(
                                f"[ERROR] line {line_num}: "
                                "The value of 'max_drones' "
                                "must be a positive integer."
                            )
                            sys.exit(1)
                    except ValueError as err:
                        print(
                            f"[ERROR] line {line_num}: 'max_drones': {err}"
                        )
                        sys.exit(1)

                    dict_base[key] = int_val
                    continue

                dict_base[key] = val

            except ValueError as err:
                print(f"[ERROR] line {line_num}: {err}")
                sys.exit(1)

        return dict_base

    def split_hub(
            self,
            data: str,
            line_num: int) -> tuple[str, tuple[int, int], dict[str, Any]]:

        """Split a hub definition string into name,
        coords and metadata dict."""

        dict_base: dict[str, Any] = {
            'zone': 'normal',
            'color': None,
            'max_drones': 1
        }

        if '[' in data:
            parts = data.split("[")
            base_data: str = parts[0]
            meta_data: str = parts[1]

            if not meta_data.endswith(']'):
                print(
                    f'[ERROR] line {line_num}: Invalid metadata block, '
                    'must start with "[" and end with "]"'
                )
                sys.exit(1)
            else:
                meta_data = meta_data[:-1]

            base_data_list = base_data.split()
            name, coords = self.parse_name_coords(base_data_list, line_num)
            meta_data_list = meta_data.split()
            dict_base = self.check_metadata(
                meta_data_list, dict_base, line_num
            )

            return name, coords, dict_base

        else:
            base_data_list = data.split()
            name, coords = self.parse_name_coords(base_data_list, line_num)

            return name, coords, dict_base

    def check_unique_names(self, name_list: list[str], line_num: int) -> None:
        """Raise an error if any name appears more than once in the list."""
        if len(name_list) != len(set(name_list)):
            print(
                f"[ERROR] line {line_num}: "
                "Each zone must have a unique name."
            )
            sys.exit(1)

    def separate_connection(
            self,
            base_connection: str,
            name_list: list[str],
            line_num: int) -> tuple[str, str]:

        """Split a connection string into its two zone names."""

        try:
            parts = base_connection.strip().split('-')

            if len(parts) != 2:
                print(
                    f"[ERROR] line {line_num}: "
                    "Connection must follow the format <hub1>-<hub2>."
                )
                sys.exit(1)
            zone_a, zone_b = parts

            if zone_a not in name_list or zone_b not in name_list:
                print(
                    f"[ERROR] line {line_num}: "
                    f"Hub {repr(zone_a)} or {repr(zone_b)} "
                    "is not defined, connections must link existing hubs."
                )
                sys.exit(1)

        except ValueError as err:
            print(f"[ERROR] line {line_num}: {err}")
            sys.exit(1)

        return zone_a, zone_b

    def check_link_capacity(
            self,
            meta_connection: str,
            metadata: dict[str, int],
            line_num: int) -> dict[str, int]:

        """Validate the max_link_capacity metadata and store it in the dict."""

        try:
            is_several_elem = meta_connection.split()

            if len(is_several_elem) != 1:
                print(
                    f"[ERROR] line {line_num}: "
                    "Connection metadata must contain "
                    "exactly one key: 'max_link_capacity'."
                )
                sys.exit(1)

            key, val = meta_connection.split('=')
            int_value = int(val)

            if key != 'max_link_capacity':
                print(
                    f"[ERROR] line {line_num}: "
                    "Invalid key. Valid key is: 'max_link_capacity'"
                )
                sys.exit(1)

            if int_value < 1:
                print(
                    f"[ERROR] line {line_num}: "
                    "'max_link_capacity' must be a positive integer "
                    "greater than 0."
                )
                sys.exit(1)

        except ValueError as err:
            print(f"[ERROR] line {line_num}: {err}")
            sys.exit(1)

        metadata['max_link_capacity'] = int_value

        return metadata

    def check_connection(
            self,
            connection: str,
            name_list: list[str],
            line_num: int) -> tuple[str, str, dict[str, int]]:

        """Validate a full connection line and return
        both zones and metadata."""

        metadata: dict[str, int] = {'max_link_capacity': 1}
        connection = connection.removeprefix("connection:")

        try:
            if '[' in connection:
                parts = connection.split("[")
                base_connection: str = parts[0]
                meta_connection: str = parts[1]

                if not meta_connection.endswith(']'):
                    print(
                        f'[ERROR] line {line_num}: Invalid metadata block, '
                        'must start with "[" and end with "]"'
                    )
                    sys.exit(1)

                else:
                    meta_connection = meta_connection[:-1]
                zone_a, zone_b = self.separate_connection(
                    base_connection, name_list, line_num
                )
                metadata = self.check_link_capacity(
                    meta_connection, metadata, line_num
                )

            else:
                zone_a, zone_b = self.separate_connection(
                    connection, name_list, line_num
                )

        except IndexError as err:
            print(f"[ERROR] line {line_num}: {err}")
            sys.exit(1)

        return zone_a, zone_b, metadata

    def parse_start_hub(
            self,
            start_hub: list[tuple[int, str]],
            name_list: list[str],
            nb_drones: int) -> tuple[StartHub, list[str]]:

        """Parse the start_hub lines and return a StartHub instance."""
        start_hub = self.strip_prefix(start_hub)

        if len(start_hub) != 1:
            print("[ERROR]: There must be exactly one start_hub defined.")
            sys.exit(1)

        line_num, data = start_hub[0]
        name, coords, metadata = self.split_hub(data, line_num)
        name_list.append(name)
        start = StartHub(name, coords, metadata['color'], nb_drones)

        return start, name_list

    def parse_hubs(
            self,
            hub: list[tuple[int, str]],
            name_list: list[str]) -> tuple[list[Hub], list[str]]:

        """Parse all hub lines and return a list of Hub instances."""

        hub = self.strip_prefix(hub)
        hub_class: list[Hub] = []

        for line_num, h in hub:
            name, coords, metadata = self.split_hub(h, line_num)
            name_list.append(name)
            self.check_unique_names(name_list, line_num)
            hub_cla = Hub(
                name, coords, metadata['zone'],
                metadata['color'], metadata['max_drones']
            )
            hub_class.append(hub_cla)

        return hub_class, name_list

    def parse_end_hub(
            self,
            end_hub: list[tuple[int, str]],
            name_list: list[str],
            nb_drones: int) -> tuple[EndHub, list[str]]:

        """Parse the end_hub lines and return an EndHub instance."""

        end_hub = self.strip_prefix(end_hub)

        if len(end_hub) != 1:
            print("[ERROR]: There must be exactly one end_hub defined.")
            sys.exit(1)

        line_num, data = end_hub[0]
        name, coords, metadata = self.split_hub(data, line_num)
        name_list.append(name)
        self.check_unique_names(name_list, line_num)
        end = EndHub(name, coords, metadata['color'], nb_drones)

        return end, name_list

    def parse_connections(
            self,
            connection: list[tuple[int, str]],
            name_list: list[str]) -> list[Connection]:

        """Parse all connection lines and return
        a list of Connection instances."""

        frozen_list: list[frozenset[str]] = []
        hub_connection: list[Connection] = []

        for line_num, c in connection:
            zone_a, zone_b, co_metadata = self.check_connection(
                c, name_list, line_num
            )
            frozen_list.append(frozenset({zone_a, zone_b}))
            hub_co = Connection(
                zone_a, zone_b, co_metadata['max_link_capacity']
            )
            hub_connection.append(hub_co)

        if len(frozen_list) != len(set(frozen_list)):
            print(
                '[ERROR]: Duplicate connection found, '
                'each connection must be defined only once.'
            )
            sys.exit(1)

        return hub_connection
