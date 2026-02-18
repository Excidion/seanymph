from __future__ import annotations

import math
import re
from pathlib import Path


def _format_category(label: str) -> str:
    """Return a Mermaid-safe category label, quoting if necessary."""
    s = str(label)
    if re.search(r'[\s,\[\]]', s):
        return f'"{s.replace(chr(34), chr(92) + chr(34))}"'
    return s


def _format_number(n: float) -> str:
    """Format a float cleanly, omitting .0 suffix for whole numbers."""
    if n == int(n):
        return str(int(n))
    return str(n)


class Figure:
    """A Mermaid xyChart diagram builder with a matplotlib-style fluent API."""

    def __init__(self, title: str | None = None) -> None:
        self._title = title
        self._x_categories: list[str] | None = None
        self._x_count: int | None = None  # length for numeric x, since no category list
        self._x_label: str | None = None
        self._x_min: float | None = None
        self._x_max: float | None = None
        self._y_label: str | None = None
        self._y_min: float | None = None
        self._y_max: float | None = None
        self._series: list[tuple[str, list[float]]] = []
        self._horizontal: bool | None = None

    def xlabel(self, label: str) -> Figure:
        self._x_label = label
        return self

    def ylabel(self, label: str) -> Figure:
        self._y_label = label
        return self

    def xlim(self, min: float, max: float) -> Figure:
        self._x_min = float(min)
        self._x_max = float(max)
        return self

    def ylim(self, min: float, max: float) -> Figure:
        self._y_min = float(min)
        self._y_max = float(max)
        return self

    def bar(self, x, y) -> Figure:
        self._set_x_axis(x)
        return self._add_series("bar", y, horizontal=False)

    def line(self, x, y) -> Figure:
        self._set_x_axis(x)
        return self._add_series("line", y, horizontal=False)

    def barh(self, x, y) -> Figure:
        self._set_x_axis(x)
        return self._add_series("bar", y, horizontal=True)

    def lineh(self, x, y) -> Figure:
        self._set_x_axis(x)
        return self._add_series("line", y, horizontal=True)

    def _set_x_axis(self, x) -> None:
        x_list = list(x)
        try:
            x_floats = [float(v) for v in x_list]
        except (TypeError, ValueError):
            x_floats = None

        if x_floats is not None:
            x_min, x_max = min(x_floats), max(x_floats)
            if self._x_min is not None and (self._x_min != x_min or self._x_max != x_max):
                raise ValueError(
                    f"x range [{x_min}, {x_max}] conflicts with existing x-axis range "
                    f"[{self._x_min}, {self._x_max}]"
                )
            self._x_min = x_min
            self._x_max = x_max
            self._x_count = len(x_floats)
        else:
            cats = [str(v) for v in x_list]
            if self._x_categories is not None and cats != self._x_categories:
                raise ValueError(
                    f"x values {cats} conflict with existing x-axis categories {self._x_categories}"
                )
            self._x_categories = cats

    def _add_series(self, series_type: str, data, horizontal: bool) -> Figure:
        if self._horizontal is not None and self._horizontal != horizontal:
            existing = "barh/lineh" if self._horizontal else "bar/line"
            new = "barh/lineh" if horizontal else "bar/line"
            raise ValueError(
                f"Cannot mix {existing} (horizontal={self._horizontal}) "
                f"with {new} (horizontal={horizontal})"
            )
        coerced: list[float] = []
        for i, v in enumerate(data):
            try:
                f = float(v)
            except (TypeError, ValueError):
                raise TypeError(f"data[{i}] is not numeric: {v!r}")
            if not math.isfinite(f):
                raise ValueError(f"data[{i}] is not finite: {v!r}")
            coerced.append(f)
        if not coerced:
            raise ValueError("data must not be empty")
        x_len = len(self._x_categories) if self._x_categories is not None else self._x_count
        if x_len is not None and len(coerced) != x_len:
            raise ValueError(
                f"y length {len(coerced)} does not match x-axis length {x_len}"
            )
        if self._series and len(coerced) != len(self._series[0][1]):
            raise ValueError(
                f"y length {len(coerced)} does not match "
                f"existing series length {len(self._series[0][1])}"
            )
        self._horizontal = horizontal
        self._series.append((series_type, coerced))
        return self

    def _render_x_axis(self) -> str | None:
        if self._x_categories is not None:
            parts = []
            if self._x_label is not None:
                parts.append(f'"{self._x_label}"')
            cats = [_format_category(c) for c in self._x_categories]
            parts.append(f"[{', '.join(cats)}]")
            return f"    x-axis {' '.join(parts)}"
        if self._x_label is not None or self._x_min is not None:
            parts = []
            if self._x_label is not None:
                parts.append(f'"{self._x_label}"')
            if self._x_min is not None:
                parts.append(f"{_format_number(self._x_min)} --> {_format_number(self._x_max)}")
            return f"    x-axis {' '.join(parts)}"
        return None

    def _render_y_axis(self) -> str | None:
        if self._y_label is None and self._y_min is None:
            return None
        parts = []
        if self._y_label is not None:
            parts.append(f'"{self._y_label}"')
        if self._y_min is not None:
            parts.append(f"{_format_number(self._y_min)} --> {_format_number(self._y_max)}")
        return f"    y-axis {' '.join(parts)}"

    def _validate_series_consistency(self) -> None:
        if not self._series:
            return
        expected = len(self._series[0][1])
        for i, (stype, data) in enumerate(self._series):
            if len(data) != expected:
                raise ValueError(
                    f"Series {i} ({stype}) has length {len(data)}, expected {expected}"
                )
        x_len = len(self._x_categories) if self._x_categories is not None else self._x_count
        if x_len is not None and x_len != expected:
            raise ValueError(
                f"x-axis has {x_len} points but series have {expected} values"
            )

    def render(self) -> str:
        self._validate_series_consistency()
        lines: list[str] = []

        header = "xychart-beta"
        if self._horizontal:
            header += " horizontal"
        lines.append(header)

        if self._title is not None:
            escaped = self._title.replace('"', '\\"')
            lines.append(f'    title "{escaped}"')

        x_line = self._render_x_axis()
        if x_line:
            lines.append(x_line)

        y_line = self._render_y_axis()
        if y_line:
            lines.append(y_line)

        for series_type, data in self._series:
            values = ", ".join(_format_number(v) for v in data)
            lines.append(f"    {series_type} [{values}]")

        return "\n".join(lines)

    def __str__(self) -> str:
        return f"```mermaid\n{self.render()}\n```"

    def save(self, path: str | Path) -> None:
        Path(path).write_text(str(self) + "\n", encoding="utf-8")
