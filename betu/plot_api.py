"""界面开关适配；仿真计算由 core_functions 原函数完成。"""

from functools import wraps
from inspect import signature, Parameter
from matplotlib.patches import Patch
from . import core_functions as core
from ._plotting import apply_legend
from ._default_setting import LEGEND_DEFAULTS


def adapt(function, default_legend=True):
    @wraps(function)
    def call(*args, show_legend=default_legend, **kwargs):
        regional = function.__name__ in ("draw_detail_area", "draw_max_area")
        smart_labels = kwargs.pop("smart_labels", True) if regional else False
        params = signature(function).parameters
        extra_legend = (
            kwargs.pop("legend_options", None)
            if "legend_options" not in params
            else None
        )
        if "isgrid" not in params:
            kwargs.pop("isgrid", None)
        bound = signature(function).bind(*args, **kwargs)
        values = bound.arguments
        legend = values.get("legend_options", extra_legend)
        if legend is None and "legend_options" in params:
            legend = params["legend_options"].default
        if not show_legend:
            legend = None
        # Use the core's geometry and numerical output; apply optional legends afterward.
        if "legend_options" in params:
            values["legend_options"] = None
        save_dir = values.get("save_dir")
        values["save_dir"] = None
        result = function(**values)
        if result is None:
            return result
        if show_legend:
            ax = result.gca()
            options = dict(legend or LEGEND_DEFAULTS)
            if options.get("loc") == "outside right center":
                options["loc"] = "outside right"
            if function.__name__ == "draw_lines":
                if len(ax.lines) == 1:
                    ax.lines[0].set_label(next(iter(values["expressions"])))
                apply_legend(ax, legend_options=options)
            elif function.__name__ == "draw_3D":
                colors = values.get("colors", params["colors"].default)
                handles = [
                    Patch(facecolor=colors[i % len(colors)], label=name)
                    for i, name in enumerate(values["expressions"])
                ]
                apply_legend(ax, legend_options=options, handles=handles)
            elif function.__name__ == "draw_detail_area":
                # Core-generated regional patches use the same ordering as its text labels.
                # Build the original legend handles without recomputing the numerical regions.
                handles = getattr(ax, "_betu_region_handles", [])
                apply_legend(ax, legend_options=options, handles=handles)
            else:
                colors = values.get("colors", params["colors"].default)
                patterns = values.get("patterns", params["patterns"].default)
                handles = [
                    Patch(
                        facecolor=colors[i % len(colors)],
                        hatch=patterns[i % len(patterns)],
                        label=label.get_text(),
                    )
                    for i, label in enumerate(ax.texts)
                ]
                apply_legend(ax, legend_options=options, handles=handles)
        if regional:
            from .region_labels import label_disconnected_regions

            manual_positions = values.get("pattern_moves", "auto") != "auto"
            label_disconnected_regions(
                result.gca(),
                smart=smart_labels,
                preserve_offsets=manual_positions,
            )
        if save_dir is not None:
            from .advanced import resolve_save_path

            result.savefig(
                resolve_save_path(save_dir),
                dpi=600,
                bbox_inches="tight",
                transparent=False,
            )
        return result

    parameters = list(signature(function).parameters.values())
    if "legend_options" not in signature(function).parameters:
        parameters.append(
            Parameter("legend_options", Parameter.KEYWORD_ONLY, default=None)
        )
    parameters.append(
        Parameter("show_legend", Parameter.KEYWORD_ONLY, default=default_legend)
    )
    if function.__name__ in ("draw_detail_area", "draw_max_area"):
        parameters.append(
            Parameter("smart_labels", Parameter.KEYWORD_ONLY, default=True)
        )
    call.__signature__ = signature(function).replace(parameters=parameters)
    return call


draw_lines = adapt(core.draw_lines)
draw_3D = adapt(core.draw_3D)
draw_max_area = adapt(core.draw_max_area, False)
draw_detail_area = adapt(core.draw_detail_area)
