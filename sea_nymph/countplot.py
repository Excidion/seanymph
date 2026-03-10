from __future__ import annotations

import narwhals as nw
import narwhals.typing as nwt

from sea_nymph.barplot import barplot
from sea_nymph.mermaidplotlib.xychart import XYChart


@nw.narwhalify
def countplot(
    data: nwt.IntoFrame,
    *,
    x: str | None = None,
    y: str | None = None,
    hue: str | None = None,
    order: list | None = None,
    hue_order: list | None = None,
    stat: str = "count",
    color: str | None = None,
    palette: list | None = None,
) -> XYChart:
    """Plot counts (or proportions) of a categorical variable.

    Args:
        data: Input data. Any narwhals-compatible DataFrame or LazyFrame.
        x: Column name for horizontal categories (mutually exclusive with `y`).
        y: Column name for vertical categories (mutually exclusive with `x`).
        hue: Column name for grouping into separate series.
        order: Explicit category order.
        hue_order: Explicit order for hue levels.
        stat: Statistic to compute. One of `"count"`, `"percent"`,
            `"proportion"`, `"probability"`.
        color: Single colour for all bars (CSS colour string).
        palette: List of colours, one per hue level.

    Returns:
        XYChart: An instance ready to render or further configure.

    Raises:
        ValueError: If neither or both of `x`/`y` are provided, or `stat` is invalid.
    """
    if (x is None) == (y is None):
        raise ValueError("exactly one of x or y must be provided")
    if stat not in ("count", "percent", "proportion", "probability"):
        raise ValueError(
            f"stat must be 'count', 'percent', 'proportion', or 'probability', got {stat!r}"
        )

    cat_col = x if x is not None else y
    group_cols = [cat_col] + ([hue] if hue else [])

    order = order or data[cat_col].unique(maintain_order=True).to_list()
    hue_order = hue_order or (
        data[hue].unique(maintain_order=True).to_list() if hue else None
    )
    counts = data.lazy().group_by(group_cols).agg(nw.len().alias("__count__")).collect()

    if stat != "count":
        n = counts["__count__"].sum()
        factor = 100 / n if stat == "percent" else 1 / n
        counts = counts.with_columns((nw.col("__count__") * factor).alias("__count__"))

    stat_label = stat.capitalize()
    bp_x, bp_y = (cat_col, "__count__") if x is not None else ("__count__", cat_col)
    chart = barplot(
        counts,
        x=bp_x,
        y=bp_y,
        hue=hue,
        order=order,
        hue_order=hue_order,
        color=color,
        palette=palette,
    )
    return chart.ylabel(stat_label) if x is not None else chart.xlabel(stat_label)
