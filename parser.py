import sys
from typing import Any
from data import StartHub, EndHub, Hub, Connection


def read_fd(fd: str) -> list[str]:

    content: list[str] = []

    try:
        with open(fd, "r") as f:
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


def check_keywords(content: list[str]) -> None:

    prefixes = [
        "nb_drones:",
        "start_hub:",
        "end_hub:",
        "hub:",
        "connection:"
    ]

    start: bool = False
    for c in content:
        start = any(c.startswith(prefix) for prefix in prefixes)
        if start is False:
            print(
                "[ERROR]: Each line must begin with one of these keywords: "
                "nb_drones:, start_hub:, end_hub:, hub:, connection:"
            )
            sys.exit(1)


def check_first_line(content: list[str]) -> int:

    nb_drones: str = content[0]
    if not nb_drones.startswith('nb_drones:'):
        print(
            "[ERROR]: The first line must start with "
            "nb_drones: <positive_integer>."
        )
        sys.exit(1)

    drones: list[str] = nb_drones.split(':')
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


def categorize_lines(
        content: list[str]
        ) -> tuple[list[str], list[str], list[str], list[str]]:

    start_hub: list[str] = []
    hub: list[str] = []
    end_hub: list[str] = []
    connection: list[str] = []

    for c in content:
        if c.startswith("start_hub:"):
            start_hub.append(c)
        if c.startswith("hub:"):
            hub.append(c)
        if c.startswith("end_hub:"):
            end_hub.append(c)
        if c.startswith("connection:"):
            connection.append(c)

    return start_hub, hub, end_hub, connection


def strip_prefix(data: list[str]) -> list[str]:

    info: list[list[str]] = []

    for d in data:
        info.append(d.split(':'))
    data.clear()
    for i in info:
        data.append(i[1].strip())

    if data == ['']:
        print('[ERROR]: Expected a value after keyword but got nothing.')
        sys.exit(1)

    return data


def check_name(name: str) -> None:

    if name.find('-') != -1:
        print("[ERROR]: <name> must not contain '-'.")
        sys.exit(1)


def parse_name_coords(
        base_data_list: list[str]) -> tuple[str, tuple[int, int]]:

    try:
        if len(base_data_list) != 3:
            print(
                "[ERROR]: A hub must contain exactly 3 values: <name> <x> <y>."
            )
            sys.exit(1)
        name: str = base_data_list[0]
        check_name(name)
        coords: tuple[int, int] = (
            int(base_data_list[1]), int(base_data_list[2])
        )
    except ValueError as err:
        print(f"[ERROR]: {err}")
        sys.exit(1)

    return name, coords


def check_metadata(
        metadata: list[str],
        dict_base: dict[str, Any]) -> dict[str, Any]:

    keys_base = ['zone', 'color', 'max_drones']
    zone_base = ['normal', 'blocked', 'restricted', 'priority']

    keys_list: list[str] = []
    for data in metadata:
        key = data.split('=')[0]
        keys_list.append(key)

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

            else:
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


def split_hub(
        data: str) -> tuple[str, tuple[int, int], dict[str, Any]]:

    dict_base: dict[str, Any] = {
        'zone': 'normal',
        'color': None,
        'max_drones': 1
    }

    if data.find('[') != -1:
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
        name, coords = parse_name_coords(base_data_list)

        meta_data_list = meta_data.split()
        dict_base = check_metadata(
            meta_data_list, dict_base
        )

        return name, coords, dict_base

    else:
        base_data_list = data.split()
        name, coords = parse_name_coords(base_data_list)

        return name, coords, dict_base


def check_unique_names(name_list: list[str]) -> None:

    if len(name_list) != len(set(name_list)):
        print("[ERROR]: Each zone must have a unique name.")
        sys.exit(1)


def separate_connection(
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


def check_link_capacity(
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


def check_connection(
        connection: str,
        name_list: list[str]) -> tuple[str, str, dict[str, int]]:

    metadata: dict[str, int] = {
        'max_link_capacity': 1
    }

    connection = connection.removeprefix("connection:")

    try:
        if connection.find('[') != -1:
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

            zone_a, zone_b = separate_connection(base_connection, name_list)
            metadata = check_link_capacity(meta_connection, metadata)

        else:
            zone_a, zone_b = separate_connection(connection, name_list)
    except IndexError as err:
        print(f"[ERROR]: {err}")
        sys.exit(1)

    return zone_a, zone_b, metadata


def parse_start_hub(
        start_hub: list[str],
        name_list: list[str],
        nb_drones: int) -> tuple[StartHub, list[str]]:

    start_hub = strip_prefix(start_hub)
    if len(start_hub) != 1:
        print("[ERROR]: There must be exactly one start_hub defined.")
        sys.exit(1)
    name, coords, metadata = split_hub(start_hub[0])
    name_list.append(name)
    start = StartHub(name, coords, metadata['color'], nb_drones)

    return start, name_list


def parse_hubs(
        hub: list[str],
        name_list: list[str]) -> tuple[list[Hub], list[str]]:

    hub = strip_prefix(hub)
    hub_class: list[Hub] = []
    for h in hub:
        name, coords, metadata = split_hub(h)
        name_list.append(name)
        check_unique_names(name_list)
        hub_cla = Hub(
            name, coords, metadata['zone'],
            metadata['color'], metadata['max_drones']
        )
        hub_class.append(hub_cla)

    return hub_class, name_list


def parse_end_hub(
        end_hub: list[str],
        name_list: list[str]) -> tuple[EndHub, list[str]]:

    end_hub = strip_prefix(end_hub)
    if len(end_hub) != 1:
        print("[ERROR]: There must be exactly one end_hub defined.")
        sys.exit(1)
    name, coords, metadata = split_hub(end_hub[0])
    name_list.append(name)
    check_unique_names(name_list)
    end = EndHub(name, coords, metadata['color'])

    return end, name_list


def parse_connections(
        connection: list[str],
        name_list: list[str]) -> list[Connection]:

    frozen_list: list[frozenset[str]] = []
    hub_connection: list[Connection] = []
    for c in connection:
        zone_a, zone_b, co_metadata = check_connection(c, name_list)
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


def main_parser(
        fd: str
        ) -> tuple[StartHub, list[Hub], EndHub, list[Connection]]:

    content = read_fd(fd)
    nb_drones = check_first_line(content)

    check_keywords(content)

    start_hub, hub, end_hub, connection = categorize_lines(content)
    name_list: list[str] = []

    start, name_list = parse_start_hub(start_hub, name_list, nb_drones)

    hub_class: list[Hub] = []
    hub_class, name_list = parse_hubs(hub, name_list)

    end, name_list = parse_end_hub(end_hub, name_list)

    hub_connection: list[Connection] = []
    hub_connection = parse_connections(connection, name_list)

    return start, hub_class, end, hub_connection
