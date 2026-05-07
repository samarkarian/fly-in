import sys
from parser import Parser
from graph import main_graph
from dijkstra import Dijkstra
from simulator import Simulator


def main() -> None:

    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        print(
            "[ERROR] -> Usage: python fly_in.py <file.txt> "
        )
        sys.exit(1)

    fd = sys.argv[1]
    start, hub_class, end, hub_connection = Parser(fd).parse()
    adjacency_dict = main_graph(hub_connection)
    paths, total_drones = Dijkstra(
        start, hub_class, end, adjacency_dict.adjacency
    ).run()
    Simulator(paths, total_drones, hub_class, adjacency_dict.adjacency).run()


if __name__ == "__main__":
    main()
