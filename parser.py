import sys
from typing import Any
from data import DroneSetUp, HubSetUp
from termcolor import colored
from simple_term_menu import TerminalMenu


def banned_area_name(area_name: str) -> None:

    area_name = area_name.strip()
    if area_name.find(' ') != -1 or area_name.find('-') != -1:
        print('[Warning]: Area name must not contains dashes or spaces !')
        sys.exit(1)


def check_coords(coords: list[str]) -> tuple[int, int]:

    if len(coords) != 2:
        print(
            "[Warning]: Values must contains 2 elements ! "
            "Example: 4 7"
        )
        sys.exit(1)
    try:
        coords[0] = int(coords[0])
        coords[1] = int(coords[1])
    except ValueError:
        print(
            "[Warning]: Values must be integers ! "
            "Example: 4 7"
        )
        sys.exit(1)
    for value in coords:
        if value < 0:
            print("Values must be positive")
            sys.exit(1)
    coords = tuple(coords)


def menu_zone() -> None:

    print('Choose an option for the zone (default: normal) :')
    options = ["normal", "priority", "restricted", "blocked"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

    return options[menu_entry_index]


def menu_color() -> None:

    print('Choose a color (default: none): ')
    options = [
        "red",
        "blue",
        "cyan",
        "green",
        "magenta",
        "none"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
        print(colored("Red color selected !", 'light_red'))
    if menu_entry_index == 1:
        print(colored("Blue color selected !", 'light_blue'))
    if menu_entry_index == 2:
        print(colored("Purple color selected !", 'light_cyan'))
    if menu_entry_index == 3:
        print(colored("Green color selected !", 'light_green'))
    if menu_entry_index == 4:
        print(colored("Mangenta color selected !", "light_magenta"))
    if menu_entry_index == 5:
        print("No color selected !")

    return options[menu_entry_index]


def drone_set_up() -> tuple[Any]:

    try:
        nb_drones = int(input('Number of drones: '))
    except ValueError:
        print("[Warning]: Drones value must be an integer !")
        sys.exit(1)

    start_hub = input("Enter a name for the starting area: ")
    banned_area_name(start_hub)

    end_hub = input("Enter a name for the ending area: ")
    banned_area_name(end_hub)

    start_coords = list((input(
            'Enter the starting position, '
            'coordinates x, y must be separated by spaces: '
            ).split()))
    start_coords = check_coords(start_coords)

    end_coords = list((input(
        'Enter the ending position, '
        'coordinates x, y must be separated by spaces: '
        ).split()))
    end_coords = check_coords(end_coords)

    return nb_drones, start_hub, end_hub, start_coords, end_coords


def hub_set_up():

    hub_name = input("Choose a name for the hub: ")
    banned_area_name(hub_name)

    coords = list((input(
            'Enter coordinates for the hub, '
            'coordinates x, y must be separated by spaces: '
            ).split()))
    coords = check_coords(coords)

    zone = menu_zone()

    color = menu_color()


def main() -> None:

    nb_drones, start_hub, end_hub, start_coords, end_coords = drone_set_up()
    DroneSetUp(nb_drones, start_hub, end_hub, start_coords, end_coords)

    try:
        hub_nb = int(input('Enter the number of zones you wish to create: '))
    except ValueError:
        print("[Warning]: Value must be an integer !")
        sys.exit(1)

    for _ in range(hub_nb):
        hub_set_up()


if __name__ == "__main__":
    main()