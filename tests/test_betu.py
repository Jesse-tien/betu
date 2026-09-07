import ast
import inspect
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
import betu
from betu import helpers as H
from betu.formula import parse_formulas, read_plot_code


@pytest.fixture(autouse=True)
def plots(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")
    H.set_language("zh")


def test_forward_integral_and_functions():
    text = "Area = integrate(p*t+b-3*t**2, (t,p-c,p+a*b))\np := 2*a+b-c**3/2"
    plan = parse_formulas(text)
    assert plan.symbols == ["a", "b", "c", "t"]
    scope = {}
    exec("from betu import *\n" + plan.source(), scope)
    assert scope["expressions"]["Area"].free_symbols <= {
        scope["a"],
        scope["b"],
        scope["c"],
    }
    assert "p" not in plan.symbols and "Area" not in plan.symbols


def test_reassignment_and_indexing_roundtrip():
    text = "Final = value\nvalue := pairs[1][0]\npairs := cse([x**2 + 2*x])\nvalue := value + 1"
    plan = parse_formulas(text)
    assert plan.symbols == ["x"]
    parameters = H.default_parameters("draw_lines")
    parameters.update(assigns={}, the_var="x", ranges=[0, 2, 0.1])
    code = H.build_code("draw_lines", text, parameters, 'the_plt.title("Sample")')
    fn, restored, settings, advanced = read_plot_code(code)
    assert parse_formulas(restored).intermediates == plan.intermediates
    assert "the_plt.title" in advanced
    exec(code, {})


@pytest.mark.parametrize(
    "text",
    [
        "p := q+1\nq := p+1\nA = p",
        "p := p+1\nA = p",
        "9a := x\nA = x",
        "integrate := x\nA = x",
        "A = x\nB = A+x",
    ],
)
def test_invalid_formulas(text):
    with pytest.raises(ValueError):
        parse_formulas(text)


@pytest.mark.parametrize(
    "name", list(H.PLOT_FUNCTIONS) + ["data_" + key for key in H.CHART_LABELS]
)
def test_full_examples_run_and_restore(name):
    code = H.example_code(name)
    assert code.startswith("from betu import *")
    assert "**style" not in code and "_betu_options" not in code
    ast.parse(code, feature_version=(3, 8))
    namespace = {}
    exec(code, namespace)
    fig = plt.gcf()
    fig.canvas.draw()
    if name in H.TAB_FUNCTIONS or name.startswith("data_") and name != "data_lines":
        fn, formula, params, advanced = read_plot_code(code)
        assert params["show_legend"] == (name != "draw_max_area")
    if name in ("draw_max_area", "draw_detail_area", "draw_3D"):
        assert not any(g.get_visible() for g in fig.axes[0].get_xgridlines())


@pytest.mark.parametrize(
    "fn", [betu.draw_lines, betu.draw_max_area, betu.draw_detail_area, betu.draw_3D]
)
@pytest.mark.parametrize("visible", [False, True])
def test_legend_switches(fn, visible):
    x, y = betu.symbols("x y")
    exp = {"A": x + y, "B": 2 * x - y, "C": 2 - x}
    if fn == betu.draw_lines:
        fn(exp, {y: 1}, x, [0, 2, 0.1], show_legend=visible)
    else:
        fn(exp, {}, x, [0, 2], y, [0, 2], precision=15, show_legend=visible)
    assert (plt.gca().get_legend() is not None) == visible


@pytest.mark.parametrize("kind", list(H.CHART_LABELS))
def test_data_no_legend(kind):
    sample = H.table_example(kind)
    betu.plot_table(**sample, show_legend=False)
    assert plt.gca().get_legend() is None


def test_public_symbols_and_api():
    for name in H.SYMPY_NAMES:
        assert name in betu.__all__ and hasattr(betu, name)
    assert len(inspect.signature(betu.make_example).parameters) == 1
    for name in ("mathshow", "showlatex", "mathprint", "latex", "save_var", "get_var"):
        assert not hasattr(betu, name)
    assert "InlineBackend.figure_format = 'retina'" in H.IMPORT_TIPS


def test_qt_roundtrip_and_language():
    from betu.main import create_application, MainWindow
    from betu.qt_widgets import AdvancedDialog, SettingsDialog, PlotDialog
    from PyQt5 import QtCore as C

    app = create_application()
    window = MainWindow()
    try:
        assert window.tabs.count() == 5
        for index, page in enumerate(window.pages):
            page.load_example(confirm=False)
            code = page.compile_code()
            page.restore_code(code)
            assert page.compile_code() == code
            assert (page.grid_check is None) == (index in (1, 2, 3))
            assert page.show_legend is not None
            dialog = AdvancedDialog(page, 'the_plt.title("A")')
            assert dialog.check()
            dialog.editor.setPlainText("the_plt.title(")
            assert not dialog.check()
            dialog.close()
        panel_page = window.pages[0]
        panel_page.symbols_dialog()
        app.processEvents()
        panel = panel_page.symbol_panel
        assert panel.windowModality() == C.Qt.NonModal
        assert panel.windowFlags() & C.Qt.WindowStaysOnTopHint
        assert panel.width() <= 500 and panel.height() <= 450
        panel.close()
        data = window.pages[4]
        assert data.grid.showGrid()
        window.language.setCurrentIndex(1)
        assert window.tabs.tabText(0) == "Formula to Curves"
        assert all(
            not any("\u4e00" <= ch <= "\u9fff" for ch in w.text())
            for page in window.pages
            for w, key in page.text_bindings
        )
        window.language.setCurrentIndex(0)
        fig = plt.figure()
        preview = PlotDialog(window, fig)
        assert preview.windowModality() == C.Qt.ApplicationModal
        preview.close()
    finally:
        window.close()


def test_latex_outputs():
    from betu.latex_input import convert_formula

    assert convert_formula("lambda.^2+x^3", 2) == "lamda**2+x**3"
    result = convert_formula(r"\lambda^2+x^3")
    assert "lamda**2" in result and "^" not in result
    ast.parse(result, mode="eval")


def test_original_auto_ticks_and_scientific_notation():
    x = betu.Symbol("x")
    betu.draw_lines({"A": 1e5 * x, "B": 2e5 * x}, {}, x, [1, 2, 0.01])
    ax = plt.gca()
    ax.figure.canvas.draw()
    assert ax.yaxis.get_offset_text().get_text()
    assert len(ax.get_xticks()) > 2


def test_editor_zoom_spacing_and_error_line():
    from betu.main import create_application, MainWindow
    from betu.qt_widgets import CodeEditor
    from PyQt5 import QtGui as G, QtCore as C

    app = create_application()
    editor = CodeEditor()
    editor.setPlainText("x")
    cursor = editor.textCursor()
    cursor.movePosition(G.QTextCursor.End)
    editor.setTextCursor(cursor)
    editor.insert_symbol("alpha")
    assert editor.toPlainText() == "x alpha "
    editor.mark_error(1, "error")
    assert editor.error_line == 1
    editor.setPlaceholderText("Hint")
    editor.clear()
    assert editor.error_line == 0 and editor.placeholderText() == "Hint"
    with pytest.raises(ValueError) as exc:
        parse_formulas("A = x\nB = sin(")
    assert exc.value.lineno == 2
    window = MainWindow()
    p = window.pages[0]
    p.x_start.setValue(0)
    p.x_end.setValue(0.08)
    assert p.step.value() == 0.0008
    window.close()
    editor.close()


def test_style_editor_per_series_title_and_legend():
    from betu.main import create_application, MainWindow
    from betu.style_editor import StyleDialog

    app = create_application()
    window = MainWindow()
    page = window.pages[0]
    page.load_example(confirm=False)
    excluded = {
        "assigns",
        "expressions",
        "the_var",
        "ranges",
        "legend_options",
        "show_legend",
        "isgrid",
    }
    values = {
        key: value for key, value in page.parameters.items() if key not in excluded
    }
    values.update(legend_options=page.parameters["legend_options"], show_legend=True)
    dialog = StyleDialog(page, values, ["A", "B", "C", "D"], "draw_lines")
    dialog.common_fields["title"].field.setText("利润 Profit")
    dialog.selector.setCurrentIndex(1)
    dialog.series_fields["colors"].entry.setCurrentText("#aa3322")
    dialog.series_fields["linewidth"].field.setValue(2.5)
    dialog.series_fields["markers"].setCurrentIndex(
        dialog.series_fields["markers"].findData("D")
    )
    dialog.selector.setCurrentIndex(0)
    assert dialog.series_fields["colors"].entry.currentText() == values["colors"][0]
    dialog.selector.setCurrentIndex(1)
    assert dialog.series_fields["colors"].entry.currentText() == "#aa3322"
    dialog.legend_fields["ncol"].field.setValue(2)
    dialog.save()
    assert dialog.result() == dialog.Accepted
    page.parameters.update(dialog.values)
    code = page.compile_code()
    page.restore_code(code)
    assert page.parameters["title"] == "利润 Profit"
    assert page.parameters["legend_options"]["ncol"] == 2
    scope = {}
    exec(code, scope)
    assert plt.gca().get_title() == "利润 Profit"
    assert plt.gca().lines[1].get_color() == "#aa3322"
    assert plt.gca().lines[1].get_linewidth() == 2.5
    assert plt.gcf().get_figheight() > page.parameters["figsize"][1]
    window.close()


def test_single_curve_respects_explicit_style():
    x = betu.Symbol("x")
    betu.draw_lines(
        {"A": x**2},
        {},
        x,
        [0, 2, 0.1],
        colors=["crimson"],
        markers=["s"],
        linestyles=["dashed"],
        linewidth=[2],
    )
    line = plt.gca().lines[0]
    assert (
        line.get_color() == "crimson"
        and line.get_marker() == "s"
        and line.get_linestyle() == "--"
    )


def test_automatic_save_includes_legend(tmp_path):
    x = betu.Symbol("x")
    path = tmp_path / "legend.svg"
    betu.draw_lines({"VisibleLabel": x}, {}, x, [0, 2, 0.1], save_dir=path)
    assert "VisibleLabel" in path.read_text(encoding="utf-8")


def test_html_help_renders_math_and_code():
    from betu.main import create_application
    from betu.qt_widgets import HelpBrowser

    app = create_application()
    browser = HelpBrowser()
    for lang in ("zh", "en"):
        H.set_language(lang)
        browser.set_help(H.label(H.HELP_HTML))
        assert len(browser.formula_images) == 3
        assert all(not image.isNull() for image in browser.formula_images)
        assert "integrate" in browser.toPlainText()
        assert "formula:0" in browser.toHtml()
    browser.close()


def test_language_popup_at_small_window():
    from betu.main import create_application, MainWindow
    app=create_application();window=MainWindow();window.resize(900,600);window.show()
    combo=window.language
    for language in (0,1):
        combo.setCurrentIndex(language);combo.showPopup();app.processEvents()
        assert combo.width()>=138
        for row in range(combo.count()):
            assert combo.view().viewport().rect().contains(combo.view().visualRect(combo.model().index(row,0)))
        combo.hidePopup()
    window.close()


def test_title_and_annotation_in_automatic_save(tmp_path):
    parameters=H.default_parameters('draw_lines')
    path=tmp_path/'titled.svg'
    parameters.update(assigns={},the_var='x',ranges=[0,2,.1],save_dir=str(path),title='Saved Title')
    code=H.build_code('draw_lines','A = x**2',parameters,'the_plt.text(0.5, 1, "Saved Note")')
    exec(code,{})
    svg=path.read_text(encoding='utf-8')
    assert 'Saved Title' in svg and 'Saved Note' in svg
    function,formula,restored,advanced=read_plot_code(code)
    assert advanced=='the_plt.text(0.5, 1, "Saved Note")'


def test_mode_legend_matches_visible_regions():
    x,y=betu.symbols('x y')
    betu.draw_max_area({'A':x+y,'B':x+y+1,'C':x+y+2},{},x,[0,2],y,[0,2],precision=12,show_legend=True)
    labels=[text.get_text() for text in plt.gca().get_legend().get_texts()]
    assert labels==['C']


@pytest.mark.parametrize("axis", ["rows", "columns"])
@pytest.mark.parametrize("confirmed", [False, True])
def test_delete_table_confirmation(monkeypatch, axis, confirmed):
    from betu.main import create_application
    from betu.qt_widgets import DataGrid
    from PyQt5 import QtWidgets as W

    app = create_application()
    grid = DataGrid()
    grid.load(["A", "B", "C"], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    grid.setRangeSelected(W.QTableWidgetSelectionRange(0, 0, 1, 1), True)
    records = []

    def answer(dialog):
        assert dialog.defaultButton().text() == H.tr("cancel")
        assert "2" in dialog.text()
        records.append(dialog)
        return 0

    monkeypatch.setattr(W.QMessageBox, "exec_", answer)
    monkeypatch.setattr(
        W.QMessageBox,
        "clickedButton",
        lambda d: next(
            b
            for b in d.buttons()
            if b.text() == H.tr("confirm_delete" if confirmed else "cancel")
        ),
    )
    grid.delete_selected(axis)
    assert len(records) == 1
    assert (grid.rowCount() if axis == "rows" else grid.columnCount()) == (
        1 if confirmed else 3
    )
    grid.close()
