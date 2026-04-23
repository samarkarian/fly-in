import sys
from parser import main_parser
from graph import main_graph


def main() -> None:

    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        print(
            "[ERROR] -> Usage: python fly_in.py <file.txt> "
        )
        sys.exit(1)

    fd = sys.argv[1]

    _, _, _, hub_connection = main_parser(fd)
    main_graph(hub_connection)


if __name__ == "__main__":
    main()
