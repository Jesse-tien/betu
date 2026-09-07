from .helpers import tr
from ._default_setting import *

"Shared publication plotting defaults and legend handling."
import math
import numpy as np
from itertools import cycle, islice
import matplotlib.colors as mcolors
from matplotlib.transforms import blended_transform_factory


def fill_text_color(color, background="white"):
    """Choose black or white text with the higher contrast against a fill.

    Composite transparent colors onto the plot background before measuring
    relative luminance; use white behind a transparent figure background.
    """
    fill = mcolors.to_rgba(color)
    bg = mcolors.to_rgba(background)
    rgb = [
        fill[i] * fill[3] + (bg[i] * bg[3] + 1 - bg[3]) * (1 - fill[3])
        for i in range(3)
    ]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    luminance = sum((v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722))))
    black_contrast = (luminance + 0.05) / 0.05
    white_contrast = 1.05 / (luminance + 0.05)
    return "white" if white_contrast > black_contrast else "black"


def series_values(value, count, default, *, kind=None):
    """Accept a scalar or cycle a nonempty sequence without mutating it."""
    if value is None and kind != "marker":
        value = default
    if isinstance(value, str) or value is None:
        values = [value]
    elif kind == "color" and mcolors.is_color_like(value):
        values = [value]
    elif (
        kind == "linestyle"
        and isinstance(value, tuple)
        and (len(value) == 2)
        and (isinstance(value[0], (int, float)) and isinstance(value[1], (tuple, list)))
    ):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]
    if not values:
        raise ValueError(tr("message_37"))
    if kind == "marker":
        values = ["v" if v == "V" else None if v == "None" else v for v in values]
    return list(islice(cycle(values), count))


def line_styles(count, linestyles, linewidth, markers, markersize, colors):
    return zip(
        series_values(linestyles, count, DEFAULT_LINESTYLES, kind="linestyle"),
        series_values(linewidth, count, DEFAULT_LINEWIDTHS),
        series_values(markers, count, DEFAULT_MARKERS, kind="marker"),
        series_values(markersize, count, DEFAULT_MARKERSIZES),
        series_values(colors, count, DEFAULT_COLORS, kind="color"),
    )


def apply_grid(ax, isgrid=True):
    """Use the same soft dashed grid for 2D axes and 3D axis planes."""
    if getattr(ax, "name", "") == "3d":
        ax.grid(isgrid)
        if isgrid:
            for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
                axis._axinfo["grid"].update(
                    linestyle="--", color=mcolors.to_rgba("lightgray", 0.3)
                )
    elif isgrid:
        ax.grid(visible=True, linestyle="--", alpha=0.3, color="lightgray", axis="both")
    else:
        ax.grid(visible=False, axis="both")


def validate_legend(options):
    result = dict(options)
    loc = result.get("loc", "best")
    if loc not in MPL_LOCATIONS and loc not in LOCATIONS and (loc not in range(11)):
        raise ValueError(tr("message_38"))
    result["loc"] = loc
    for key in (
        "ncol",
        "fontsize",
        "borderpad",
        "labelspacing",
        "handlelength",
        "handletextpad",
        "columnspacing",
    ):
        if key not in result:
            continue
        value = float(result[key])
        if (
            not math.isfinite(value)
            or value < 0
            or (key in ("ncol", "fontsize") and value == 0)
        ):
            raise ValueError(tr("message_39", v0=key))
        if key == "ncol":
            if not value.is_integer():
                raise ValueError(tr("message_40"))
            value = int(value)
        result[key] = value
    return result


def apply_legend(
    ax,
    location="best",
    ncol=1,
    fsize=14,
    legendsize="auto",
    legend_options=None,
    handles=None,
    **kwargs,
):
    """Apply to an existing axes; retain explicit region/surface legend handles."""
    if legend_options is False:
        return None
    options = dict(
        loc=location, ncol=ncol, fontsize=fsize if legendsize == "auto" else legendsize
    )
    options.update(legend_options or {})
    options.update(kwargs)
    options = validate_legend(options)
    if options["loc"] in ("best", 0) and "bbox_to_anchor" not in options:
        options["loc"] = getattr(ax, "_betu_default_legend_location", options["loc"])
    outside = options["loc"] in ("图外右侧", "outside right")
    if outside:
        options.update(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            borderaxespad=0,
            bbox_transform=blended_transform_factory(
                ax.transAxes, ax.figure.transFigure
            ),
        )
    options["loc"] = LOCATIONS.get(options["loc"], options["loc"])
    if getattr(ax, "name", "") == "3d" and options["loc"] in ("best", 0):
        options["loc"] = "upper right"
    if handles is not None:
        ax._betu_legend_handles = list(handles)
    handles = getattr(ax, "_betu_legend_handles", None)
    if handles is None:
        handles, _ = ax.get_legend_handles_labels()
    if handles:
        legend = ax.legend(handles=handles, **options)
        legend._betu_outside_right = outside
        if outside:
            layout_figure(ax.figure)
        return legend
    return None


def complete_3d_bounds(ax):
    """Include 3D axis names in layout and tightly cropped exports."""
    from matplotlib.transforms import Bbox

    original = ax.get_tightbbox

    def tightbbox(renderer=None, *args, **kwargs):
        box = original(renderer, *args, **kwargs)
        boxes = [box] if box is not None else []
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            label = axis.label
            if label.get_visible() and label.get_text() and label.get_in_layout():
                boxes.append(label.get_window_extent(renderer))
        return Bbox.union(boxes) if boxes else None

    ax.get_tightbbox = tightbbox


def distinguish_tick_labels(axis):
    """Increase decimal precision only when distinct ticks round to the same text."""
    from matplotlib.ticker import FormatStrFormatter

    ticks = np.unique(axis.get_majorticklocs())
    labels = axis.get_major_formatter().format_ticks(ticks)
    if len(set(labels)) == len(ticks):
        return
    for decimals in range(16):
        formatter = FormatStrFormatter(f"%.{decimals}f")
        if len(set(formatter.format_ticks(ticks))) == len(ticks):
            axis.set_major_formatter(formatter)
            return


def layout_figure(figure, pad=1.08):
    from matplotlib.layout_engine import PlaceHolderLayoutEngine

    if isinstance(figure.get_layout_engine(), PlaceHolderLayoutEngine):
        figure.set_layout_engine(None)
    for ax in figure.axes:
        for annotation in getattr(ax, "_betu_callouts", []):
            if getattr(annotation, "_betu_external", False):
                annotation.set_in_layout(False)
    _layout_base(figure, pad)
    from .region_labels import position_callouts

    position_callouts(figure)


def _layout_base(figure, pad=1.08):
    """Reserve a separate right column for legends, including during title layout.

    Keep the requested plot width and extend the canvas for long legend text.
    Temporarily exclude the legends from tight_layout, but include them again
    for bbox_inches='tight' exports. Repeated calls do not accumulate width.
    """
    legends = [
        ax.get_legend()
        for ax in figure.axes
        if ax.get_legend() is not None
        and getattr(ax.get_legend(), "_betu_outside_right", False)
    ]
    if not legends:
        figure.tight_layout(pad=pad)
        return
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    boxes = [legend.get_window_extent(renderer) for legend in legends]
    reserve = max((box.width for box in boxes)) / figure.dpi + 0.35
    width, height = figure.get_size_inches()
    base_width = getattr(figure, "_betu_plot_width", width)
    figure._betu_plot_width = base_width
    width = max(width, base_width + reserve)
    height = max(height, max((box.height for box in boxes)) / figure.dpi + 0.5)
    figure.set_size_inches(width, height, forward=True)
    for legend in legends:
        legend.set_in_layout(False)
    try:
        figure.tight_layout(pad=pad, rect=(0, 0, (width - reserve) / width, 1))
    finally:
        for legend in legends:
            legend.set_in_layout(True)
