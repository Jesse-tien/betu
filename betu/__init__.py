from .helpers import PACKAGE_DOC, make_example
from .plot_api import draw_lines, draw_3D, draw_max_area, draw_detail_area
from .data_plotting import data_lines
from .table import plot_table, read_table
from .advanced import plot_context, documents_dir, run_advanced, check_advanced_syntax
from ._plotting import apply_grid, apply_legend
from sympy import (
    symbols,
    Symbol,
    Abs,
    exp,
    oo,
    sqrt,
    root,
    log,
    ln,
    integrate,
    diff,
    limit,
    summation,
    product,
    sin,
    cos,
    tan,
    csc,
    sec,
    cot,
    sinh,
    cosh,
    tanh,
    coth,
    acos,
    acosh,
    acot,
    acoth,
    acsc,
    acsch,
    asec,
    asech,
    asin,
    asinh,
    atan,
    atan2,
    atanh,
    csch,
    cse,
    Mod,
    pi,
    sech,
    sinc,
    floor,
    ceiling,
    Piecewise,
    Rational,
    Number,
)
import numpy as np
from .helpers import SYMPY_NAMES

__doc__ = PACKAGE_DOC
__version__ = "1.0.1"


def makefig():
    from .main import makefig as launch

    return launch()


__all__ = SYMPY_NAMES + [
    "np",
    "data_lines",
    "draw_lines",
    "draw_3D",
    "draw_max_area",
    "draw_detail_area",
    "plot_table",
    "read_table",
    "plot_context",
    "documents_dir",
    "run_advanced",
    "check_advanced_syntax",
    "apply_grid",
    "apply_legend",
    "make_example",
    "makefig",
]
from .helpers import IMPORT_TIPS

print(IMPORT_TIPS)

# 缺少商业字体的平台使用可用字体回退。
from matplotlib import font_manager as _fm, rcParams as _rc

_fonts = {font.name for font in _fm.fontManager.ttflist}
_english = next(
    (name for name in ["Times New Roman", "Times", "DejaVu Serif"] if name in _fonts),
    "DejaVu Serif",
)
_chinese = next(
    (
        name
        for name in [
            "SimSun",
            "Songti SC",
            "STSong",
            "PingFang SC",
            "Noto Serif CJK SC",
        ]
        if name in _fonts
    ),
    "DejaVu Serif",
)
_rc["font.family"] = [_english, _chinese]
_rc["mathtext.rm"] = _english
_rc["mathtext.it"] = _english + ":italic"
_rc["mathtext.bf"] = _english + ":bold"
del _fm, _rc, _fonts, _english, _chinese
