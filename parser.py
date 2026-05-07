import sys
from typing import Any
from data import StartHub, EndHub, Hub, Connection


class Parser:

    def __init__(self, fd: str) -> None:
        self._fd = fd


    def parse(self) -> tuple[StartHub, list[Hub], EndHub, list[Connection]]:

        content = self._read_fd()
        nb_drones = self._check_first_line(content)
        self._check_keywords(content)
        start_hub, hub, end_hub, connection = self._categorize_lines(content)
        name_list: list[str] = []
        start, name_list = self._parse_start_hub(start_hub, name_list, nb_drones)
        hub_class, name_list = self._parse_hubs(hub, name_list)
        end, name_list = self._parse_end_hub(end_hub, name_list, nb_drones)
        hub_connection = self._parse_connections(connection, name_list)

        return start, hub_class, end, hub_connection


    def _read_fd(self) -> list[str]:

        content: list[str] = []

        try:
            with open(self._fd, "r") as f:
                for line in f:
                    if not line.strip().startswith('#') and not line.strip() == '':
                        content.append(line.strip())
        except FileNotFoundError:
            print("[ERROR]: File not found.")
            sys.exit(1)
        except PermissionError:
            print("[ERROR]: Permission denied.")
            sys.exit(1)

        return content


    def _check_keywords(self, content: list[str]) -> None:

        prefixes = [
            "nb_drones:",
            "start_hub:",
            "end_hub:",
            "hub:",
            "connection:"
        ]

        for c in content:
            valid = any(c.startswith(prefix) for prefix in prefixes)
            if not valid:
                print(
                    "[ERROR]: Each line must begin with one of these keywords: "
                    "nb_drones:, start_hub:, end_hub:, hub:, connection:"
                )
                sys.exit(1)


    def _check_first_line(self, content: list[str]) -> int:

        nb_drones: str = content[0]

        if not nb_drones.startswith('nb_drones:'):
            print(
                "[ERROR]: The first line must start with "
                "nb_drones: <positive_integer>."
            )
            sys.exit(1)

        drones: list[str] = nb_drones.split(':', 1)

        try:
            value = int(drones[1])
            if value <= 0:
                print("[ERROR]: Number of drones must be positive.")
                sys.exit(1)
        except ValueError:
            print(
                "[ERROR]: Number of drones must be an integer "
                "with only one value."
            )
            sys.exit(1)
        except IndexError as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)
        return value


    def _categorize_lines(
            self,
            content: list[str]) -> tuple[list[str], list[str], list[str], list[str]]:

        start_hub: list[str] = []
        hub: list[str] = []
        end_hub: list[str] = []
        connection: list[str] = []

        for c in content:
            if c.startswith("start_hub:"):
                start_hub.append(c)
            elif c.startswith("hub:"):
                hub.append(c)
            elif c.startswith("end_hub:"):
                end_hub.append(c)
            elif c.startswith("connection:"):
                connection.append(c)

        return start_hub, hub, end_hub, connection


    def _strip_prefix(self, data: list[str]) -> list[str]:

        result: list[str] = [d.split(':', 1)[1].strip() for d in data]

        if result == ['']:
            print('[ERROR]: Expected a value after keyword but got nothing.')
            sys.exit(1)

        return result


    def _check_name(self, name: str) -> None:

        if '-' in name:
            print("[ERROR]: <name> must not contain '-'.")
            sys.exit(1)


    def _parse_name_coords(
            self,
            base_data_list: list[str]) -> tuple[str, tuple[int, int]]:

        try:
            if len(base_data_list) != 3:
                print(
                    "[ERROR]: A hub must contain exactly 3 values: <name> <x> <y>."
                )
                sys.exit(1)
            name: str = base_data_list[0]
            self._check_name(name)
            coords: tuple[int, int] = (
                int(base_data_list[1]), int(base_data_list[2])
            )
        except ValueError as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)

        return name, coords


    def _check_metadata(
            self,
            metadata: list[str],
            dict_base: dict[str, Any]) -> dict[str, Any]:

        keys_base = ['zone', 'color', 'max_drones']
        zone_base = ['normal', 'blocked', 'restricted', 'priority']
        keys_list: list[str] = [data.split('=')[0] for data in metadata]

        if len(keys_list) != len(set(keys_list)):
            print('[ERROR]: Duplicate keys found in metadata.')
            sys.exit(1)

        for meta in metadata:
            try:
                key, val = meta.split('=')

                if key not in keys_base:
                    print(
                        "[ERROR]: Invalid key. Valid keys are: "
                        "'zone', 'color', 'max_drones'."
                    )
                    sys.exit(1)

                if key == 'zone':
                    if val not in zone_base:
                        print(
                            "[ERROR]: Invalid value for 'zone'. "
                            "Valid values are: 'normal', 'blocked', "
                            "'restricted', 'priority'."
                        )
                        sys.exit(1)

                elif key == 'max_drones':

                    try:
                        int_val = int(val)
                        if int_val < 0:
                            print(
                                "[ERROR]: The value of 'max_drones' "
                                "must be a positive integer."
                            )
                            sys.exit(1)
                    except ValueError as err:
                        print(f"[ERROR]: 'max_drones': {err}")
                        sys.exit(1)

                    dict_base[key] = int_val
                    continue

                dict_base[key] = val

            except ValueError as err:
                print(f"[ERROR]: {err}")
                sys.exit(1)

        return dict_base


    def _split_hub(
            self,
            data: str) -> tuple[str, tuple[int, int], dict[str, Any]]:

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
                    '[ERROR]: Invalid metadata block, '
                    'must start with "[" and end with "]"'
                )
                sys.exit(1)
            else:
                meta_data = meta_data[:-1]

            base_data_list = base_data.split()
            name, coords = self._parse_name_coords(base_data_list)
            meta_data_list = meta_data.split()
            dict_base = self._check_metadata(meta_data_list, dict_base)

            return name, coords, dict_base

        else:
            base_data_list = data.split()
            name, coords = self._parse_name_coords(base_data_list)

            return name, coords, dict_base


    def _check_unique_names(self, name_list: list[str]) -> None:

        if len(name_list) != len(set(name_list)):
            print("[ERROR]: Each zone must have a unique name.")
            sys.exit(1)


    def _separate_connection(
            self,
            base_connection: str,
            name_list: list[str]) -> tuple[str, str]:

        try:
            parts = base_connection.strip().split('-')

            if len(parts) != 2:
                print("[ERROR]: Connection must follow the format <hub1>-<hub2>.")
                sys.exit(1)
            zone_a, zone_b = parts

            if zone_a not in name_list or zone_b not in name_list:
                print(
                    f"[ERROR]: Hub {repr(zone_a)} or {repr(zone_b)} "
                    "is not defined, connections must link existing hubs."
                )
                sys.exit(1)

        except ValueError as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)

        return zone_a, zone_b

    def _check_link_capacity(
            self,
            meta_connection: str,
            metadata: dict[str, int]) -> dict[str, int]:

        try:
            is_several_elem = meta_connection.split()

            if len(is_several_elem) != 1:
                print(
                    "[ERROR]: Connection metadata must contain "
                    "exactly one key: 'max_link_capacity'."
                )
                sys.exit(1)

            key, val = meta_connection.split('=')
            int_value = int(val)

            if key != 'max_link_capacity':
                print(
                    "[ERROR]: Invalid key. Valid key is: 'max_link_capacity'"
                )
                sys.exit(1)

            if int_value < 1:
                print(
                    "[ERROR]: 'max_link_capacity' must be a positive integer "
                    "greater than 0."
                )
                sys.exit(1)

        except ValueError as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)

        metadata['max_link_capacity'] = int_value

        return metadata


    def _check_connection(
            self,
            connection: str,
            name_list: list[str]) -> tuple[str, str, dict[str, int]]:

        metadata: dict[str, int] = {'max_link_capacity': 1}
        connection = connection.removeprefix("connection:")

        try:
            if '[' in connection:
                parts = connection.split("[")
                base_connection: str = parts[0]
                meta_connection: str = parts[1]

                if not meta_connection.endswith(']'):
                    print(
                        '[ERROR]: Invalid metadata block, '
                        'must start with "[" and end with "]"'
                    )
                    sys.exit(1)

                else:
                    meta_connection = meta_connection[:-1]
                zone_a, zone_b = self._separate_connection(
                    base_connection, name_list
                )
                metadata = self._check_link_capacity(meta_connection, metadata)

            else:
                zone_a, zone_b = self._separate_connection(connection, name_list)

        except IndexError as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)

        return zone_a, zone_b, metadata


    def _parse_start_hub(
            self,
            start_hub: list[str],
            name_list: list[str],
            nb_drones: int) -> tuple[StartHub, list[str]]:

        start_hub = self._strip_prefix(start_hub)

        if len(start_hub) != 1:
            print("[ERROR]: There must be exactly one start_hub defined.")
            sys.exit(1)

        name, coords, metadata = self._split_hub(start_hub[0])
        name_list.append(name)
        start = StartHub(name, coords, metadata['color'], nb_drones)

        return start, name_list


    def _parse_hubs(
            self,
            hub: list[str],
            name_list: list[str]) -> tuple[list[Hub], list[str]]:

        hub = self._strip_prefix(hub)
        hub_class: list[Hub] = []

        for h in hub:
            name, coords, metadata = self._split_hub(h)
            name_list.append(name)
            self._check_unique_names(name_list)
            hub_cla = Hub(
                name, coords, metadata['zone'],
                metadata['color'], metadata['max_drones']
            )
            hub_class.append(hub_cla)

        return hub_class, name_list


    def _parse_end_hub(
            self,
            end_hub: list[str],
            name_list: list[str],
            nb_drones: int) -> tuple[EndHub, list[str]]:

        end_hub = self._strip_prefix(end_hub)

        if len(end_hub) != 1:
            print("[ERROR]: There must be exactly one end_hub defined.")
            sys.exit(1)

        name, coords, metadata = self._split_hub(end_hub[0])
        name_list.append(name)
        self._check_unique_names(name_list)
        end = EndHub(name, coords, metadata['color'], nb_drones)

        return end, name_list


    def _parse_connections(
            self,
            connection: list[str],
            name_list: list[str]) -> list[Connection]:

        frozen_list: list[frozenset[str]] = []
        hub_connection: list[Connection] = []

        for c in connection:
            zone_a, zone_b, co_metadata = self._check_connection(c, name_list)
            frozen_list.append(frozenset({zone_a, zone_b}))
            hub_co = Connection(zone_a, zone_b, co_metadata['max_link_capacity'])
            hub_connection.append(hub_co)

        if len(frozen_list) != len(set(frozen_list)):
            print(
                '[ERROR]: Duplicate connection found, '
                'each connection must be defined only once.'
            )
            sys.exit(1)

        return hub_connection
