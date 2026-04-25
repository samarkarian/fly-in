import sys
from parser import main_parser
from graph import main_graph
from dijkstra import main_djikstra


def main() -> None:

    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        print(
            "[ERROR] -> Usage: python fly_in.py <file.txt> "
        )
        sys.exit(1)

    fd = sys.argv[1]

    start, hub_class, end, hub_connection = main_parser(fd)
    adjacency_dict = main_graph(hub_connection)
    main_djikstra(start, hub_class, end, adjacency_dict.adjacency)


if __name__ == "__main__":
    main()
