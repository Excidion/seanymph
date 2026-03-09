from __future__ import annotations

import narwhals as nw

from seanymph.barplot import barplot
from seanymph.mermaidplotlib.xychart import XYChart


@nw.narwhalify
def countplot(
    data,
    *,
    x: str | None = None,
    y: str | None = None,
    hue: str | None = None,
    order: list | None = None,
    hue_order: list | None = None,
    color: str | None = None,
    palette=None,
) -> XYChart:
    if (x is None) == (y is None):
        raise ValueError("exactly one of x or y must be provided")

    cat_col = x if x is not None else y
    group_cols = [cat_col] + ([hue] if hue else [])

    order = order or list(dict.fromkeys(data[cat_col].to_list()))
    counts = data.lazy().group_by(group_cols).agg(nw.len().alias("__count__")).collect().to_native()

    bp_x, bp_y = (cat_col, "__count__") if x is not None else ("__count__", cat_col)
    return barplot(counts, x=bp_x, y=bp_y, hue=hue, order=order, hue_order=hue_order, color=color, palette=palette)
