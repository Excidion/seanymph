from __future__ import annotations

import narwhals as nw
import narwhals.typing as nwt

from sea_nymph._utils import resolve_palette
from sea_nymph.mermaidplotlib.xychart import XYChart


@nw.narwhalify
def lineplot(
    data: nwt.IntoFrame,
    *,
    x: str,
    y: str,
    hue: str | None = None,
    hue_order: list | None = None,
    estimator: nw.Expr | None = None,
    color: str | None = None,
    palette: list | None = None,
) -> XYChart:
    """Plot a line chart with optional aggregation.

    Accepts any DataFrame supported by narwhals. Numeric x values must be evenly
    spaced — Mermaid places all points equidistantly regardless of actual values.

    Args:
        data: Input data. Any narwhals-compatible DataFrame or LazyFrame.
        x: Column name for the x-axis.
        y: Column name for the y-axis.
        hue: Column name for grouping into separate series.
        hue_order: Explicit order for hue levels.
        estimator: Aggregation expression (narwhals Expr). Defaults to mean.
        color: Single colour for the line (CSS colour string).
        palette: List of colours, one per hue level.

    Returns:
        XYChart: An instance ready to render or further configure.

    Raises:
        ValueError: If a required column is missing or numeric x values are not
            evenly spaced.
    """
    for col in [x, y] + ([hue] if hue else []):
        if col not in data.columns:
            raise ValueError(f"Column {col!r} not found in data")

    agg_expr = estimator if estimator is not None else nw.col(y).mean()
    group_cols = [x, hue] if hue else [x]
    numeric_x = data.schema[x].is_numeric()

    if numeric_x:
        result = data.lazy().group_by(group_cols).agg(agg_expr).sort(x).collect()
        xs = result[x].unique(maintain_order=True).to_list()
    else:
        result = data.lazy().group_by(group_cols).agg(agg_expr).collect()
        xs = data[x].unique(maintain_order=True).to_list()

    levels = hue_order or (
        data[hue].unique(maintain_order=True).to_list() if hue else [None]
    )
    colors = resolve_palette(palette, levels, color)

    chart = XYChart()
    for level, c in zip(levels, colors):
        sub = result.filter(nw.col(hue) == level) if level is not None else result
        lookup = dict(zip(sub[x].to_list(), sub[y].to_list()))
        chart.line(xs, [lookup[xi] for xi in xs], color=c)

    return chart
