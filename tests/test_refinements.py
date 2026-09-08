import ast
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import numpy as np
import matplotlib.pyplot as plt
import pytest
from PyQt5 import QtCore as C, QtGui as G, QtWidgets as W, QtTest
import betu
from betu import helpers as H
from betu.formula import parse_formulas, parse_assignments, read_plot_code
from betu.main import create_application, MainWindow
from betu.qt_widgets import CodeEditor, ComboBox, AdvancedDialog


@pytest.fixture
def window():
    app = create_application()
    view = MainWindow()
    yield view
    view.close()
    app.processEvents()
    plt.close("all")
    H.set_language("zh")


@pytest.mark.parametrize(
    "formula,expected",
    [
        ("F = integrate(a*t+x, (t, 0, y))", ["a", "x", "y"]),
        ("F = integrate(t*x, (t, 0, 1))+t", ["t", "x"]),
        ("p := a*t\nF = integrate(p, (t, 0, y))+x", ["a", "x", "y"]),
        ("F = integrate(t*x, (t, 0, t))", ["t", "x"]),
        ("F = integrate(t*x, (t, 0, y), (y, 0, a))", ["a", "x"]),
        ("F = integrate(t*x, t)", ["t", "x"]),
        ("F = summation(a*t, (t, 0, n))", ["a", "n"]),
    ],
)
def test_bound_names(formula, expected):
    plan = parse_formulas(formula)
    assert "t" in plan.symbols
    assert plan.analysis_symbols == expected


@pytest.mark.parametrize("index", range(4))
def test_analysis_assignment_memory(window, index):
    page = window.pages[index]
    p = H.default_parameters(page.function)
    p.update(assigns={"a": 2, "y": 0.5, "z": 3})
    if index:
        p.update(the_var_x="x", the_var_y="z", start_end_x=[0, 2], start_end_y=[0, 2])
        p["assigns"].pop("z")
    else:
        p.update(the_var="x", ranges=[0, 2, 0.02])
    page.restore_code(
        H.build_code(page.function, "F = integrate(a*t, (t, 0, x))+y+z\nG = x-y+z", p)
    )
    assert page.assigns.gutter_width() == 0
    assert "assigns" not in page.wrap_controls
    assert page.assigns.lineWrapMode() == W.QPlainTextEdit.WidgetWidth
    assert page.x.findText("t") == -1
    assert parse_assignments(page.assigns.toPlainText())["y"] == 0.5
    page.x.setCurrentText("y")
    assert "y" not in parse_assignments(page.assigns.toPlainText())
    assert parse_assignments(page.assigns.toPlainText())["x"] == 1
    page.x.setCurrentText("x")
    assert parse_assignments(page.assigns.toPlainText())["y"] == 0.5
    if index:
        page.y.setCurrentText("y")
        assert "y" not in parse_assignments(page.assigns.toPlainText())
        page.y.setCurrentText("z")
        assert parse_assignments(page.assigns.toPlainText())["y"] == 0.5
    page.assigns.setPlainText("a=2, y=oops(")
    old = page.x.currentText()
    page.x.setCurrentText("a")
    assert page.x.currentText() == old
    assert page.assigns.toPlainText() == "a=2, y=oops("


@pytest.mark.parametrize("index", range(5))
def test_save_edit_and_wrap(window, index, tmp_path, monkeypatch):
    page = window.pages[index]
    page.load_example(confirm=False)
    window.tabs.setCurrentIndex(index)
    for key, check in page.wrap_controls.items():
        editor = (
            page.output
            if key == "output"
            else page.editor if key == "formula" else page.assigns
        )
        check.setChecked(True)
        assert editor.lineWrapMode() == W.QPlainTextEdit.WidgetWidth
        check.setChecked(False)
        assert editor.lineWrapMode() == W.QPlainTextEdit.NoWrap
    path = tmp_path / ("page" + str(index) + ".py")
    calls = []

    def choose(*args):
        calls.append(1)
        return str(path), ""

    monkeypatch.setattr(W.QFileDialog, "getSaveFileName", choose)
    page.save_code()
    assert page.code_path == path
    assert H.tr("save_update") == page.save_button.text()
    assert not hasattr(page, "edit_code")
    assert page.output.isReadOnly()
    page.parameters["fsize"] = 18
    code = page.compile_code()
    window.show()
    window.activateWindow()
    page.output.setFocus()
    W.QApplication.processEvents()
    QtTest.QTest.keyClicks(page.output, "unwanted edit")
    assert page.output.toPlainText() == code
    QtTest.QTest.keyClick(page.output, C.Qt.Key_S, C.Qt.ControlModifier)
    W.QApplication.processEvents()
    assert path.read_text(encoding="utf-8") == code
    assert len(calls) == 1
    assert page.output.isReadOnly()
    assert page.code_path == path
    page.load_example(confirm=False)
    assert page.code_path is None


def test_existing_file_restores_controls(window, tmp_path, monkeypatch):
    page = window.pages[0]
    source = tmp_path / "opened.py"
    source.write_text(H.example_code("draw_lines").replace("fsize = 14", "fsize = 18"), encoding="utf-8")
    monkeypatch.setattr(W.QFileDialog, "getOpenFileName", lambda *a: (str(source), ""))
    page.open_code()
    assert page.code_path == source
    assert page.parameters["fsize"] == 18
    assert page.output.isReadOnly()
    page.save_code()
    assert "fsize = 18" in source.read_text(encoding="utf-8")


def test_advanced_wrap_and_markers(window):
    from betu.style_editor import StyleDialog

    page = window.pages[0]
    page.load_example(confirm=False)
    d = AdvancedDialog(page, "")
    d.wrap.setChecked(True)
    assert d.editor.lineWrapMode() == W.QPlainTextEdit.WidgetWidth
    style = StyleDialog(page, page.parameters, ["A", "B"], page.function)
    markers = style.series_fields["markers"]
    assert markers.itemText(markers.findData("o")) == H.label(H.MARKER_NAMES["o"])
    assert not markers.itemIcon(markers.findData("o")).isNull()
    colors = style.series_fields["colors"].entry
    for index in range(colors.count()):
        value = colors.itemData(index)
        if value:
            from matplotlib.colors import to_hex

            icon = colors.itemIcon(index)
            assert not icon.isNull()
            swatch = icon.pixmap(24, 18).toImage()
            assert swatch.pixelColor(12, 9).name() == to_hex(value)
    lines = style.series_fields["linestyles"]
    assert all(not lines.itemIcon(i).isNull() for i in range(lines.count()))
    assert (
        lines.itemIcon(0).pixmap(48, 22).toImage()
        != lines.itemIcon(1).pixmap(48, 22).toImage()
    )
    assert all(
        isinstance(combo, ComboBox) for combo in window.findChildren(W.QComboBox)
    )
    d.close()
    style.close()


def test_conversion_modes_and_wrapping(window, monkeypatch):
    from betu.qt_widgets import Dialog

    def inspect(dialog):
        modes = dialog.findChild(ComboBox)
        assert [modes.itemData(i) for i in range(3)] == [1, 2, 0]
        modes.setCurrentIndex(2)
        assert any(
            label.text() == H.tr("latex_hint_general")
            for label in dialog.findChildren(W.QLabel)
        )
        assert len(dialog.findChildren(CodeEditor)) == 2
        assert (
            len(
                [
                    c
                    for c in dialog.findChildren(W.QCheckBox)
                    if c.text() == H.tr("wrap")
                ]
            )
            == 2
        )
        return 0

    monkeypatch.setattr(Dialog, "exec_", inspect)
    window.pages[0].latex_dialog()


def test_precision_and_icon(window):
    for fn in H.TAB_FUNCTIONS[1:4]:
        assert H.default_parameters(fn)["precision"] == 1000
        assert read_plot_code(H.example_code(fn))[2]["precision"] == 1000
    assert not window.windowIcon().isNull()


def test_connected_regions_and_each_component_label():
    from betu.region_labels import connected_regions

    mask = np.zeros((20, 30), dtype=bool)
    mask[1:6, 1:4] = True
    mask[3:12, 18:25] = True
    mask[16, 2] = True
    components = list(connected_regions(mask))
    assert len(components) == 3
    assert sum(c[0].sum() for c in components) == mask.sum()
    diagonal = np.eye(1000, dtype=bool)
    assert len(list(connected_regions(diagonal))) == 1
    x, y = betu.symbols("x y")
    betu.draw_max_area(
        {"NC": (x - 0.4) * (x - 0.6), "NP": 0 * x},
        {},
        x,
        [0, 1],
        y,
        [0, 1],
        precision=100,
        show_legend=True,
    )
    ax = plt.gca()
    regions = ax._betu_regions
    assert sum(text.get_text() == "NC" for text, *_ in regions) == 2
    assert len(ax.get_legend().get_texts()) == 2
    for text, mask, xs, ys in regions:
        if text.get_visible():
            tx, ty = text.get_position()
            assert mask[np.argmin(abs(ys - ty)), np.argmin(abs(xs - tx))]
    plt.close("all")


@pytest.mark.parametrize("dpi", [100, 180])
def test_small_region_arrows_and_title(tmp_path, dpi):
    from betu.advanced import plot_context

    x, y = betu.symbols("x y")
    plot = betu.draw_detail_area(
        {"A": x, "B": 0.49 + 0 * x, "C": 0.51 + 0 * x, "D": y},
        {},
        x,
        [0, 1],
        y,
        [0, 1],
        precision=100,
        dropout=0.00001,
    )
    fig, ax = plot.gcf(), plot.gca()
    arrows = ax._betu_callouts
    assert arrows
    assert len(arrows) <= 16
    plot_context(plot).title("Region comparison")
    fig.set_dpi(dpi)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = [a.get_bbox_patch().get_window_extent(renderer) for a in arrows]
    for i, box in enumerate(boxes):
        assert box.y0 >= ax.bbox.y1
        assert not box.overlaps(ax.title.get_window_extent(renderer))
        assert not any(box.overlaps(other) for other in boxes[i + 1 :])
    for annotation in arrows:
        text, mask, xs, ys = next(
            r
            for r in ax._betu_regions
            if r[0].get_text() == annotation._betu_region_label
        )
        tx, ty = annotation.xy
        assert mask[np.argmin(abs(ys - ty)), np.argmin(abs(xs - tx))]
    before = fig.get_size_inches().copy()
    rendered_bounds = []

    def record_bounds(event):
        rendered_bounds.extend(
            (
                a.get_bbox_patch().get_window_extent(event.renderer).frozen(),
                fig.bbox.frozen(),
            )
            for a in arrows
        )

    token = fig.canvas.mpl_connect("draw_event", record_bounds)
    plot_context(plot).savefig(tmp_path / "arrows.svg", bbox_inches="tight")
    fig.canvas.mpl_disconnect(token)
    assert np.allclose(fig.get_size_inches(), before)
    assert rendered_bounds
    for box, canvas in rendered_bounds:
        assert box.x0 >= canvas.x0 and box.y0 >= canvas.y0
        assert box.x1 <= canvas.x1 and box.y1 <= canvas.y1
    plt.close("all")


@pytest.mark.parametrize("name", ["draw_detail_area", "smart_regions"])
def test_region_examples_at_default_precision(name):
    code = H.example_code(name)
    assert "precision = 1000" in code
    exec(code.replace("the_plt.show()", ""), {})
    fig, ax = plt.gcf(), plt.gca()
    assert len(ax._betu_regions) == 6
    for item in ax.get_legend().get_texts():
        assert item.get_text().startswith("Region ")
        assert ": $" in item.get_text()
    assert [t.get_text() for t, *_ in ax._betu_regions] == [
        "Region " + number for number in ("I", "II", "III", "IV", "V", "VI")
    ]
    arrows = getattr(ax, "_betu_callouts", [])
    if name == "draw_detail_area":
        expected_positions = {"Region II": (0.753, 0.049), "Region III": (0.725, 0.054)}
        manual_arrows = [arrow for arrow in arrows if arrow.get_text() in expected_positions]
        assert len(arrows) == 2
        assert len(manual_arrows) == 2
        for arrow in manual_arrows:
            assert not arrow._betu_external
            assert np.allclose(
                arrow.get_position(), expected_positions[arrow.get_text()], atol=0.001
            )
            assert arrow.xy[1] > arrow.get_position()[1]
        function, formula, parameters, _ = read_plot_code(code)
        assert parameters["assigns"]["E"] == 2.0
        assert parameters["the_var_x"] == "alpha"
        assert parameters["start_end_x"] == [0.7, 0.8]
        assert parameters["the_var_y"] == "b"
        assert parameters["start_end_y"] == [0, 0.08]
    else:
        assert 1 <= len(arrows) <= 6
    assert fig.get_figheight() < 10
    plt.close("all")


def test_manual_offset_retained_for_disconnected_modes():
    x, y = betu.symbols("x y")
    args = ({"NC": (x - 0.4) * (x - 0.6), "NP": 0 * x}, {}, x, [0, 1], y, [0, 1])
    betu.draw_max_area(*args, precision=100, smart_labels=False)
    before = [t.get_position() for t, *_ in plt.gca()._betu_regions]
    betu.draw_max_area(*args, precision=100, pattern_moves=[[0.01, 0.03], [0.01, 0.03]])
    after = [t.get_position() for t, *_ in plt.gca()._betu_regions]
    assert len(before) == len(after) == 3
    assert np.allclose(np.asarray(after)[:2] - np.asarray(before)[:2], [0.01, 0.03])
    assert not getattr(plt.gca(), "_betu_callouts", [])
    plt.close("all")


def test_help_images_are_available_offline(window):
    import re
    from betu.qt_widgets import HelpBrowser

    browser = HelpBrowser()
    browser.set_help(H.HELP_HTML[0])
    for html in H.HELP_HTML:
        for name in re.findall(r'<img src="([^"]+)"', html):
            resource = browser.document().resource(
                G.QTextDocument.ImageResource, C.QUrl(name)
            )
            assert resource is not None, name
            assert not resource.isNull(), name
    browser.close()


def test_help_limits_image_memory_and_reloads_replaced_files(
    window, monkeypatch, tmp_path
):
    import betu.qt_widgets as widgets

    assets = tmp_path / "assets" / "help"
    assets.mkdir(parents=True)
    monkeypatch.setattr(widgets, "__file__", str(tmp_path / "qt_widgets.py"))
    path = assets / "replacement.png"
    source = G.QImage(3200, 1800, G.QImage.Format_RGB32)
    source.fill(G.QColor("red"))
    assert source.save(str(path), "PNG")
    browser = widgets.HelpBrowser()
    html = '<p><img src="help/replacement.png" width="600"></p>'
    browser.set_help(html)
    image = browser.document().resource(
        G.QTextDocument.ImageResource, C.QUrl("help/replacement.png")
    )
    assert (image.width(), image.height()) == (1200, 675)
    assert image.pixelColor(0, 0) == G.QColor("red")
    assert 'height="338"' in browser.document().toHtml()
    source.fill(G.QColor("blue"))
    assert source.save(str(path), "PNG")
    browser.set_help(html)
    image = browser.document().resource(
        G.QTextDocument.ImageResource, C.QUrl("help/replacement.png")
    )
    assert image.pixelColor(0, 0) == G.QColor("blue")
    absolute = browser.document().baseUrl().resolved(C.QUrl("help/replacement.png"))
    assert (
        not browser.document()
        .resource(G.QTextDocument.ImageResource, absolute)
        .isNull()
    )
    browser.close()


def test_help_detects_image_content_and_reports_missing_files(
    window, monkeypatch, tmp_path
):
    import betu.qt_widgets as widgets

    assets = tmp_path / "assets" / "help"
    assets.mkdir(parents=True)
    monkeypatch.setattr(widgets, "__file__", str(tmp_path / "qt_widgets.py"))
    image = G.QImage(120, 60, G.QImage.Format_RGB32)
    image.fill(G.QColor("green"))
    assert image.save(str(assets / "legacy.png"), "JPG")
    browser = widgets.HelpBrowser()
    browser.set_help(
        '<img src="help/legacy.png" width="120"><img src="help/missing.png" width="120">'
    )
    resource = browser.document().resource(
        G.QTextDocument.ImageResource, C.QUrl("help/legacy.png")
    )
    assert not resource.isNull()
    assert "help/missing.png" in browser.toPlainText()
    browser.close()


def test_dropout_filters_individual_fragments():
    from betu.region_labels import filter_small_regions

    mask = np.zeros((100, 100), dtype=bool)
    mask[40:60, 40:60] = True
    mask[0:20:4, 0:20:4] = True
    mask[80:82, 80:82] = True
    original = mask.copy()
    result = filter_small_regions(mask, 0.001)
    assert np.count_nonzero(result) == 400
    assert result[40:60, 40:60].all()
    assert np.array_equal(mask, original)
    assert np.array_equal(filter_small_regions(mask, 0), original)


def test_default_mode_example_drops_tiny_tie_regions():
    code = H.example_code("draw_max_area")
    assert "dropout = 0.001" in code
    exec(code.replace("the_plt.show()", ""), {})
    ax = plt.gca()
    assert len(ax._betu_regions) == 4
    assert not getattr(ax, "_betu_callouts", [])
    assert all(
        np.count_nonzero(mask) >= 1000 and "," not in text.get_text()
        for text, mask, *_ in ax._betu_regions
    )
    plt.close("all")


def test_mode_dropout_is_applied_after_merging_orderings():
    x, y = betu.symbols("x y")
    betu.draw_max_area(
        {"A": 0.51 + 0 * x, "B": x, "C": y},
        {},
        x,
        [0, 1],
        y,
        [0, 1],
        precision=100,
        dropout=0.2,
        show_legend=True,
    )
    ax = plt.gca()
    region = next(mask for text, mask, *_ in ax._betu_regions if text.get_text() == "A")
    assert np.count_nonzero(region) >= 2500
    assert len(ax.get_legend().get_texts()) == 3
    plt.close("all")


@pytest.mark.parametrize("value", [-0.001, 1.01, float("nan"), float("inf")])
def test_dropout_rejects_invalid_values(value):
    x, y = betu.symbols("x y")
    with pytest.raises(ValueError, match="dropout"):
        betu.draw_max_area({"A": x, "B": y}, {}, x, [0, 1], y, [0, 1], dropout=value)


@pytest.mark.parametrize("function", ["draw_max_area", "draw_detail_area"])
def test_dropout_style_and_code_roundtrip(window, function):
    from betu.style_editor import StyleDialog

    settings = H.default_parameters(function)
    settings.update(the_var_x="x", the_var_y="y", assigns={}, dropout=0.005)
    dialog = StyleDialog(window, settings, ["A", "B"], function)
    field = dialog.common_fields["dropout"]
    assert field.field.minimum() == 0
    assert field.field.maximum() == 1
    assert field.value() == 0.005
    _, _, restored, _ = read_plot_code(H.build_code(function, "A = x\nB = y", settings))
    assert restored["dropout"] == 0.005
    dialog.close()


def test_surface_and_relationship_examples_share_paper_parameters():
    _, formula_3d, surface, _ = read_plot_code(H.example_code("draw_3D"))
    _, formula_regions, regions, _ = read_plot_code(H.example_code("draw_detail_area"))
    assert formula_3d == formula_regions
    for key in (
        "assigns",
        "the_var_x",
        "the_var_y",
        "start_end_x",
        "start_end_y",
        "x_name",
        "y_name",
    ):
        assert surface[key] == regions[key]
    assert surface["z_name"] == r"$\pi_r$"
    defaults = H.default_parameters("draw_3D")
    for key in ("colors", "linestyles", "linewidth", "edgecolor", "color_alpha"):
        assert surface[key] == defaults[key]


def test_surface_profit_ticks_and_exported_axis_name(tmp_path):
    fn, formula, params, _ = read_plot_code(H.example_code("draw_3D"))
    params["precision"] = 60
    exec(H.build_code(fn, formula, params).replace("the_plt.show()", ""), {})
    fig, ax = plt.gcf(), plt.gca()
    fig.canvas.draw()
    labels = [label.get_text() for label in ax.get_zticklabels()]
    assert len(set(labels)) == len(labels)
    renderer = fig.canvas.get_renderer()
    frame = ax.get_tightbbox(renderer)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        box = axis.label.get_window_extent(renderer)
        assert frame.x0 <= box.x0 <= box.x1 <= frame.x1
        assert frame.y0 <= box.y0 <= box.y1 <= frame.y1
    bounds = []

    def record(event):
        bounds.append(
            (
                ax.zaxis.label.get_window_extent(event.renderer).frozen(),
                fig.bbox.frozen(),
            )
        )

    connection = fig.canvas.mpl_connect("draw_event", record)
    fig.savefig(tmp_path / "surface.svg", bbox_inches="tight")
    fig.canvas.mpl_disconnect(connection)
    assert bounds
    label, canvas = bounds[-1]
    assert canvas.x0 <= label.x0 <= label.x1 <= canvas.x1
    assert canvas.y0 <= label.y0 <= label.y1 <= canvas.y1
    plt.close("all")
