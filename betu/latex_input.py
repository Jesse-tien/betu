"""按来源转换表达式；只有通用 LaTeX 使用 SymPy 的 LaTeX 解析器。"""

import ast
import re
from .formula import normalize
from . import helpers as H


def _matching(text, start, opening="(", closing=")"):
    depth = 1
    for i in range(start + 1, len(text)):
        if text[i] == opening:
            depth += 1
        elif text[i] == closing:
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(H.tr("conversion_brackets"))


def replace_frac_sqrt(expr):
    """递归处理分式和平方根，按成对花括号读取嵌套内容。"""
    pattern = re.compile(r"\\(frac|sqrt)\s*\{")
    while True:
        match = pattern.search(expr)
        if match is None:
            return expr
        start = match.end() - 1
        end = _matching(expr, start, "{", "}")
        inner = replace_frac_sqrt(expr[start + 1:end])
        if match.group(1) == "frac":
            second = end + 1
            while second < len(expr) and expr[second].isspace():
                second += 1
            if second >= len(expr) or expr[second] != "{":
                raise ValueError(H.tr("conversion_fraction"))
            end = _matching(expr, second, "{", "}")
            denominator = replace_frac_sqrt(expr[second + 1:end])
            replacement = f"({inner})/({denominator})"
        else:
            replacement = f"({inner})^(1/2)"
        expr = expr[:match.start()] + replacement + expr[end + 1:]


def mathematica_latex(latex_str):
    cleaned_expr = latex_str.replace(r"\left", "").replace(r"\right", "")
    cleaned_expr = re.sub(r"\s+", " ", cleaned_expr).strip()
    cleaned_expr = replace_frac_sqrt(cleaned_expr)
    # 复合指数必须保留括号，避免 a^{b+c} 被误写成 a**b+c。
    while re.search(r"\^\s*\{", cleaned_expr):
        match = re.search(r"\^\s*\{", cleaned_expr)
        start = match.end() - 1
        end = _matching(cleaned_expr, start, "{", "}")
        cleaned_expr = cleaned_expr[:match.start()] + "^(" + cleaned_expr[start + 1:end] + ")" + cleaned_expr[end + 1:]
    cleaned_expr = cleaned_expr.replace("\\", "").replace("{", "").replace("}", "")
    for operator in "+-^/":
        cleaned_expr = cleaned_expr.replace(operator + " ", operator).replace(" " + operator, operator)
    cleaned_expr = cleaned_expr.replace(" ", "*")
    return cleaned_expr.replace("*)", ")")


def replace_sqrt_nthroot(expr):
    def find_top_level_comma(s):
        depth = 0
        for i, char in enumerate(s):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                return i
        return -1

    def process(text):
        i = 0
        while i < len(text):
            boundary = i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")
            if boundary and text.startswith("sqrt(", i):
                start = i + 5
                end = _matching(text, start - 1)
                inner = process(text[start:end])
                replacement = f"({inner})^(1/2)"
            elif boundary and text.startswith("nthroot(", i):
                start = i + 8
                end = _matching(text, start - 1)
                args = text[start:end]
                comma = find_top_level_comma(args)
                if comma < 0 or not args[:comma] or not args[comma + 1:] or find_top_level_comma(args[comma + 1:]) >= 0:
                    raise ValueError(H.tr("conversion_nthroot"))
                base = process(args[:comma].strip())
                root = process(args[comma + 1:].strip())
                replacement = f"({base})^(1/({root}))"
            else:
                i += 1
                continue
            text = text[:i] + replacement + text[end + 1:]
            i += len(replacement)
        return text

    return process(expr)


def matlab_sp(latex_str):
    cleaned_expr = latex_str.replace(".*", "*").replace("./", "/").replace(".^", "^")
    cleaned_expr = re.sub(r"\s+", "", cleaned_expr.replace("...", ""))
    cleaned_expr = cleaned_expr.replace(";", "")
    return replace_sqrt_nthroot(cleaned_expr)


def convert_formula(text, mode=0):
    source = text.strip()
    for delimiter in (r"\[", r"\]", r"\(", r"\)", "$"):
        source = source.replace(delimiter, "")
    if not source.strip():
        raise ValueError(H.tr("conversion_empty"))
    if mode == 1:
        cleaned_expr = mathematica_latex(source)
    elif mode == 2:
        cleaned_expr = matlab_sp(source)
    elif mode == 0:
        from sympy.parsing.latex import parse_latex

        source = source.replace("{}", "").replace("{ }", "")
        greek = "|".join(sorted(H.GREEK_NAMES, key=len, reverse=True))
        source = re.sub(r"\\(?:" + greek + r")(?![A-Za-z])", lambda m: "{" + m.group(0) + "}", source)
        cleaned_expr = str(parse_latex(source)).replace("{", "").replace("}", "")
        # 保留标准函数；把解析器生成的未知函数 a(x) 还原为 a*(x)。
        def function_call(match):
            name = match.group(1)
            if name in H.CONVERSION_FUNCTION_ALIASES:
                return H.CONVERSION_FUNCTION_ALIASES[name] + "("
            return match.group(0) if name in H.SYMPY_NAMES else name + "*("

        cleaned_expr = re.sub(r"\b([A-Za-z_][A-Za-z_0-9]*)\(", function_call, cleaned_expr)
    else:
        raise ValueError(H.tr("conversion_mode"))
    cleaned_expr = cleaned_expr.replace('lambda', 'lamda')
    cleaned_expr = normalize(cleaned_expr)
    ast.parse(cleaned_expr, mode="eval")
    return cleaned_expr
