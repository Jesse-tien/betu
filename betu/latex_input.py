"""LaTeX 与 Matlab 公式输入规范化。"""

import re
from .formula import normalize


def convert_formula(text, mode=0):
    if mode == 2:
        result = (
            text.strip()
            .rstrip(";")
            .replace(".*", "*")
            .replace("./", "/")
            .replace(".^", "**")
        )
        return normalize(result)
    from sympy.parsing.latex import parse_latex

    source = (
        text.strip()
        .replace("\\[", "")
        .replace("\\]", "")
        .replace("\\(", "")
        .replace("\\)", "")
        .replace("$", "")
    )
    # Mathematica 的字体包装不改变变量含义。
    source = re.sub(r"\\(?:text|mathrm|operatorname)\{([^{}]+)\}", r"\1", source)
    result = str(parse_latex(source)).replace("{", "").replace("}", "")
    return normalize(result)
