import sys
from parser import Parser
from graph import main_graph
from dijkstra import Dijkstra
from simulator import Simulator
from visualizer import Visualizer


def main() -> None:
    """Parse input, compute paths, run simulation, and open the visualizer."""
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

    if not paths:
        print("[ERROR]: No path found between start and end zones.")
        sys.exit(1)

    turns = Simulator(paths, total_drones, hub_class, adjacency_dict.adjacency).run()
    Visualizer(start, hub_class, end, adjacency_dict.adjacency, turns).show()


if __name__ == "__main__":
    main()
