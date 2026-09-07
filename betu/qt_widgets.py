"""Qt5 通用控件、居中对话框与独占绘图窗口。"""

import ast
from copy import deepcopy
from PyQt5 import QtCore as C, QtGui as G, QtWidgets as W
from . import helpers as H


class Dialog(W.QDialog):
    def __init__(self, parent, key):
        super().__init__(parent)
        self.setWindowTitle(H.tr(key))
        self.setWindowModality(C.Qt.ApplicationModal)
        self.setWindowFlag(C.Qt.WindowContextHelpButtonHint, False)
        self.setSizeGripEnabled(True)

    def showEvent(self, event):
        super().showEvent(event)
        available = self.screen().availableGeometry()
        self.resize(
            min(self.width(), available.width() - 40),
            min(self.height(), available.height() - 60),
        )
        center = (
            self.parentWidget().window().frameGeometry().center()
            if self.parentWidget()
            else available.center()
        )
        rect = self.frameGeometry()
        rect.moveCenter(center)
        self.move(
            max(available.left(), min(rect.left(), available.right() - rect.width())),
            max(available.top(), min(rect.top(), available.bottom() - rect.height())),
        )


def button(key, callback, parent=None):
    b = W.QPushButton(H.tr(key), parent)
    b.clicked.connect(callback)
    return b


def error(parent, exc):
    W.QMessageBox.warning(parent, H.tr("error"), str(exc))


class NumberInput(W.QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLocale(C.QLocale.c())
        self.setMinimumWidth(50)
        self.setSizePolicy(W.QSizePolicy.Ignored, W.QSizePolicy.Fixed)

    def textFromValue(self, value):
        return (
            format(value, "." + str(self.decimals()) + "f").rstrip("0").rstrip(".")
            if self.decimals()
            else str(round(value))
        )

    def sizeHint(self):
        hint = super().sizeHint()
        hint.setWidth(95)
        return hint

    def minimumSizeHint(self):
        hint = super().minimumSizeHint()
        hint.setWidth(50)
        return hint


class ListPopupStyle(W.QProxyStyle):
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == W.QStyle.SH_ComboBox_Popup:
            return 0
        return super().styleHint(hint, option, widget, returnData)


class PopupDelegate(W.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(max(32, size.height() + 10))
        size.setWidth(size.width() + 24)
        return size


class ComboBox(W.QComboBox):
    """带滚动列表的下拉框，优先在控件下方展开。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.popup_style = ListPopupStyle("Fusion")
        self.popup_style.setParent(self)
        self.setStyle(self.popup_style)
        view = W.QListView()
        view.setUniformItemSizes(True)
        view.setTextElideMode(C.Qt.ElideNone)
        view.setHorizontalScrollBarPolicy(C.Qt.ScrollBarAlwaysOff)
        view.setItemDelegate(PopupDelegate(view))
        self.setView(view)
        self.setMaxVisibleItems(9)
        self.setMinimumHeight(30)

    def showPopup(self):
        rows = min(self.count(), self.maxVisibleItems())
        height = sum(self.view().sizeHintForRow(i) for i in range(rows)) + 6
        screen = self.screen().availableGeometry()
        origin = self.mapToGlobal(C.QPoint(0, self.height()))
        available = screen.bottom() - origin.y() - 5
        self.view().setMinimumHeight(min(height, max(40, available - 6)))
        self.view().setMinimumWidth(
            max(self.width(), self.view().sizeHintForColumn(0) + 26)
        )
        super().showPopup()
        popup = self.view().window()
        if available >= 70:
            popup.resize(
                min(popup.width(), screen.width()), min(popup.height(), available)
            )
            popup.move(
                max(screen.left(), min(origin.x(), screen.right() - popup.width())),
                origin.y(),
            )


def wrap_checkbox(editor, parent=None):
    control = W.QCheckBox(H.tr("wrap"), parent)
    control.toggled.connect(
        lambda checked: editor.setLineWrapMode(
            W.QPlainTextEdit.WidgetWidth if checked else W.QPlainTextEdit.NoWrap
        )
    )
    return control


class HelpBrowser(W.QTextBrowser):
    def set_help(self, html):
        import re
        from pathlib import Path
        from io import BytesIO
        from html import escape
        from matplotlib.mathtext import math_to_image

        assets = Path(__file__).parent / "assets"
        base_url = C.QUrl.fromLocalFile(str(assets) + "/")
        self.document().clear()
        self.document().setBaseUrl(base_url)
        self.document().setDefaultStyleSheet(H.HELP_CSS)
        self.setSearchPaths([str(assets)])
        self.formula_images = []
        images = {}

        def load_image(match):
            tag = match.group(0)
            source = re.search(r'\bsrc=["\x27]([^"\x27]+)["\x27]', tag)
            if source is None or not source.group(1).startswith("help/"):
                return tag
            name = source.group(1)
            width = re.search(r'\bwidth=["\x27](\d+)["\x27]', tag)
            display_width = int(width.group(1)) if width else 760
            if name not in images:
                reader = G.QImageReader(str(assets / name))
                reader.setDecideFormatFromContent(True)
                size = reader.size()
                pixel_width = round(display_width * max(2, self.devicePixelRatioF()))
                if size.isValid() and size.width() > pixel_width:
                    reader.setScaledSize(
                        C.QSize(
                            pixel_width,
                            max(1, round(size.height() * pixel_width / size.width())),
                        )
                    )
                images[name] = reader.read()
            image = images[name]
            if image.isNull():
                return "<p>" + escape(H.tr("help_image_missing", name=name)) + "</p>"
            url = C.QUrl(name)
            self.document().addResource(G.QTextDocument.ImageResource, url, image)
            self.document().addResource(
                G.QTextDocument.ImageResource, base_url.resolved(url), image
            )
            height = max(1, round(image.height() * display_width / image.width()))
            tag = re.sub(r'\sheight=["\x27]\d+["\x27]', "", tag)
            dimensions = f' height="{height}"'
            if width is None:
                dimensions += f' width="{display_width}"'
            return tag[:-1].rstrip(" /") + dimensions + ">"

        def render(match):
            data = BytesIO()
            math_to_image("$" + match.group(1) + "$", data, format="png", dpi=180)
            image = G.QImage.fromData(data.getvalue())
            url = C.QUrl("formula:" + str(len(self.formula_images)))
            self.formula_images.append(image)
            self.document().addResource(G.QTextDocument.ImageResource, url, image)
            return (
                '<img src="'
                + url.toString()
                + '" width="'
                + str(round(image.width() / 1.8))
                + '" height="'
                + str(round(image.height() / 1.8))
                + '">'
            )

        html = re.sub(r"<img\b[^>]*>", load_image, html)
        self.setHtml(re.sub(r"<math>(.*?)</math>", render, html, flags=re.S))
        self.setReadOnly(True)


class SettingsDialog(Dialog):
    def __init__(self, parent, values, legend=False):
        super().__init__(parent, "legend" if legend else "style")
        self.values = deepcopy(values)
        self.fields = {}
        self.defaults = deepcopy(values)
        self.resize(740, 650 if not legend else 510)
        layout = W.QVBoxLayout(self)
        scroll = W.QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        body = W.QWidget()
        form = W.QFormLayout(body)
        form.setSpacing(12)
        scroll.setWidget(body)
        self.legend = legend
        for name, value in values.items():
            if legend and name == "loc":
                field = ComboBox()
                for key, pair in H.LOC_LABELS.items():
                    field.addItem(H.label(pair), key)
                field.setCurrentIndex(max(0, field.findData(value)))
            elif isinstance(value, bool):
                field = W.QCheckBox()
                field.setChecked(value)
            else:
                field = W.QLineEdit(
                    repr(value) if not isinstance(value, str) else value
                )
            self.fields[name] = field
            label = (
                H.label(H.LEGEND_LABELS[name]) if legend else H.parameter_label(name)
            )
            if name in ("colors", "edgecolor"):
                row = W.QWidget()
                r = W.QHBoxLayout(row)
                r.setContentsMargins(0, 0, 0, 0)
                r.addWidget(field)
                pick = W.QPushButton("…")
                pick.setMaximumWidth(40)
                pick.clicked.connect(lambda _, f=field: self.pick_color(f))
                r.addWidget(pick)
                form.addRow(label + " (" + name + ")", row)
            else:
                form.addRow(label + " (" + name + ")", field)
        actions = W.QHBoxLayout()
        layout.addLayout(actions)
        actions.addWidget(button("reset", self.reset))
        actions.addStretch()
        actions.addWidget(button("cancel", self.reject))
        ok = button("ok", self.save)
        ok.setDefault(True)
        actions.addWidget(ok)

    def pick_color(self, field):
        try:
            current = ast.literal_eval(field.text())
        except (ValueError, SyntaxError):
            current = field.text()
        index = 0
        if isinstance(current, (list, tuple)):
            index, accepted = W.QInputDialog.getInt(
                self, H.tr("style"), H.tr("color_index"), 1, 1, len(current)
            )
            if not accepted:
                return
            index -= 1
        color = W.QColorDialog.getColor(parent=self)
        if color.isValid():
            if isinstance(current, (list, tuple)):
                current = list(current)
                current[index] = color.name()
                field.setText(repr(current))
            else:
                field.setText(color.name())

    def reset(self):
        for key, value in self.defaults.items():
            field = self.fields[key]
            if isinstance(field, W.QComboBox):
                field.setCurrentIndex(max(0, field.findData(value)))
            elif isinstance(field, W.QCheckBox):
                field.setChecked(value)
            else:
                field.setText(value if isinstance(value, str) else repr(value))

    def save(self):
        try:
            result = {}
            for key, field in self.fields.items():
                if isinstance(field, W.QComboBox):
                    value = field.currentData()
                elif isinstance(field, W.QCheckBox):
                    value = field.isChecked()
                else:
                    raw = field.text().strip()
                    try:
                        value = ast.literal_eval(raw)
                    except (ValueError, SyntaxError):
                        if (
                            isinstance(self.values[key], str)
                            or self.values[key] is None
                        ):
                            value = raw or None
                        else:
                            raise ValueError(H.tr("invalid_value", name=key, value=raw))
                result[key] = value
            if self.legend:
                from ._plotting import validate_legend

                result = validate_legend(result)
            else:
                import matplotlib.colors as colors

                for key in ("colors", "edgecolor"):
                    if key in result and result[key] is not None:
                        seq = (
                            result[key]
                            if isinstance(result[key], list)
                            else [result[key]]
                        )
                        for c in seq:
                            colors.to_rgba(c)
                for key in ("fsize", "precision", "density"):
                    if key in result and float(result[key]) <= 0:
                        raise ValueError(
                            H.tr("invalid_value", name=key, value=result[key])
                        )
                if "figsize" in result and (
                    len(result["figsize"]) != 2 or min(result["figsize"]) <= 0
                ):
                    raise ValueError(
                        H.tr("invalid_value", name="figsize", value=result["figsize"])
                    )
            self.values = result
            self.accept()
        except Exception as exc:
            error(self, exc)


class PythonHighlighter(G.QSyntaxHighlighter):
    def highlightBlock(self, text):
        import re, keyword

        for pattern, color in [
            (r"\b(" + "|".join(H.SYMPY_NAMES) + r")\b", "#137c98"),
            (r":=|\*\*", "#ba5c18"),
            (r"\b(" + "|".join(keyword.kwlist) + r")\b", "#7957b8"),
            (r"#[^\n]*", "#718096"),
            (r'"[^"\n]*"|\x27[^\x27\n]*\x27', "#197761"),
            (r"\b\d+(?:\.\d+)?\b", "#b85b25"),
        ]:
            fmt = G.QTextCharFormat()
            fmt.setForeground(G.QColor(color))
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)


class AdvancedDialog(Dialog):
    def __init__(self, parent, code):
        super().__init__(parent, "advanced")
        self.resize(860, 630)
        layout = W.QVBoxLayout(self)
        layout.addWidget(W.QLabel(H.tr("advanced_hint")))
        self.editor = CodeEditor()
        self.editor.setFont(G.QFont("Consolas", 11))
        self.editor.setPlainText(code)
        self.highlighter = PythonHighlighter(self.editor.document())
        extras = W.QHBoxLayout()
        layout.addLayout(extras)
        extras.addWidget(W.QLabel(H.tr("more_templates")))
        self.templates = ComboBox()
        for key, code in [
            ("add_title", H.label(H.TITLE_CODE)),
            ("add_text", H.label(H.TEXT_CODE)),
            ("add_save", H.SAVE_CODE),
        ]:
            self.templates.addItem(H.tr(key), code)
        for title, code in H.ADVANCED_SNIPPETS:
            self.templates.addItem(H.label(title), code)
        extras.addWidget(self.templates, 1)
        extras.addWidget(
            button(
                "insert",
                lambda: self.editor.appendPlainText(self.templates.currentData()),
            )
        )
        extras.addWidget(button("clear", self.editor.clear))
        self.wrap = wrap_checkbox(self.editor, self)
        layout.addWidget(self.wrap)
        layout.addWidget(self.editor, 1)
        note = W.QLabel(H.tr("advanced_note"))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.status = W.QLabel()
        layout.addWidget(self.status)
        bottom = W.QHBoxLayout()
        bottom.addWidget(button("check", self.check))
        bottom.addStretch()
        bottom.addWidget(button("cancel", self.reject))
        bottom.addWidget(button("ok", self.save))
        layout.addLayout(bottom)

    def check(self):
        try:
            compile(self.editor.toPlainText(), "<BeTu>", "exec")
            self.status.setText(H.tr("syntax_ok"))
            return True
        except SyntaxError as exc:
            message = H.tr("line_error", line=exc.lineno, message=exc.msg)
            self.status.setText(message)
            self.editor.mark_error(exc.lineno, message)
            return False

    def save(self):
        if self.check():
            self.accept()


class TableImportDialog(Dialog):
    def __init__(self, parent, rows):
        from .table import has_header, normalize_table

        super().__init__(parent, "table_preview")
        self.resize(780, 500)
        _, self.source_rows = normalize_table(rows, header=False)
        layout = W.QVBoxLayout(self)
        self.first_row_header = W.QCheckBox(H.tr("first_row_header"))
        self.first_row_header.setChecked(has_header(self.source_rows))
        layout.addWidget(self.first_row_header)
        hint = W.QLabel(H.tr("table_preview_hint"))
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.preview = W.QTableWidget()
        self.preview.setEditTriggers(W.QAbstractItemView.NoEditTriggers)
        self.preview.setShowGrid(True)
        self.preview.setAlternatingRowColors(True)
        layout.addWidget(self.preview, 1)
        self.count = W.QLabel()
        layout.addWidget(self.count)
        bottom = W.QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(button("cancel", self.reject))
        confirm = button("table_import_confirm", self.accept)
        confirm.setDefault(True)
        bottom.addWidget(confirm)
        layout.addLayout(bottom)
        self.first_row_header.toggled.connect(self.update_preview)
        self.update_preview()

    def update_preview(self):
        from .table import normalize_table

        self.headers, self.rows = normalize_table(
            self.source_rows, header=self.first_row_header.isChecked()
        )
        shown = min(50, len(self.rows))
        self.preview.clearContents()
        self.preview.setColumnCount(len(self.headers))
        self.preview.setRowCount(shown)
        self.preview.setHorizontalHeaderLabels(self.headers)
        for i, row in enumerate(self.rows[:shown]):
            for j, value in enumerate(row):
                self.preview.setItem(i, j, W.QTableWidgetItem(value))
        self.preview.resizeColumnsToContents()
        self.count.setText(
            H.tr(
                "table_preview_count",
                rows=len(self.rows),
                columns=len(self.headers),
                shown=shown,
            )
        )


class DataGrid(W.QTableWidget):
    pasted = C.pyqtSignal()
    zoomed = C.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(8, 3, parent)
        self.zoom = 100
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(W.QHeaderView.Interactive)
        self.setHorizontalHeaderLabels(["A", "B", "C"])
        self.horizontalHeader().sectionDoubleClicked.connect(self.rename_column)

    def rename_column(self, col):
        name, ok = W.QInputDialog.getText(
            self,
            H.tr("column_name"),
            H.tr("column_name"),
            text=self.horizontalHeaderItem(col).text(),
        )
        if ok and name.strip():
            self.setHorizontalHeaderItem(col, W.QTableWidgetItem(name.strip()))
            self.pasted.emit()

    def delete_selected(self, axis):
        indices = sorted(
            {
                index.row() if axis == "rows" else index.column()
                for index in self.selectedIndexes()
            },
            reverse=True,
        )
        if not indices:
            error(self, H.tr("select_cells_first"))
            return
        dialog = W.QMessageBox(
            W.QMessageBox.Question,
            H.tr("delete_" + axis),
            H.tr("confirm_delete_" + axis, count=len(indices)),
            parent=self,
        )
        confirm = dialog.addButton(H.tr("confirm_delete"), W.QMessageBox.AcceptRole)
        cancel = dialog.addButton(H.tr("cancel"), W.QMessageBox.RejectRole)
        dialog.setDefaultButton(cancel)
        dialog.setEscapeButton(cancel)
        dialog.exec_()
        if dialog.clickedButton() is not confirm:
            return
        for index in indices:
            (self.removeRow if axis == "rows" else self.removeColumn)(index)
        self.pasted.emit()

    def wheelEvent(self, event):
        if event.modifiers() & C.Qt.ControlModifier:
            self.zoom = max(
                50, min(250, self.zoom + (10 if event.angleDelta().y() > 0 else -10))
            )
            font = self.font()
            font.setPointSizeF(10 * self.zoom / 100)
            self.setFont(font)
            self.verticalHeader().setDefaultSectionSize(round(28 * self.zoom / 100))
            for col in range(self.columnCount()):
                self.setColumnWidth(col, round(140 * self.zoom / 100))
            self.zoomed.emit(self.zoom)
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.matches(G.QKeySequence.Paste):
            try:
                self.paste()
            except Exception as exc:
                error(self, exc)
            return
        if event.matches(G.QKeySequence.Copy):
            selected = self.selectedRanges()
            if selected:
                r = selected[0]
                rows = [
                    "\t".join(
                        self.item(i, j).text() if self.item(i, j) else ""
                        for j in range(r.leftColumn(), r.rightColumn() + 1)
                    )
                    for i in range(r.topRow(), r.bottomRow() + 1)
                ]
                W.QApplication.clipboard().setText("\n".join(rows))
            return
        super().keyPressEvent(event)

    def paste(self, replace=False):
        from .table import parse_pasted_table

        text = W.QApplication.clipboard().text()
        if replace:
            _, rows = parse_pasted_table(text, header=False)
            return self.import_rows(rows)
        else:
            _, rows = parse_pasted_table(text, header=False)
            row, col = max(self.currentRow(), 0), max(self.currentColumn(), 0)
            self.setRowCount(max(self.rowCount(), row + len(rows)))
            self.setColumnCount(max(self.columnCount(), col + len(rows[0])))
            for i, values in enumerate(rows):
                for j, value in enumerate(values):
                    self.setItem(row + i, col + j, W.QTableWidgetItem(value))
            for c in range(self.columnCount()):
                if not self.horizontalHeaderItem(c):
                    self.setHorizontalHeaderItem(c, W.QTableWidgetItem(str(c + 1)))
        self.pasted.emit()
        return True

    def import_rows(self, rows):
        dialog = TableImportDialog(self, rows)
        try:
            if dialog.exec_() != W.QDialog.Accepted:
                return False
            self.load(dialog.headers, dialog.rows)
            return True
        finally:
            dialog.deleteLater()

    def load(self, headers, rows):
        self.setColumnCount(len(headers))
        self.setRowCount(len(rows))
        self.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.setItem(i, j, W.QTableWidgetItem(str(value)))
        self.resizeColumnsToContents()
        self.pasted.emit()

    def data(self):
        from .table import normalize_table

        heads = [
            (
                self.horizontalHeaderItem(j).text()
                if self.horizontalHeaderItem(j)
                else str(j + 1)
            )
            for j in range(self.columnCount())
        ]
        rows = [
            [
                self.item(i, j).text() if self.item(i, j) else ""
                for j in range(self.columnCount())
            ]
            for i in range(self.rowCount())
        ]
        heads, rows = normalize_table([heads] + rows)
        return {name: [row[j] for row in rows] for j, name in enumerate(heads)}


class PlotDialog(Dialog):
    def __init__(self, parent, figure):
        super().__init__(parent, "plot_window")
        from matplotlib.backends.backend_qt5agg import (
            FigureCanvasQTAgg,
            NavigationToolbar2QT,
        )

        self.figure = figure
        self.canvas = FigureCanvasQTAgg(figure)
        layout = W.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas, 1)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)
        self.canvas.draw()
        self.resize(
            round(figure.get_figwidth() * 110), round(figure.get_figheight() * 110) + 55
        )

    def closeEvent(self, event):
        import matplotlib.pyplot as plt

        plt.close(self.figure)
        super().closeEvent(event)


class LineNumbers(W.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return C.QSize(self.editor.gutter_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_numbers(event)


class CodeEditor(W.QPlainTextEdit):
    zoomed = C.pyqtSignal(int)

    def __init__(self, parent=None, line_numbers=True):
        super().__init__(parent)
        self.show_line_numbers = line_numbers
        self._placeholder = ""
        self.error_line = 0
        self.error_message = ""
        self.base_size = 11
        self.setFont(G.QFont("Consolas", self.base_size))
        self.setLineWrapMode(W.QPlainTextEdit.NoWrap)
        self.numbers = LineNumbers(self)
        self.numbers.setVisible(line_numbers)
        self.blockCountChanged.connect(self.update_gutter)
        self.updateRequest.connect(self.update_numbers)
        self.cursorPositionChanged.connect(self.highlight_line)
        self.textChanged.connect(self.clear_error)
        self.update_gutter()
        self.highlighter = PythonHighlighter(self.document())
        self.highlight_line()

    def insert_symbol(self, value):
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        text = self.toPlainText()
        word = bool(value) and (value[0].isalpha() or value[0] == "_")
        before = text[start - 1 : start] if start else ""
        after = text[end : end + 1]
        prefix = (
            " " if word and before and (before.isalnum() or before in "_)]") else ""
        )
        suffix = " " if word and (not after or not after.isspace()) else ""
        cursor.insertText(prefix + value + suffix)
        self.setTextCursor(cursor)

    def setPlaceholderText(self, text):
        self._placeholder = text
        super().setPlaceholderText("")
        self.viewport().update()

    def placeholderText(self):
        return self._placeholder

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.toPlainText() and self._placeholder:
            painter = G.QPainter(self.viewport())
            painter.setFont(self.font())
            painter.setPen(G.QColor("#778698"))
            rect = self.viewport().rect().adjusted(8, 5, -8, -5)
            painter.drawText(
                rect,
                C.Qt.TextWordWrap | C.Qt.AlignTop | C.Qt.AlignLeft,
                self._placeholder,
            )

    def gutter_width(self):
        if not self.show_line_numbers:
            return 0
        return 22 + self.fontMetrics().horizontalAdvance("9") * len(
            str(max(1, self.blockCount()))
        )

    def update_gutter(self, *args):
        self.setViewportMargins(self.gutter_width(), 0, 0, 0)

    def update_numbers(self, rect, dy):
        if dy:
            self.numbers.scroll(0, dy)
        else:
            self.numbers.update(0, rect.y(), self.numbers.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_gutter()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.contentsRect()
        self.numbers.setGeometry(
            C.QRect(rect.left(), rect.top(), self.gutter_width(), rect.height())
        )

    def paint_numbers(self, event):
        painter = G.QPainter(self.numbers)
        painter.fillRect(event.rect(), G.QColor("#edf3f8"))
        painter.setFont(self.font())
        block = self.firstVisibleBlock()
        number = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(
                    G.QColor("#cf3c43" if number + 1 == self.error_line else "#71869a")
                )
                painter.drawText(
                    0,
                    top,
                    self.numbers.width() - 7,
                    self.fontMetrics().height(),
                    C.Qt.AlignRight,
                    str(number + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            number += 1

    def highlight_line(self):
        selections = []
        sel = W.QTextEdit.ExtraSelection()
        sel.format.setBackground(G.QColor("#f0f7fc"))
        sel.format.setProperty(G.QTextFormat.FullWidthSelection, True)
        sel.cursor = self.textCursor()
        sel.cursor.clearSelection()
        if self.toPlainText():
            selections.append(sel)
        if self.error_line:
            block = self.document().findBlockByNumber(self.error_line - 1)
            if block.isValid():
                sel = W.QTextEdit.ExtraSelection()
                sel.format.setBackground(G.QColor("#fde5e7"))
                sel.format.setProperty(G.QTextFormat.FullWidthSelection, True)
                sel.cursor = G.QTextCursor(block)
                selections.append(sel)
        self.setExtraSelections(selections)
        self.numbers.update()

    def mark_error(self, line, message):
        self.error_line = max(1, min(int(line), self.blockCount()))
        self.error_message = message
        block = self.document().findBlockByNumber(self.error_line - 1)
        self.setTextCursor(G.QTextCursor(block))
        self.ensureCursorVisible()
        self.setToolTip(message)
        self.highlight_line()

    def clear_error(self):
        self.error_line = 0
        self.setToolTip(H.tr("editor_tip"))
        self.highlight_line()

    def wheelEvent(self, event):
        if event.modifiers() & C.Qt.ControlModifier:
            size = max(
                8,
                min(
                    28,
                    self.font().pointSize() + (1 if event.angleDelta().y() > 0 else -1),
                ),
            )
            font = self.font()
            font.setPointSize(size)
            self.setFont(font)
            self.document().setDefaultFont(font)
            self.update_gutter()
            self.numbers.update()
            self.viewport().update()
            self.zoomed.emit(round(size / self.base_size * 100))
            event.accept()
        else:
            super().wheelEvent(event)
