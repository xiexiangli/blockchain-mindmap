"""Professional animated time-series visualization.

Usage:
    python animated_timeseries.py --input sample_timeseries.json --output timeseries_animation.mp4

JSON schema:
{
  "title": "KPI Trend",
  "x_label": "Date",
  "y_label": "Value",
  "series": [
    {"time": "2026-01-01", "value": 120},
    {"time": "2026-01-02", "value": 127}
  ]
}
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from datetime import datetime


@dataclass(frozen=True)
class TimePoint:
    """Single time-series observation."""

    timestamp: datetime
    value: float


@dataclass
class TimeSeriesConfig:
    """Configuration parsed from JSON input."""

    title: str
    x_label: str
    y_label: str
    points: List[TimePoint]


class TimeSeriesLoader:
    """Loads and validates time-series JSON data."""

    @staticmethod
    def load_from_json(path: Path) -> TimeSeriesConfig:
        data = json.loads(path.read_text(encoding="utf-8"))

        if "series" not in data or not isinstance(data["series"], list):
            raise ValueError("JSON must contain a 'series' array.")

        points: List[TimePoint] = []
        for i, item in enumerate(data["series"]):
            if not isinstance(item, dict):
                raise ValueError(f"series[{i}] must be an object.")

            if "time" not in item or "value" not in item:
                raise ValueError(f"series[{i}] requires 'time' and 'value'.")

            try:
                timestamp = datetime.fromisoformat(str(item["time"]))
            except ValueError as exc:
                raise ValueError(
                    f"series[{i}].time '{item['time']}' must be ISO-8601 format."
                ) from exc

            value = float(item["value"])
            points.append(TimePoint(timestamp=timestamp, value=value))

        points.sort(key=lambda p: p.timestamp)

        if not points:
            raise ValueError("series cannot be empty.")

        return TimeSeriesConfig(
            title=str(data.get("title", "Time-Series Animation")),
            x_label=str(data.get("x_label", "Time")),
            y_label=str(data.get("y_label", "Value")),
            points=points,
        )


class TimeSeriesAnimator:
    """Builds and exports an animated time-series chart."""

    def __init__(self, config: TimeSeriesConfig, fps: int = 30, interval_ms: int = 60) -> None:
        self.config = config
        self.fps = fps
        self.interval_ms = interval_ms

        self.fig: Figure
        self.ax: Axes
        self.line = None
        self.scatter = None
        self.annotation = None

    def _setup_figure(self) -> None:
        plt.style.use("seaborn-v0_8-whitegrid")
        self.fig, self.ax = plt.subplots(figsize=(12, 7), dpi=120)

        dates = [p.timestamp for p in self.config.points]
        values = [p.value for p in self.config.points]

        self.ax.set_title(self.config.title, fontsize=20, fontweight="bold", pad=18)
        self.ax.set_xlabel(self.config.x_label, fontsize=13)
        self.ax.set_ylabel(self.config.y_label, fontsize=13)

        y_min, y_max = min(values), max(values)
        y_pad = (y_max - y_min) * 0.15 if y_max > y_min else 1.0

        self.ax.set_xlim(min(dates), max(dates))
        self.ax.set_ylim(y_min - y_pad, y_max + y_pad)
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))

        self.line, = self.ax.plot([], [], linewidth=2.8, color="#0B6EFD", label="Observed")
        self.scatter = self.ax.scatter([], [], s=80, color="#FF6B35", zorder=3)
        self.annotation = self.ax.text(
            0.02,
            0.92,
            "",
            transform=self.ax.transAxes,
            fontsize=12,
            bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "#d0d0d0"},
        )

        self.ax.fill_between(dates, values, y2=y_min - y_pad, alpha=0.08, color="#0B6EFD")
        self.ax.legend(loc="upper left", frameon=False)

    def _init_animation(self):
        self.line.set_data([], [])
        self.scatter.set_offsets([])
        self.annotation.set_text("")
        return self.line, self.scatter, self.annotation

    def _animate_frame(self, frame: int):
        subset = self.config.points[: frame + 1]
        dates = [p.timestamp for p in subset]
        values = [p.value for p in subset]

        self.line.set_data(dates, values)
        self.scatter.set_offsets([[mdates.date2num(dates[-1]), values[-1]]])

        self.annotation.set_text(
            f"Date: {dates[-1].date().isoformat()}\nValue: {values[-1]:,.2f}"
        )
        return self.line, self.scatter, self.annotation

    def render(self, output_path: Path) -> None:
        self._setup_figure()
        anim = FuncAnimation(
            self.fig,
            self._animate_frame,
            init_func=self._init_animation,
            frames=len(self.config.points),
            interval=self.interval_ms,
            blit=True,
            repeat=False,
        )

        writer = FFMpegWriter(
            fps=self.fps,
            codec="libx264",
            bitrate=2400,
            extra_args=["-pix_fmt", "yuv420p"],
        )
        anim.save(str(output_path), writer=writer)
        plt.close(self.fig)


class App:
    """CLI app entry point."""

    @staticmethod
    def run() -> None:
        parser = argparse.ArgumentParser(description="Animate time-series JSON and export to MP4.")
        parser.add_argument("--input", required=True, type=Path, help="Path to input JSON file")
        parser.add_argument("--output", required=True, type=Path, help="Path to output MP4 file")
        parser.add_argument("--fps", type=int, default=30, help="Frames per second for output video")
        parser.add_argument("--interval-ms", type=int, default=60, help="Frame interval in milliseconds")
        args = parser.parse_args()

        config = TimeSeriesLoader.load_from_json(args.input)
        animator = TimeSeriesAnimator(config=config, fps=args.fps, interval_ms=args.interval_ms)
        animator.render(args.output)
        print(f"Saved animation to: {args.output}")


if __name__ == "__main__":
    App.run()
