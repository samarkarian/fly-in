import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from typing import Any
from data import Hub, StartHub, EndHub

DRONE_COLORS = [
    'red', 'royalblue', 'limegreen', 'gold', 'purple',
    'teal', 'orange', 'deeppink', 'brown', 'navy', 'olive', 'coral',
]

HUB_COLORS: dict[Any, str] = {
    'green': '#27ae60', 'orange': '#e67e22', 'blue': '#2980b9',
    'red': '#e74c3c', 'cyan': '#17a589', 'yellow': '#f1c40f',
    None: '#ecf0f1',
}


class Visualizer:
    """Graphical step-through visualizer for the drone
    simulation using matplotlib."""

    def __init__(
            self,
            start: StartHub,
            hub_class: list[Hub],
            end: EndHub,
            adjacency: dict[str, list[tuple[str, int]]],
            turns: list[list[tuple[str, str, bool, str]]]) -> None:
        """Initialize the Visualizer with network data and
        simulation snapshots.

        Args:
            start (StartHub): Starting hub.
            hub_class (list[Hub]): All intermediate hubs.
            end (EndHub): Destination hub.
            adjacency (dict[str, list[tuple[str, int]]]): Adjacency
                list mapping zone names to (neighbor, capacity) pairs.
            turns (list[list[tuple[str, str, bool, str]]]): Per-turn
                snapshots of (id, pos, in_transit, next_zone).
        """
        self.hub_map: dict[str, Hub | StartHub | EndHub] = {
            start.name: start, end.name: end
        }

        for h in hub_class:
            self.hub_map[h.name] = h

        self.adjacency = adjacency
        self.turns = turns
        self.turn = 0

        self.pos = {name: hub.coords for name, hub in self.hub_map.items()}

        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.fig.subplots_adjust(bottom=0.12)

        ax_prev = self.fig.add_axes((0.35, 0.02, 0.12, 0.05))
        ax_next = self.fig.add_axes((0.53, 0.02, 0.12, 0.05))
        self.btn_prev = Button(ax_prev, '← Prev')
        self.btn_next = Button(ax_next, 'Next →')
        self.btn_prev.on_clicked(self.go_prev)
        self.btn_next.on_clicked(self.go_next)

    def show(self) -> None:
        """Draw the initial state and open the matplotlib
        interactive window."""
        self.draw()
        plt.show()

    def go_prev(self, _event: Any) -> None:
        """Step backward one turn when the Prev button is clicked.

        Args:
            _event (Any): Matplotlib click event (unused).
        """
        if self.turn > 0:
            self.turn -= 1
            self.draw()
            self.fig.canvas.draw_idle()

    def go_next(self, _event: Any) -> None:
        """Step forward one turn when the Next button is clicked.

        Args:
            _event (Any): Matplotlib click event (unused).
        """
        if self.turn < len(self.turns) - 1:
            self.turn += 1
            self.draw()
            self.fig.canvas.draw_idle()

    def draw(self) -> None:
        """Redraw edges, hubs, and drone positions for the current turn."""
        self.ax.clear()
        self.ax.axis('off')

        seen: set[frozenset[str]] = set()
        for zone, neighbors in self.adjacency.items():
            for neighbor, cap in neighbors:
                edge: frozenset[str] = frozenset({zone, neighbor})
                if edge in seen:
                    continue
                seen.add(edge)
                x0, y0 = self.pos[zone]
                x1, y1 = self.pos[neighbor]
                self.ax.plot(
                    [x0, x1], [y0, y1], color='gray', linewidth=2, zorder=1
                )
                self.ax.text(
                    (x0 + x1) / 2, (y0 + y1) / 2 + 0.1,
                    str(cap), fontsize=7, ha='center', color='gray', zorder=2,
                )

        for name, hub in self.hub_map.items():
            x, y = self.pos[name]
            color = HUB_COLORS.get(hub.color, '#ecf0f1')
            self.ax.add_patch(
                mpatches.Circle(
                    (x, y), 0.3, color=color, ec='black', lw=1.5, zorder=3
                )
            )
            self.ax.text(
                x, y - 0.45, name, fontsize=7, ha='center', va='top', zorder=4
            )

        for drone_id, pos, in_transit, next_zone in self.turns[self.turn]:
            if in_transit:
                x0, y0 = self.pos[pos]
                x1, y1 = self.pos[next_zone]
                dx, dy = (x0 + x1) / 2, (y0 + y1) / 2
            else:
                dx, dy = self.pos[pos]

            color = DRONE_COLORS[(int(drone_id[1:]) - 1) % len(DRONE_COLORS)]
            self.ax.add_patch(
                mpatches.Circle(
                    (dx, dy), 0.13, color=color, ec='black', lw=0.8, zorder=5
                )
            )
            self.ax.text(
                dx, dy, drone_id,
                fontsize=5, ha='center', va='center',
                color='white', fontweight='bold', zorder=6,
            )

        xs = [c[0] for c in self.pos.values()]
        ys = [c[1] for c in self.pos.values()]
        self.ax.set_xlim(min(xs) - 1, max(xs) + 1)
        self.ax.set_ylim(min(ys) - 1, max(ys) + 1)
        self.ax.set_aspect('equal')
        self.ax.set_title(
            f'Turn {self.turn} / {len(self.turns) - 1}  |  <- -> to navigate',
            fontsize=12,
        )
