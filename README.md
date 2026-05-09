*This project has been created as part of the 42 curriculum by samarkar.*

## Description

Fly-in is a drone routing simulation written in Python. The goal is to move a fleet
of drones from a start hub to an end hub in the fewest possible simulation turns,
while respecting zone capacity, link capacity, and movement cost constraints.

The program reads a map file that defines hubs, zone types, connections and
capacities, then computes optimal paths, runs the simulation, and renders an
interactive graphical view of each turn.

## Instructions

### Requirements

- Python 3.10 or later
- matplotlib, mypy, flake8

### Installation

```bash
make install
```

### Running

```bash
make run ARGS=maps/easy/01_simple.txt
```

### Debug mode

```bash
make debug ARGS=maps/easy/01_simple.txt
```

### Linting

```bash
make lint
```

### Clean

```bash
make clean
```

## Algorithm explanation

### Pathfinding — Dijkstra with penalties

The algorithm uses a modified Dijkstra's algorithm run iteratively to discover
multiple distinct paths:

1. **First run**: standard Dijkstra, weighting each node by its zone cost
   (`normal`/`priority` = 1 turn, `restricted` = 2 turns, `blocked` = skipped).
2. **Subsequent runs**: nodes that appear in already-found paths receive a +100
   penalty, steering the next search toward a different route.
3. The loop runs up to `nb_drones` times and stops early when no new distinct
   path can be found.

This produces a set of diverse paths that drones are assigned to in round-robin
order, spreading traffic across the graph to maximise simultaneous throughput.

### Simulation

The simulator advances one discrete turn at a time:

- **Occupancy tracking**: at the start of each turn, available capacity per zone
  is computed as `max_drones − current_occupancy` (in-transit drones do not
  count as occupying their source zone).
- **Pre-commit pass**: drones already in transit reserve capacity in their
  destination zone before other drones are allowed to move.
- **Movement pass**: each drone attempts to advance. Normal/priority zones are
  reached in 1 turn. Restricted zones take 2 turns — the drone is marked
  `in_transit` on turn 1 and arrives on turn 2; it cannot wait on the connection.
- Drones that cannot move simply wait; they are omitted from the turn output.

The simulation ends when every drone has reached the end hub. The total number
of turns is printed as the final line.

## Visual representation

The graphical interface is built with **matplotlib** and displays the hub network
and drone positions at each simulation turn:

- **Hubs** are drawn as coloured circles using the `color` attribute defined
  in the map file metadata (e.g. `color=green`, `color=red`). Hubs with no
  `color` attribute are drawn in light grey.
- **Edges** are drawn in grey with the `max_link_capacity` value shown at the
  midpoint.
- **Drones** appear as small coloured circles on their current hub. Drones that
  are in transit between two hubs (restricted zone movement) are placed at the
  midpoint of the corresponding edge.
- Navigation is done via the **← Prev** and **Next →** buttons at the bottom of
  the window, allowing step-by-step replay of the entire simulation.

## Example

Input (`maps/easy/01_simple.txt`):
```
nb_drones: 2
start_hub: start 0 0 [color=green max_drones=2]
hub: mid 1 0 [color=blue]
end_hub: goal 2 0 [color=green max_drones=2]
connection: start-mid
connection: mid-goal
```

Output:
```
D1-mid
D1-goal D2-mid
D2-goal
3
```

## Resources

- Dijkstra's algorithm — [Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- Python `heapq` module — [docs.python.org](https://docs.python.org/3/library/heapq.html)
- matplotlib documentation — [matplotlib.org](https://matplotlib.org/stable/index.html)
- PEP 257 — Docstring Conventions — [python.org](https://peps.python.org/pep-0257/)
- https://www.w3schools.com
- https://www.geeksforgeeks.org
- https://stackoverflow.com/questions

### AI usage

Claude Code was used throughout this project to:

- Fix mypy type errors
- Write README.md

All generated code was reviewed, tested against every provided map, and
understood before being included in the project.
