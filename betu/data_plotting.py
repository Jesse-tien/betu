from .helpers import tr

"""数值仿真与论文绘图核心；不依赖图形界面。"""
from sympy import *
from itertools import permutations, product
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
from matplotlib import rcParams
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import copy
import string
import re
import platform
from ._default_setting import *
from ._plotting import (
    apply_grid,
    apply_legend,
    layout_figure,
    line_styles,
    series_values,
)


def set_font(label):
    from matplotlib import font_manager

    available = {font.name for font in font_manager.fontManager.ttflist}
    choices = (
        [
            "SimSun",
            "Songti SC",
            "STSong",
            "PingFang SC",
            "Noto Serif CJK SC",
            "DejaVu Serif",
        ]
        if re.search(r"[一-鿿]", label)
        else ["Times New Roman", "Times", "DejaVu Serif"]
    )
    return next(name for name in choices if name in available)


def data_lines(
    data,
    label_x=None,
    x_name="$x$",
    y_name="$y$",
    save_dir=None,
    location="best",
    ncol=1,
    fsize=14,
    figsize=[6, 5],
    xt_rotation=0,
    xrotation=0,
    yrotation=0,
    linestyles=None,
    linewidth=DEFAULT_LINEWIDTHS,
    markers=DEFAULT_MARKERS,
    markersize=DEFAULT_MARKERSIZES,
    colors=DEFAULT_COLORS,
    isgrid=True,
    xpad=3,
    ypad=3,
    xlabelpad=10,
    ylabelpad=10,
    xlabelsize="auto",
    ylabelsize="auto",
    legendsize="auto",
    legend_options=None,
    show_legend=True,
):
    if not show_legend:
        legend_options = False
    if not data or any((len(values) == 0 for values in data.values())):
        raise ValueError(tr("message_1"))
    max_len = max((len(values) for values in data.values()))
    labels = list(label_x) if label_x is not None else list(range(1, max_len + 1))
    labels += list(range(len(labels) + 1, max_len + 1))
    fig, ax = plt.subplots(figsize=figsize)
    styles = line_styles(len(data), linestyles, linewidth, markers, markersize, colors)
    for (name, values), (ls, lw, marker, ms, color) in zip(data.items(), styles):
        values = np.asarray(values, dtype=float)
        if not np.isfinite(values).any():
            plt.close(fig)
            raise ValueError(tr("message_2", v0=name))
        ax.plot(
            np.arange(1, len(values) + 1),
            values,
            label=name,
            linestyle=ls,
            linewidth=lw,
            marker=marker,
            markersize=ms,
            color=color,
            markevery=max(1, len(values) // 10),
        )
    step = max(1, max_len // 10)
    ax.set_xticks(np.arange(1, max_len + 1, step))
    ax.set_xticklabels([str(v) for v in labels[:max_len:step]])
    if max_len > 1:
        ax.set_xlim(1, max_len)
    if y_name is None:
        y_name = next(iter(data)) if len(data) == 1 else "$y$"
    ax.set_xlabel(
        x_name,
        fontsize=fsize if xlabelsize == "auto" else xlabelsize,
        rotation=xrotation,
        labelpad=xlabelpad,
    )
    ax.set_ylabel(
        y_name,
        fontsize=fsize if ylabelsize == "auto" else ylabelsize,
        rotation=yrotation,
        labelpad=ylabelpad,
    )
    ax.tick_params(
        axis="x", direction="in", pad=xpad, labelsize=fsize, labelrotation=xt_rotation
    )
    ax.tick_params(axis="y", direction="in", pad=ypad, labelsize=fsize)
    apply_legend(ax, location, ncol, fsize, legendsize, legend_options)
    apply_grid(ax, isgrid)
    fig.tight_layout()
    if save_dir is not None:
        fig.savefig(save_dir, dpi=300, bbox_inches="tight")
    return plt
