# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Read the saved rainfall data and draw daily rainfall for 2025."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
DATA = HERE / "data" / "daily_HKO_RF_2025.csv"
OUT = HERE / "out" / "rainfall-2025.png"


def rainfall_amount(text):
    """Convert a rainfall entry to millimetres, or None if it is unavailable."""
    if text == "***":
        return None
    if text == "Trace":
        return 0.0  # Less than 0.05 mm; too small to show at this chart's scale
    return float(text)


def main():
    days = []
    amounts = []
    month_positions = []
    month_labels = []

    with DATA.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            # The file has title lines above the data and notes below it.
            if len(row) != 5 or not row[0].isdigit():
                continue

            year, month, day, value, quality = row
            amount = rainfall_amount(value)

            if amount is None or quality != "C":
                continue

            if day == "1":
                month_positions.append(len(days))
                month_labels.append(int(month))

            days.append(f"{year}-{int(month):02d}-{int(day):02d}")
            amounts.append(amount)

    highest = max(amounts)
    highest_index = amounts.index(highest)
    print(f"Read {len(days)} days. Highest: {days[highest_index]}, {highest} mm")

    colours = ["#527a96"] * len(amounts)
    colours[highest_index] = "#d65a31"

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(range(len(amounts)), amounts, width=1.0, color=colours)
    ax.set_xticks(month_positions, month_labels)
    ax.set_xlabel("Month of 2025")
    ax.set_ylabel("Daily total rainfall (mm)")
    ax.set_title("Daily rainfall at the Hong Kong Observatory in 2025")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    ax.annotate(
        f"Highest day: {days[highest_index]}\n{highest:.1f} mm",
        xy=(highest_index, highest),
        xytext=(highest_index - 65, highest * 0.75),
        arrowprops={"arrowstyle": "->", "color": "#d65a31"},
        color="#a63f24",
    )

    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=160)
    print(f"Saved {OUT}")
    plt.show()

if __name__ == "__main__":
    main()