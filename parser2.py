import sys


def read_fd(fd: str) -> list[str]:

    content: list[str] = []

    try:
        with open(fd, "r") as f:
            for line in f:
                if not line.strip().startswith('#') and not line.strip() == '':
                    content.append(line.strip())
    except FileNotFoundError:
        print("[ERROR]: File not found !")
        sys.exit(1)
    except PermissionError:
        print("[ERROR]: Permission denied !")
        sys.exit(1)

    return content


def check_key(content: list[str]) -> None:

    prefixes = [
        "nb_drones:",
        "start_hub:",
        "end_hub:",
        "hub:",
        "connection:"
    ]

    res = False
    for c in content:
        res = any(c.startswith(prefix) for prefix in prefixes)
        if res is False:
            sys.exit(1)
        else:
            print(res)

    # x = []
    # for c in content:
    #     x.append(c.split(':'))

    # print(x)

    # for x[0] in x:
    #     print(x[0])

    # for c in content:
    #     if c not in prefixes:
    #         print("[ERROR]: ")
    #         sys.exit(1)

    # for prefix in prefixes:

    # for c in content:
    #     if not c.startswith("")


def check_start(content: list[str]):

    nb_drones: str = content[0]
    if not nb_drones.startswith('nb_drones:'):
        print(
            "[ERROR]: The first line must be start with "
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
        print("[ERROR]: Number of drones must be an integer.")
        sys.exit(1)


def main_parser(fd: str) -> None:

    content = read_fd(fd)
    check_start(content)
    check_key(content)
