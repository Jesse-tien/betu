import ast
import os
from pathlib import Path
import re

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import pytest
import sympy as sp
import matplotlib.pyplot as plt
from PyQt5 import QtCore as C, QtGui as G, QtWidgets as W
import betu
from betu import helpers as H
from betu.latex_input import convert_formula
from betu.formula import read_plot_code
from betu.main import create_application, MainWindow
from betu.style_editor import StyleDialog
from betu.qt_widgets import HelpBrowser


@pytest.mark.parametrize("source, mode, expected", [
    (r"\frac{\left(\alpha x+\lambda\right)^2}{8 \left(k+\sqrt{\frac{x}{2}}\right)^2}", 1,
     "(alpha*x+lamda)**2/(8*(k+sqrt(x/2))**2)"),
    (r"\frac{1}{\sqrt{a^{2}+b^{2}}}", 1, "1/sqrt(a**2+b**2)"),
    (r"\frac{\frac{a}{b}+\frac{c}{d}}{\frac{e}{f}}", 1, "(a/b+c/d)/(e/f)"),
    (r"\[\lambda^{x+2} + \alpha^{\frac{1}{2}}\]", 1, "lamda**(x+2)+sqrt(alpha)"),
    ("sqrt(sin(x).^2 + nthroot(y+sqrt(z),3));", 2, "sqrt(sin(x)**2+(y+sqrt(z))**(1/3))"),
    ("lambda.^2 .* x ./ ...\n nthroot(sqrt(y),2);", 2, "lamda**2*x/(sqrt(y))**(1/2)"),
    ("nthroot(sin(x)+cos(y),nthroot(z,2))", 2, "(sin(x)+cos(y))**(1/sqrt(z))"),
])
def test_source_specific_conversion_without_latex_parser(source, mode, expected, monkeypatch):
    import sympy.parsing.latex as latex

    def forbidden(*args, **kwargs):
        pytest.fail("Source-specific conversion must not call parse_latex")

    monkeypatch.setattr(latex, "parse_latex", forbidden)
    result = convert_formula(source, mode)
    assert "^" not in result and "lambda" not in result
    ast.parse(result, mode="eval")
    names = set(re.findall(r"\b[A-Za-z_]+\b", expected)) - {"sin", "cos", "sqrt"}
    namespace = {name: sp.Symbol(name, positive=True) for name in names}
    assert sp.simplify(sp.sympify(result, locals=namespace) - sp.sympify(expected, locals=namespace)) == 0


@pytest.mark.parametrize("source,expected", [
    (r"\lambda^2", "lamda**2"),
    (r"\sin(x)+\log(x)", "sin(x)+log(x)"),
    (r"a (x+1)", "a*(x+1)"),
    (r"\int_0^1 x^2 dx", "1/3"),
])
def test_general_latex_keeps_standard_functions(source, expected):
    result = convert_formula(source, 0)
    assert "^" not in result and "lambda" not in result
    namespace = dict(sp.__dict__)
    namespace["x"] = sp.Symbol("x")
    namespace["a"] = sp.Symbol("a")
    namespace["lamda"] = sp.Symbol("lamda")
    assert sp.simplify(sp.sympify(result, locals=namespace) - sp.sympify(expected)) == 0


@pytest.mark.parametrize("source,mode", [("$$", 1), (r"\frac{x}", 1),
    (r"\sqrt{x", 1), ("sqrt(x", 2), ("nthroot(x)", 2), ("nthroot(x,2,3)", 2)])
def test_invalid_conversion_reports_an_error(source, mode):
    with pytest.raises((ValueError, SyntaxError)):
        convert_formula(source, mode)


@pytest.fixture
def window():
    app = create_application()
    window = MainWindow()
    yield window
    window.close()
    app.processEvents()
    plt.close("all")
    H.set_language("zh")


def test_blank_labels_and_partial_overrides_roundtrip(window):
    function = "draw_max_area"
    parameters = H.default_parameters(function)
    dialog = StyleDialog(window, parameters, ["区域 1", "区域 2", "区域 3"], function)
    entry = dialog.series_fields["texts"]
    assert entry.text() == ""
    assert entry.placeholderText() == "该值为空，则默认用表达式名标注"
    dialog.commit_series()
    assert dialog.values["texts"] is None
    entry.setText("自定义区域")
    dialog.selector.setCurrentIndex(1)
    assert entry.text() == ""
    assert dialog.values["texts"] == ["自定义区域", None, None]
    dialog.selector.setCurrentIndex(0)
    assert entry.text() == "自定义区域"
    entry.clear()
    dialog.commit_series()
    assert dialog.values["texts"] is None
    formula = "A = x\nB = y"
    parameters.update(assigns={}, the_var_x="x", the_var_y="y", start_end_x=[0, 1], start_end_y=[0, 1])
    for labels in (None, [None, "自定义区域"]):
        parameters["texts"] = labels
        code = H.build_code(function, formula, parameters)
        assert read_plot_code(code)[2]["texts"] == labels
    dialog.close()


def test_expression_names_are_used_for_blank_region_labels():
    function = "draw_max_area"
    x, y = sp.symbols("x y")
    fn = getattr(betu, function)
    args = ({"$A$": x, "$B$": y}, {}, x, [0, 1], y, [0, 1])
    fn(*args, precision=50, smart_labels=False, dropout=0.03)
    automatic = [label.get_text() for label, *_ in plt.gca()._betu_regions]
    assert all("Region" not in label for label in automatic)
    assert set(automatic) == {"$A$", "$B$"}
    fn(*args, precision=50, smart_labels=False, dropout=0.03, texts=["Custom", ""])
    changed = [label.get_text() for label, *_ in plt.gca()._betu_regions]
    assert "Custom" in changed
    assert automatic[1] in changed
    plt.close("all")


@pytest.mark.parametrize("prefix,numbers,expected", [
    ("Region", "roman", ["Region I", "Region II"]),
    ("Region", "letter", ["Region A", "Region B"]),
    ("区域", "number", ["区域 1", "区域 2"]),
    ("", "letter", ["A", "B"]),
])
def test_relationship_prefix_and_numbering(window, prefix, numbers, expected):
    import inspect

    assert "texts" not in inspect.signature(betu.draw_detail_area).parameters
    page = window.pages[2]
    page.load_example(confirm=False)
    values = dict(page.parameters, texts=["old label"])
    dialog = StyleDialog(page, values, ["区域 1", "区域 2"], page.function)
    assert "texts" not in dialog.values
    assert "texts" not in dialog.series_fields
    dialog.common_fields["prefix"].field.setText(prefix)
    number_field = dialog.common_fields["numbers"].field
    number_field.setCurrentIndex(number_field.findData(numbers))
    dialog.save()
    assert dialog.result() == W.QDialog.Accepted
    assert dialog.values["prefix"] == prefix
    assert dialog.values["numbers"] == numbers
    page.parameters.update(dialog.values)
    code = page.compile_code()
    assert "texts =" not in code and "texts=texts" not in code
    page.restore_code(code)
    assert page.parameters["prefix"] == prefix
    assert page.parameters["numbers"] == numbers

    x, y = sp.symbols("x y")
    betu.draw_detail_area({"$A$": x, "$B$": y}, {}, x, [0, 1], y, [0, 1],
                          prefix=prefix, numbers=numbers, precision=50, dropout=0.03,
                          smart_labels=False)
    ax = plt.gca()
    assert [text.get_text() for text, *_ in ax._betu_regions] == expected
    legend_texts = [text.get_text() for text in ax.get_legend().get_texts()]
    assert legend_texts == [expected[0] + ": $A>B$", expected[1] + ": $B>A$"]
    plt.close("all")
    dialog.close()


def test_hatch_icons_include_matplotlib_patterns(window):
    parameters = H.default_parameters("draw_max_area")
    dialog = StyleDialog(window, parameters, ["区域 1", "区域 2"], "draw_max_area")
    combo = dialog.series_fields["patterns"]
    for _, code in H.STYLE_PATTERN_CHOICES:
        assert combo.findData(code) >= 0
    images = [combo.itemIcon(i).pixmap(56, 26).toImage() for i in range(combo.count())]
    assert all(not image.isNull() for image in images)
    assert images[combo.findData("/")] != images[combo.findData("|")]
    combo.setCurrentIndex(combo.findData("x"))
    dialog.commit_series()
    assert dialog.values["patterns"][0] == "x"
    dialog.close()


def test_both_help_languages_load_all_images(window):
    browser = HelpBrowser()
    for language, html in zip(("zh", "en"), H.HELP_HTML):
        H.set_language(language)
        browser.set_help(html)
        for source in re.findall(r'src="(help/[^\"]+)"', html):
            image = browser.document().resource(G.QTextDocument.ImageResource, C.QUrl(source))
            assert isinstance(image, G.QImage) and not image.isNull(), source
        assert "Edit code" not in browser.toPlainText()
    browser.close()


def test_readme_bilingual_images_and_version():
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    cn, en = readme.split('# Simple Scientific Simulation', 1)
    def images(text):
        return re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src="([^"]+)"', text)
    assert len(images(cn)) == len(images(en))
    for match in images(readme):
        assert (root / (match[0] or match[1])).is_file()
    assert not re.search(r"^!docs/", en, re.M)
    assert "LaTeX Conversion" not in en and "Edit Code" not in en
    assert betu.__version__ == "1.0.1"
    assert 'version = "1.0.1"' in (root / "pyproject.toml").read_text(encoding="utf-8")
