import os
from copy import deepcopy
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import pytest
from PyQt5 import QtWidgets as W
from betu import helpers as H
from betu.main import create_application, MainWindow
from betu.qt_widgets import TableImportDialog
from betu.table import normalize_table, parse_pasted_table, read_table


STUDENT_DATA = "S001\t16.8\t76.5\nS002\t8.1\t61.4\nS003\t10.1\t61.8"
STUDENT_HEADER = "学号\t每周自习时长（小时）\t数学成绩\n"


@pytest.fixture
def window():
    app = create_application()
    view = MainWindow()
    yield view
    view.close()
    app.processEvents()
    H.set_language("zh")


@pytest.mark.parametrize("with_header", [False, True])
def test_detect_student_headers_without_losing_first_record(with_header):
    text = (STUDENT_HEADER if with_header else "") + STUDENT_DATA
    headers, rows = parse_pasted_table(text, header=None)
    assert rows[0] == ["S001", "16.8", "76.5"]
    assert len(rows) == 3
    assert headers[0] == ("学号" if with_header else H.tr("message_17", v0=1))


@pytest.mark.parametrize(
    "text",
    [
        "16.8\n8.1",
        "S001\tGroup A\nS002\tGroup B",
        "2026-09-01\tA\n2026-09-02\tB",
        "S001\t16.8",
    ],
)
def test_uncertain_or_numeric_first_rows_are_preserved(text):
    _, rows = parse_pasted_table(text, header=None)
    assert rows == [line.split("\t") for line in text.splitlines()]


def test_explicit_numeric_headers_and_existing_api_default():
    text = "2024\t2025\n16.8\t8.1"
    headers, rows = parse_pasted_table(text)
    assert headers == ["2024", "2025"]
    assert rows == [["16.8", "8.1"]]
    assert len(parse_pasted_table(text, header=False)[1]) == 2


def test_preview_toggle_restores_first_row_and_handles_numeric_headers(window):
    _, source = parse_pasted_table(STUDENT_HEADER + STUDENT_DATA, header=False)
    original = deepcopy(source)
    dialog = TableImportDialog(window, source)
    assert dialog.first_row_header.isChecked()
    assert dialog.rows[0][0] == "S001"
    for _ in range(3):
        dialog.first_row_header.setChecked(False)
        assert len(dialog.rows) == 4 and dialog.rows[0][0] == "学号"
        dialog.first_row_header.setChecked(True)
        assert len(dialog.rows) == 3 and dialog.headers[0] == "学号"
    assert source == original
    numeric = TableImportDialog(window, [["2024", "2025"], ["16.8", "8.1"]])
    assert not numeric.first_row_header.isChecked()
    numeric.first_row_header.setChecked(True)
    assert numeric.headers == ["2024", "2025"]
    assert numeric.rows == [["16.8", "8.1"]]


@pytest.mark.parametrize("confirmed", [False, True])
def test_paste_button_preview_and_cancellation(window, monkeypatch, confirmed):
    page = window.pages[4]
    page.grid.load(["Old"], [["Keep me"]])
    monkeypatch.setattr(
        W.QApplication, "clipboard", lambda: SimpleNamespace(text=lambda: STUDENT_DATA)
    )

    def answer(dialog):
        assert not dialog.first_row_header.isChecked()
        assert dialog.preview.item(0, 0).text() == "S001"
        assert dialog.preview.rowCount() == 3
        return W.QDialog.Accepted if confirmed else W.QDialog.Rejected

    monkeypatch.setattr(TableImportDialog, "exec_", answer)
    page.paste_data()
    if confirmed:
        assert page.grid.rowCount() == 3
        assert page.grid.item(0, 0).text() == "S001"
        assert page.x.currentIndex() == 1
        assert len(page.series.selectedItems()) == 2
    else:
        assert page.grid.data() == {"Old": ["Keep me"]}


def test_cell_paste_keeps_every_row_at_selected_cell(window, monkeypatch):
    grid = window.pages[4].grid
    grid.load(["ID", "Hours", "Score"], [["Existing", "1", "2"], ["", "", ""]])
    grid.setCurrentCell(1, 0)
    monkeypatch.setattr(
        W.QApplication, "clipboard", lambda: SimpleNamespace(text=lambda: STUDENT_DATA)
    )
    monkeypatch.setattr(
        TableImportDialog,
        "exec_",
        lambda _: pytest.fail("Cell paste must not open a header preview"),
    )
    grid.paste()
    assert grid.data()["ID"] == ["Existing", "S001", "S002", "S003"]
    assert grid.horizontalHeaderItem(1).text() == "Hours"


@pytest.mark.parametrize("suffix", [".csv", ".xlsx"])
@pytest.mark.parametrize("with_header", [False, True])
def test_file_import_uses_same_preview(
    window, monkeypatch, tmp_path, suffix, with_header
):
    path = tmp_path / ("students" + suffix)
    text = (STUDENT_HEADER if with_header else "") + STUDENT_DATA
    if suffix == ".csv":
        path.write_text(text.replace("\t", ","), encoding="utf-8-sig")
    else:
        from openpyxl import Workbook

        book = Workbook()
        for row in text.splitlines():
            book.active.append(row.split("\t"))
        book.save(path)
        book.close()
    assert read_table(path, header=None)[1][0][0] == "S001"
    monkeypatch.setattr(
        W.QFileDialog, "getOpenFileName", lambda *a, **k: (str(path), "")
    )

    def answer(dialog):
        assert dialog.first_row_header.isChecked() == with_header
        assert dialog.rows[0][0] == "S001"
        return W.QDialog.Accepted

    monkeypatch.setattr(TableImportDialog, "exec_", answer)
    page = window.pages[4]
    page.import_data()
    assert page.grid.rowCount() == 3
    assert page.grid.item(0, 0).text() == "S001"


def test_preview_limit_does_not_truncate_import_and_single_series(window, monkeypatch):
    page = window.pages[4]
    source = [[str(i)] for i in range(120)]

    def answer(dialog):
        assert dialog.preview.rowCount() == 50
        assert len(dialog.rows) == 120
        return W.QDialog.Accepted

    monkeypatch.setattr(TableImportDialog, "exec_", answer)
    assert page.grid.import_rows(source)
    page.table_imported()
    assert page.grid.rowCount() == 120
    assert page.grid.item(119, 0).text() == "119"
    assert page.x.currentIndex() == 0
    assert len(page.series.selectedItems()) == 1
