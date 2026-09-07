"""Generate the compact marker reference used in the README."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from betu import helpers as H


def main():
    markers = ["o", "s", "*", "P", "X", "D", "v", None]
    fig, ax = plt.subplots(figsize=(9, 1.25))
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.04, top=0.97)
    ax.set_axis_off()
    for index, marker in enumerate(markers):
        x = (index + 0.5) / len(markers)
        ax.plot(
            [x - 0.025, x + 0.025],
            [0.74, 0.74],
            color="#175b88",
            linewidth=1,
            transform=ax.transAxes,
        )
        if marker:
            ax.plot(
                x,
                0.74,
                marker=marker,
                markersize=10,
                color="#175b88",
                transform=ax.transAxes,
            )
        ax.text(
            x,
            0.40,
            repr(marker),
            ha="center",
            va="center",
            fontsize=11,
            transform=ax.transAxes,
        )
        ax.text(
            x,
            0.10,
            H.MARKER_NAMES[marker][0],
            ha="center",
            va="center",
            fontsize=10,
            transform=ax.transAxes,
        )
    fig.savefig(
        Path(__file__).parent / "screenshots" / "markers.png",
        dpi=180,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
