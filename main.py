from pathlib import Path

from seanymph import Figure

EXAMPLES_DIR = Path("docs/examples")


def main():
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    months = ["Jan", "Feb", "Mar", "Apr"]

    (
        Figure(title="Sales 2024")
        .bar(months, [10, 40, 30, 50])
        .line(months, [15, 35, 25, 45])
        .xlabel("Month")
        .ylabel("Revenue (k)")
        .ylim(0, 60)
    ).save(EXAMPLES_DIR / "sales_2024.md")

    (
        Figure(title="Q1 Breakdown")
        .barh(["Product A", "Product B", "Product C"], [120, 85, 200])
        .ylabel("Units")
    ).save(EXAMPLES_DIR / "q1_breakdown.md")


if __name__ == "__main__":
    main()
