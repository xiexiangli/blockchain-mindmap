"""Generate and display a real-time random time-series line chart for 50 frames."""

from __future__ import annotations

import random

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


TOTAL_FRAMES = 50


class RealtimeTimeSeries:
    def __init__(self) -> None:
        self.x_data: list[int] = []
        self.y_data: list[float] = []

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.line, = self.ax.plot([], [], color="#1f77b4", linewidth=2)

        self.ax.set_title("Random Time-Series (Real Time)")
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Value")
        self.ax.set_xlim(0, TOTAL_FRAMES - 1)
        self.ax.set_ylim(0, 100)
        self.ax.grid(True, alpha=0.3)

    def init_chart(self):
        self.line.set_data([], [])
        return (self.line,)

    def update(self, frame: int):
        self.x_data.append(frame)

        previous = self.y_data[-1] if self.y_data else 50.0
        step = random.uniform(-8, 8)
        next_value = max(0.0, min(100.0, previous + step))
        self.y_data.append(next_value)

        self.line.set_data(self.x_data, self.y_data)
        return (self.line,)

    def run(self) -> None:
        _animation = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init_chart,
            frames=TOTAL_FRAMES,
            interval=120,
            repeat=False,
            blit=True,
        )
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    RealtimeTimeSeries().run()
