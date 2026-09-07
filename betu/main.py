"""BeTu Qt5 主界面。"""

import ast
import sys
from pathlib import Path
from copy import deepcopy
from PyQt5 import QtCore as C, QtGui as G, QtWidgets as W
from . import helpers as H
from .formula import parse_formulas, read_plot_code, parse_assignments, AssignmentMemory
from .qt_widgets import (
    CodeEditor,
    Dialog,
    NumberInput,
    ListPopupStyle,
    ComboBox,
    HelpBrowser,
    AdvancedDialog,
    DataGrid,
    PlotDialog,
    PythonHighlighter,
    button,
    error,
    wrap_checkbox,
)


class PlotWorker(C.QThread):
    result = C.pyqtSignal(object)
    failed = C.pyqtSignal(str)

    def __init__(self, code, parent):
        super().__init__(parent)
        self.code = code

    def run(self):
        try:
            tree = ast.parse(self.code)
            tree.body = [
                node
                for node in tree.body
                if not (
                    isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Attribute)
                    and node.value.func.attr == "show"
                    and isinstance(node.value.func.value, ast.Name)
                    and node.value.func.value.id in ("the_plt", "plt")
                )
            ]
            scope = {}
            exec(compile(tree, "<BeTu>", "exec"), scope)
            figure = scope["the_plt"].gcf()
            figure.canvas.draw()
            self.result.emit(figure)
        except Exception as exc:
            self.failed.emit(str(exc))


class PlotTab(W.QWidget):
    def __init__(self, window, index):
        super().__init__()
        self.main = window
        self.index = index
        self.function = H.TAB_FUNCTIONS[index]
        self.parameters = H.default_parameters(self.function)
        self.advanced_code = ""
        self.plan = None
        self.text_bindings = []
        self.wrap_controls = {}
        self.assignment_memory = AssignmentMemory()
        self._syncing_axes = False
        self._restoring = False
        self._axis_selection = ("", "")
        self.code_path = None
        self.is_data = index == 4
        outer = W.QVBoxLayout(self)
        outer.setSpacing(8)
        split = W.QSplitter(C.Qt.Horizontal)
        outer.addWidget(split, 1)
        left = W.QWidget()
        left_layout = W.QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        split.addWidget(left)
        right = W.QWidget()
        right_layout = W.QVBoxLayout(right)
        right_layout.setContentsMargins(4, 4, 10, 4)
        sidebar = W.QScrollArea()
        sidebar.setWidgetResizable(True)
        sidebar.setWidget(right)
        sidebar.setMinimumWidth(350)
        sidebar.setMaximumWidth(560)
        sidebar.setHorizontalScrollBarPolicy(C.Qt.ScrollBarAlwaysOff)
        split.addWidget(sidebar)
        split.setStretchFactor(0, 1)
        split.setSizes([760, 420])
        if not self.is_data:
            self.editor = CodeEditor()
            expression_header = W.QHBoxLayout()
            left_layout.addLayout(expression_header)
            self.add_label(expression_header, "expression")
            expression_header.addStretch()
            self.add_wrap(expression_header, self.editor, "formula")
            self.editor.setFont(G.QFont("Consolas", 11))
            self.editor.setPlaceholderText(H.label(H.FORMULA_PLACEHOLDER))
            self.editor.setToolTip(H.tr("editor_tip"))
            self.editor.zoomed.connect(
                lambda value: self.main.statusBar().showMessage(
                    f'{H.tr("ready")} · {value}%'
                )
            )
            left_layout.addWidget(self.editor, 2)
            self.highlighter = PythonHighlighter(self.editor.document())
            row = W.QHBoxLayout()
            left_layout.addLayout(row)
            for key, fn in [
                ("recognize", self.recognize),
                ("symbols", self.symbols_dialog),
                ("latex", self.latex_dialog),
                ("clear", self.editor.clear),
            ]:
                self.add_button(row, key, fn)
            self.add_label(right_layout, "parameters")
            form = W.QFormLayout()
            right_layout.addLayout(form)
            self.x = ComboBox()
            self.y = ComboBox()
            self.form_row(form, "x_variable", self.x)
            if index != 0:
                self.form_row(form, "y_variable", self.y)
            self.xr, self.x_start, self.x_end = self.range_row()
            self.yr, self.y_start, self.y_end = self.range_row()
            self.step = self.numeric(0.02, minimum=0.000000001)
            self.form_row(form, "x_range", self.xr)
            if index == 0:
                self.form_row(form, "step", self.step)
                self.x_start.valueChanged.connect(self.update_step)
                self.x_end.valueChanged.connect(self.update_step)
                self.update_step()
            else:
                self.form_row(form, "y_range", self.yr)
            self.assigns = CodeEditor(line_numbers=False)
            self.assigns.setFont(G.QFont("Consolas", 10))
            assignment_header = W.QHBoxLayout()
            right_layout.addLayout(assignment_header)
            self.add_label(assignment_header, "assigns")
            self.assigns.setLineWrapMode(W.QPlainTextEdit.WidgetWidth)
            self.assigns.setMinimumHeight(100)
            self.assigns.setMaximumHeight(125)
            right_layout.addWidget(self.assigns)
            self.x.currentIndexChanged.connect(self.analysis_changed)
            self.y.currentIndexChanged.connect(self.analysis_changed)
        else:
            top = W.QGridLayout()
            left_layout.addLayout(top)
            for i, (key, fn) in enumerate(
                [
                    ("import_data", self.import_data),
                    ("paste", self.paste_data),
                    (
                        "add_row",
                        lambda: self.grid.setRowCount(self.grid.rowCount() + 1),
                    ),
                    ("add_column", self.add_column),
                    ("delete_rows", lambda: self.grid.delete_selected("rows")),
                    ("delete_columns", lambda: self.grid.delete_selected("columns")),
                ]
            ):
                b = button(key, fn)
                self.bind(b, key)
                top.addWidget(b, i // 3, i % 3)
            self.add_label(left_layout, "table_hint")
            self.grid = DataGrid()
            left_layout.addWidget(self.grid, 3)
            self.grid.pasted.connect(self.update_columns)
            self.grid.zoomed.connect(
                lambda value: self.main.statusBar().showMessage(
                    f'{H.tr("ready")} · {value}%'
                )
            )
            form = W.QFormLayout()
            right_layout.addLayout(form)
            self.kind = ComboBox()
            self.form_row(form, "kind", self.kind)
            for key, pair in H.CHART_LABELS.items():
                self.kind.addItem(H.label(pair), key)
            self.kind.currentIndexChanged.connect(self.change_chart)
            self.x = ComboBox()
            self.form_row(form, "x_column", self.x)
            self.add_label(right_layout, "series")
            self.series = W.QListWidget()
            self.series.setSelectionMode(W.QAbstractItemView.MultiSelection)
            self.series.setMaximumHeight(105)
            right_layout.addWidget(self.series)
            self.bins = W.QSpinBox()
            self.bins.setRange(1, 1000)
            self.bins.setValue(6)
            self.form_row(form, "bins", self.bins)
            self.add_button(right_layout, "tutorial", self.tutorial)
            self.update_columns()
        self.show_legend = W.QCheckBox()
        self.show_legend.setChecked(self.parameters.get("show_legend", True))
        self.bind(self.show_legend, "show_legend")
        right_layout.addWidget(self.show_legend)
        self.grid_check = None
        if index in (0, 4):
            self.grid_check = W.QCheckBox()
            self.grid_check.setChecked(True)
            self.bind(self.grid_check, "grid")
            right_layout.addWidget(self.grid_check)
        settings_grid = W.QGridLayout()
        right_layout.addLayout(settings_grid)
        b = button("style", self.style_dialog)
        self.bind(b, "style")
        settings_grid.addWidget(b, 0, 0, 1, 2)
        for i, (key, fn) in enumerate(
            [("advanced", self.advanced_dialog), ("example", self.load_example)]
        ):
            b = button(key, fn)
            self.bind(b, key)
            settings_grid.addWidget(b, 1, i)
        right_layout.addSpacing(5)
        for key, fn in [
            ("draw", self.draw),
            ("save", self.save_code),
            ("open", self.open_code),
        ]:
            b = self.add_button(right_layout, key, fn)
            if key == "draw":
                b.setObjectName("primary")
            elif key == "save":
                self.save_button = b
        output_header = W.QHBoxLayout()
        left_layout.addLayout(output_header)
        output_label = self.add_label(output_header, "output")
        output_label.setWordWrap(False)
        output_label.setSizePolicy(W.QSizePolicy.Expanding, W.QSizePolicy.Preferred)
        output_header.setStretch(0, 1)
        self.output = CodeEditor()
        self.output.setReadOnly(True)
        self.output.setFont(G.QFont("Consolas", 10))
        self.edit_code = W.QCheckBox()
        self.bind(self.edit_code, "edit_code")
        self.edit_code.setToolTip(H.tr("edit_code_hint"))
        self.edit_code.toggled.connect(self.toggle_code_editing)
        output_header.addWidget(self.edit_code)
        self.add_wrap(output_header, self.output, "output")
        self.add_button(output_header, "copy_code", self.copy_code)
        left_layout.addWidget(self.output, 1)
        self.add_button(right_layout, "help", self.help_dialog)
        right_layout.addStretch()
        self.update_save_button()

    def add_wrap(self, layout, editor, name, checked=False):
        control = W.QCheckBox()
        self.bind(control, "wrap")
        control.toggled.connect(
            lambda enabled: editor.setLineWrapMode(
                W.QPlainTextEdit.WidgetWidth if enabled else W.QPlainTextEdit.NoWrap
            )
        )
        layout.addWidget(control)
        control.setChecked(checked)
        self.wrap_controls[name] = control
        return control

    def update_save_button(self):
        self.save_button.setText(H.tr("save_update" if self.code_path else "save_new"))

    def toggle_code_editing(self, checked):
        if self._restoring:
            return
        if checked:
            if not self.output.toPlainText().strip():
                try:
                    self.compile_code(force=True)
                except Exception:
                    self.output.setPlainText("from betu import *\n")
            self.output.setReadOnly(False)
            self.main.statusBar().showMessage(H.tr("manual_code"))
        else:
            try:
                self.restore_code(self.output.toPlainText(), self.code_path)
                self.main.statusBar().showMessage(H.tr("code_locked"))
            except Exception as exc:
                self.edit_code.blockSignals(True)
                self.edit_code.setChecked(True)
                self.edit_code.blockSignals(False)
                self.output.setReadOnly(False)
                if getattr(exc, "lineno", None):
                    self.output.mark_error(exc.lineno, str(exc))
                self.report_error(exc)

    def bind(self, widget, key):
        self.text_bindings.append((widget, key))
        widget.setText(H.tr(key))

    def add_label(self, layout, key):
        label = W.QLabel()
        label.setWordWrap(True)
        self.bind(label, key)
        layout.addWidget(label)
        return label

    def add_button(self, layout, key, fn):
        b = button(key, fn)
        self.bind(b, key)
        layout.addWidget(b)
        return b

    def form_row(self, form, key, widget):
        label = W.QLabel()
        self.bind(label, key)
        widget.setMinimumHeight(28)
        form.addRow(label, widget)

    def retranslate(self):
        for widget, key in self.text_bindings:
            widget.setText(H.tr(key))
        self.update_save_button()
        self.edit_code.setToolTip(H.tr("edit_code_hint"))
        if not self.is_data:
            self.editor.setPlaceholderText(H.label(H.FORMULA_PLACEHOLDER))
        else:
            for i, key in enumerate(H.CHART_LABELS):
                self.kind.setItemText(i, H.label(H.CHART_LABELS[key]))
            self.x.setItemText(0, H.tr("row_numbers"))

    def report_error(self, exc):
        if not self.is_data and getattr(exc, "lineno", None):
            self.editor.mark_error(exc.lineno, str(exc))
        self.main.statusBar().showMessage(str(exc))
        error(self, exc)

    def recognize(self):
        try:
            self.plan = parse_formulas(self.editor.toPlainText())
            self.assignment_memory.remember(self.assigns.toPlainText())
            self._syncing_axes = True
            for combo in (self.x, self.y):
                selected = combo.currentText()
                combo.clear()
                combo.addItems(self.plan.analysis_symbols)
                if selected in self.plan.analysis_symbols:
                    combo.setCurrentText(selected)
            if not self.x.currentText():
                raise ValueError(H.tr("no_analysis_symbols"))
            if self.y.currentText() == self.x.currentText() and self.y.count() > 1:
                self.y.setCurrentIndex(1)
            self._axis_selection = (self.x.currentText(), self.y.currentText())
            self.assigns.setPlainText(
                self.assignment_memory.text(
                    self.plan.analysis_symbols, self.active_axes()
                )
            )
            status = H.tr(
                "analysis_symbols",
                symbols=", ".join(self.plan.analysis_symbols),
                count=len(self.plan.intermediates),
            )
            self.main.statusBar().showMessage(status)
            if not self._restoring and not self.edit_code.isChecked():
                try:
                    self.compile_code()
                except ValueError:
                    self.output.setPlainText(
                        "from betu import *\n\n" + self.plan.source()
                    )
            return self.plan
        except Exception as exc:
            self.report_error(exc)
            return None
        finally:
            self._syncing_axes = False

    def active_axes(self):
        return [self.x.currentText()] + ([self.y.currentText()] if self.index else [])

    def analysis_changed(self):
        if self._syncing_axes or self._restoring or self.plan is None:
            return
        self._syncing_axes = True
        try:
            self.assignment_memory.remember(self.assigns.toPlainText())
            if self.index and self.x.currentText() == self.y.currentText():
                changed_x = self.sender() is self.x
                other = self.y if changed_x else self.x
                previous = self._axis_selection[0 if changed_x else 1]
                candidates = [
                    name
                    for name in self.plan.analysis_symbols
                    if name != self.x.currentText()
                ]
                if candidates:
                    other.setCurrentText(
                        previous if previous in candidates else candidates[0]
                    )
            self.assigns.setPlainText(
                self.assignment_memory.text(
                    self.plan.analysis_symbols, self.active_axes()
                )
            )
            self._axis_selection = (self.x.currentText(), self.y.currentText())
            self.main.statusBar().showMessage(H.tr("assignment_memory"))
        except Exception:
            self.x.setCurrentText(self._axis_selection[0])
            self.y.setCurrentText(self._axis_selection[1])
            self.main.statusBar().showMessage(H.tr("invalid_assignments"))
        finally:
            self._syncing_axes = False

    def numeric(self, value, minimum=-1e12):
        field = NumberInput()
        field.setDecimals(9)
        field.setRange(minimum, 1e12)
        field.setValue(value)
        field.setKeyboardTracking(False)
        return field

    def range_row(self):
        row = W.QWidget()
        layout = W.QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        start = self.numeric(0)
        end = self.numeric(2)
        for key, widget in [("start", start), ("end", end)]:
            label = W.QLabel()
            self.bind(label, key)
            layout.addWidget(label)
            layout.addWidget(widget, 1)
        return row, start, end

    def update_step(self):
        step = round((self.x_end.value() - self.x_start.value()) / 100, 6)
        self.step.setValue(max(0.000000001, step))

    def collect(self):
        parameters = deepcopy(self.parameters)
        parameters["show_legend"] = self.show_legend.isChecked()
        if "isgrid" in parameters:
            parameters["isgrid"] = (
                self.grid_check.isChecked() if self.grid_check else False
            )
        if self.is_data:
            data = self.grid.data()
            series = [i.text() for i in self.series.selectedItems()]
            if not series:
                raise ValueError(H.tr("table_empty"))
            parameters.update(
                x=self.x.currentData(),
                series=series,
                kind=self.kind.currentData(),
                bins=self.bins.value(),
            )
            return parameters, data
        plan = parse_formulas(self.editor.toPlainText())
        assigns = parse_assignments(self.assigns.toPlainText())
        self.assignment_memory.remember(self.assigns.toPlainText())
        assigns = {
            name: value
            for name, value in assigns.items()
            if name in plan.analysis_symbols and name not in self.active_axes()
        }
        parameters["assigns"] = assigns
        if self.index == 0:
            parameters.update(
                the_var=self.x.currentText(),
                ranges=[self.x_start.value(), self.x_end.value(), self.step.value()],
            )
        else:
            parameters.update(
                the_var_x=self.x.currentText(),
                start_end_x=[self.x_start.value(), self.x_end.value()],
                the_var_y=self.y.currentText(),
                start_end_y=[self.y_start.value(), self.y_end.value()],
            )
        chosen = [self.x.currentText()] + (
            [] if self.index == 0 else [self.y.currentText()]
        )
        if any(n not in plan.analysis_symbols for n in chosen) or len(
            set(chosen)
        ) != len(chosen):
            raise ValueError(H.tr("param_required", names=", ".join(plan.symbols)))
        for key in ("ranges", "start_end_x", "start_end_y"):
            if key in parameters:
                r = parameters[key]
                if r[0] >= r[1] or (key == "ranges" and r[2] <= 0):
                    raise ValueError(H.tr("invalid_value", name=key, value=r))
        # Bound integration variables belong in symbols but do not require numeric assignments.
        return parameters, None

    def compile_code(self, force=False):
        if not force and self.edit_code.isChecked():
            return self.output.toPlainText()
        parameters, data = self.collect()
        code = H.build_code(
            self.function,
            "" if self.is_data else self.editor.toPlainText(),
            parameters,
            self.advanced_code,
            data,
        )
        self.output.setPlainText(code)
        return code

    def style_dialog(self):
        from .style_editor import StyleDialog

        excluded = {
            "assigns",
            "expressions",
            "the_var",
            "ranges",
            "the_var_x",
            "the_var_y",
            "start_end_x",
            "start_end_y",
            "x",
            "series",
            "kind",
            "bins",
            "isgrid",
            "location",
            "ncol",
            "legendsize",
        }
        values = {k: v for k, v in self.parameters.items() if k not in excluded}
        values["show_legend"] = self.show_legend.isChecked()
        try:
            if self.is_data:
                names = [item.text() for item in self.series.selectedItems()]
                if self.kind.currentData() == "pie":
                    data = self.grid.data()
                    names = (
                        [str(v) for v in data[self.x.currentData()]]
                        if self.x.currentData()
                        else [str(i + 1) for i in range(self.grid.rowCount())]
                    )
            elif self.index == 2:
                names = (
                    getattr(self, "region_names", [])
                    if getattr(self, "region_source", None) == self.region_key()
                    else []
                )
            else:
                expressions = (
                    parse_formulas(self.editor.toPlainText()).expressions
                    if self.editor.toPlainText().strip()
                    else []
                )
                names = [
                    H.tr("region_number", number=i + 1) if self.index == 1 else name
                    for i, (name, expr) in enumerate(expressions)
                ]
        except Exception as exc:
            self.report_error(exc)
            return
        d = StyleDialog(
            self,
            values,
            names,
            self.function,
            self.kind.currentData() if self.is_data else None,
        )
        if d.exec_():
            self.parameters.update(d.values)
            self.show_legend.setChecked(d.values["show_legend"])

    def advanced_dialog(self):
        d = AdvancedDialog(self, self.advanced_code)
        if d.exec_():
            self.advanced_code = d.editor.toPlainText()

    def draw(self):
        try:
            code = self.compile_code()
        except Exception as exc:
            self.report_error(exc)
            return
        self.main.statusBar().showMessage(H.tr("working"))
        self.main.tabs.setEnabled(False)
        self.worker = PlotWorker(code, self)
        self.worker.result.connect(self.plot_ready)
        self.worker.failed.connect(self.plot_failed)
        self.worker.start()

    def plot_ready(self, figure):
        self.main.tabs.setEnabled(True)
        self.main.statusBar().showMessage(H.tr("complete"))
        if self.index == 2:
            self.region_names = [
                H.tr("region_number", number=i + 1)
                for i, _ in enumerate(
                    getattr(figure.axes[0], "_betu_region_handles", [])
                )
            ]
            self.region_source = self.region_key()
        self.preview = PlotDialog(self.main, figure)
        self.preview.exec_()

    def region_key(self):
        return (
            self.editor.toPlainText(),
            self.assigns.toPlainText(),
            self.x.currentText(),
            self.y.currentText(),
            self.x_start.value(),
            self.x_end.value(),
            self.y_start.value(),
            self.y_end.value(),
            self.parameters.get("precision"),
            self.parameters.get("dropout"),
        )

    def plot_failed(self, message):
        self.main.tabs.setEnabled(True)
        self.main.statusBar().showMessage(H.tr("error"))
        error(self, message)

    def copy_code(self):
        try:
            W.QApplication.clipboard().setText(self.compile_code())
            self.main.statusBar().showMessage(H.tr("code_copied"))
        except Exception as exc:
            self.report_error(exc)

    def save_code(self):
        try:
            code = self.compile_code()
            path = self.code_path
            if not path:
                path, _ = W.QFileDialog.getSaveFileName(
                    self, H.tr("save"), "figure.py", H.tr("code_filter")
                )
            if path:
                path = str(path) if Path(path).suffix else str(path) + ".py"
                Path(path).write_text(code, encoding="utf-8")
                self.code_path = Path(path)
                self.output.document().setModified(False)
                self.update_save_button()
                self.main.statusBar().showMessage(H.tr("saved"))
        except Exception as exc:
            error(self, exc)

    def open_code(self):
        path, _ = W.QFileDialog.getOpenFileName(
            self, H.tr("open"), "", H.tr("code_filter")
        )
        if path:
            try:
                code = Path(path).read_text(encoding="utf-8-sig")
                function, _, _, _ = read_plot_code(code)
                index = H.TAB_FUNCTIONS.index(function)
                self.main.tabs.setCurrentIndex(index)
                self.main.pages[index].restore_code(code, path)
            except Exception as exc:
                error(self, exc)

    def restore_code(self, code, source_path=None):
        read_plot_code(code)
        self._restoring = True
        try:
            self._restore_code(code)
            self.code_path = Path(source_path) if source_path else None
            self.edit_code.setChecked(False)
            self.output.setReadOnly(True)
            self.output.document().setModified(False)
            self.update_save_button()
        finally:
            self._restoring = False

    def _restore_code(self, code):
        function, formula, parameters, advanced = read_plot_code(code)
        if function != self.function:
            raise ValueError(H.tr("unsupported_code"))
        defaults = H.default_parameters(function)
        self.parameters = {
            key: parameters.get(key, value) for key, value in defaults.items()
        }
        self.advanced_code = advanced
        if self.is_data:
            data = parameters["data"]
            self.grid.load(list(data), list(zip(*data.values())))
            self.kind.setCurrentIndex(
                max(0, self.kind.findData(parameters.get("kind", "line")))
            )
            self.x.setCurrentIndex(max(0, self.x.findData(parameters.get("x"))))
            for i in range(self.series.count()):
                self.series.item(i).setSelected(
                    self.series.item(i).text() in parameters.get("series", [])
                )
            self.bins.setValue(parameters.get("bins", 6))
        else:
            self.assignment_memory = AssignmentMemory()
            assigns = parameters.get("assigns", {})
            self.assignment_memory.values.update(
                {str(k): v for k, v in assigns.items()}
            )
            self.assigns.clear()
            self.editor.setPlainText(formula)
            self.recognize()
            if self.index == 0:
                self.x.setCurrentText(parameters["the_var"])
                r = parameters["ranges"]
                self.x_start.setValue(r[0])
                self.x_end.setValue(r[1])
                self.step.setValue(r[2])
            else:
                self.x.setCurrentText(parameters["the_var_x"])
                self.y.setCurrentText(parameters["the_var_y"])
                self.x_start.setValue(parameters["start_end_x"][0])
                self.x_end.setValue(parameters["start_end_x"][1])
                self.y_start.setValue(parameters["start_end_y"][0])
                self.y_end.setValue(parameters["start_end_y"][1])
            self._axis_selection = (self.x.currentText(), self.y.currentText())
            self.assigns.setPlainText(
                self.assignment_memory.text(
                    self.plan.analysis_symbols, self.active_axes()
                )
            )
        self.show_legend.setChecked(parameters.get("show_legend", self.index != 1))
        if self.grid_check:
            self.grid_check.setChecked(parameters.get("isgrid", True))
        self.output.setPlainText(code)
        self.main.statusBar().showMessage(H.tr("loaded"))

    def load_example(self, checked=False, confirm=True):
        populated = (
            bool(self.editor.toPlainText())
            if not self.is_data
            else self.grid.item(0, 0) is not None
        )
        if (
            confirm
            and populated
            and W.QMessageBox.question(
                self,
                H.tr("example"),
                H.tr("overwrite"),
                W.QMessageBox.Yes | W.QMessageBox.No,
            )
            != W.QMessageBox.Yes
        ):
            return
        name = "data_" + self.kind.currentData() if self.is_data else self.function
        self.restore_code(H.example_code(name))

    def update_columns(self):
        selected = self.x.currentData()
        names = [
            self.grid.horizontalHeaderItem(j).text()
            for j in range(self.grid.columnCount())
            if self.grid.horizontalHeaderItem(j)
        ]
        series = [i.text() for i in self.series.selectedItems()]
        self.x.clear()
        self.x.addItem(H.tr("row_numbers"), None)
        for name in names:
            self.x.addItem(name, name)
        self.x.setCurrentIndex(max(0, self.x.findData(selected)))
        self.series.clear()
        self.series.addItems(names)
        for i in range(self.series.count()):
            self.series.item(i).setSelected(self.series.item(i).text() in series)

    def change_chart(self):
        self.x.setEnabled(self.kind.currentData() != "hist")
        self.bins.setEnabled(self.kind.currentData() == "hist")

    def paste_data(self):
        try:
            if self.grid.paste(replace=True):
                self.table_imported()
        except Exception as exc:
            error(self, exc)

    def table_imported(self):
        multiple_columns = self.grid.columnCount() > 1
        self.x.setCurrentIndex(1 if multiple_columns else 0)
        for i in range(self.series.count()):
            self.series.item(i).setSelected(i > 0 or not multiple_columns)
        self.main.statusBar().showMessage(
            H.tr(
                "table_imported",
                rows=self.grid.rowCount(),
                columns=self.grid.columnCount(),
            )
        )

    def add_column(self):
        col = self.grid.columnCount()
        self.grid.setColumnCount(col + 1)
        self.grid.setHorizontalHeaderItem(col, W.QTableWidgetItem(str(col + 1)))
        self.update_columns()

    def import_data(self):
        from .table import read_table, excel_sheets

        path, _ = W.QFileDialog.getOpenFileName(
            self, H.tr("import_data"), "", H.tr("data_filter")
        )
        if not path:
            return
        try:
            sheet = None
            if Path(path).suffix.lower() in (".xlsx", ".xlsm", ".xls"):
                sheets = excel_sheets(path)
                if len(sheets) > 1:
                    sheet, ok = W.QInputDialog.getItem(
                        self, H.tr("sheet"), H.tr("sheet"), sheets, 0, False
                    )
                    if not ok:
                        return
            _, rows = read_table(path, sheet, header=False)
            if self.grid.import_rows(rows):
                self.table_imported()
        except Exception as exc:
            error(self, exc)

    def tutorial(self):
        d = Dialog(self, "tutorial")
        d.resize(700, 500)
        layout = W.QVBoxLayout(d)
        text = HelpBrowser()
        kind = self.kind.currentData()
        text.set_help(
            H.label(H.CHART_HELP_TEMPLATE).format(
                name=H.label(H.CHART_LABELS[kind]),
                guide=H.label(H.CHART_GUIDES[kind]),
                kind=kind,
            )
        )
        layout.addWidget(text)
        layout.addWidget(
            button("example", lambda: (self.load_example(confirm=False), d.accept()))
        )
        layout.addWidget(button("close", d.accept))
        d.exec_()

    def help_dialog(self):
        d = Dialog(self, "help")
        d.resize(850, 650)
        layout = W.QVBoxLayout(d)
        text = HelpBrowser()
        text.set_help(H.label(H.HELP_HTML))
        layout.addWidget(text)
        layout.addWidget(button("close", d.accept))
        d.exec_()

    def symbols_dialog(self):
        if getattr(self, "symbol_panel", None) and self.symbol_panel.isVisible():
            self.symbol_panel.raise_()
            return
        d = Dialog(self, "symbols")
        self.symbol_panel = d
        d.setWindowModality(C.Qt.NonModal)
        d.setWindowFlag(C.Qt.Tool, True)
        d.setWindowFlag(C.Qt.WindowStaysOnTopHint, True)
        d.resize(440, 380)
        d.setStyleSheet(H.SYMBOL_STYLE)
        outer = W.QVBoxLayout(d)
        scroll = W.QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)
        body = W.QWidget()
        grid = W.QGridLayout(body)
        scroll.setWidget(body)
        grid.setHorizontalSpacing(3)
        grid.setVerticalSpacing(3)
        for i, (title, value) in enumerate(H.SYMBOL_BUTTONS):
            b = W.QPushButton(title)
            b.setToolTip(value)
            b.clicked.connect(lambda _, v=value: self.editor.insert_symbol(v))
            grid.addWidget(b, i // 9, i % 9)
        outer.addWidget(button("close", d.accept))
        d.show()

    def latex_dialog(self):
        from .latex_input import convert_formula

        d = Dialog(self, "latex")
        d.resize(800, 570)
        layout = W.QVBoxLayout(d)
        mode = ComboBox()
        for title, value, hint in H.CONVERSION_MODES:
            mode.addItem(H.label(title), value)
        layout.addWidget(mode)
        hint = W.QLabel()
        hint.setWordWrap(True)
        mode.currentIndexChanged.connect(
            lambda index: hint.setText(H.tr(H.CONVERSION_MODES[index][2]))
        )
        hint.setText(H.tr(H.CONVERSION_MODES[0][2]))
        layout.addWidget(hint)
        entry = CodeEditor()
        output = CodeEditor()
        for key, editor in [("latex_input", entry), ("latex_output", output)]:
            row = W.QHBoxLayout()
            row.addWidget(W.QLabel(H.tr(key)))
            row.addStretch()
            row.addWidget(wrap_checkbox(editor, d))
            layout.addLayout(row)
            layout.addWidget(editor, 1)
        output.setReadOnly(True)
        verify = W.QLabel(H.tr("latex_verify"))
        verify.setWordWrap(True)
        layout.addWidget(verify)

        def convert():
            try:
                output.setPlainText(
                    convert_formula(entry.toPlainText(), mode.currentData())
                )
            except Exception as exc:
                error(d, exc)

        bottom = W.QHBoxLayout()
        layout.addLayout(bottom)
        bottom.addWidget(button("convert", convert))
        bottom.addWidget(
            button(
                "copy", lambda: W.QApplication.clipboard().setText(output.toPlainText())
            )
        )
        bottom.addWidget(button("close", d.accept))
        d.exec_()


class MainWindow(W.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1180, 740)
        self.setMinimumSize(900, 600)
        area = W.QApplication.primaryScreen().availableGeometry()
        self.resize(min(1180, area.width() - 30), min(740, area.height() - 50))
        central = W.QWidget()
        self.setCentralWidget(central)
        layout = W.QVBoxLayout(central)
        layout.setContentsMargins(14, 10, 14, 6)
        head = W.QHBoxLayout()
        layout.addLayout(head)
        self.brand = W.QLabel()
        self.brand.setObjectName("brand")
        head.addWidget(self.brand)
        slogan = W.QLabel(H.tr("slogan"))
        slogan.setObjectName("slogan")
        head.addWidget(slogan)
        head.addStretch()
        self.language = ComboBox()
        self.language.setObjectName("languageChoice")
        self.language.setMinimumWidth(138)
        self.language.setSizeAdjustPolicy(W.QComboBox.AdjustToContents)
        self.language.setMaxVisibleItems(2)
        self.language.addItem("简体中文", "zh")
        self.language.addItem("English", "en")
        for index in range(self.language.count()):
            self.language.setItemData(index, C.QSize(138, 34), C.Qt.SizeHintRole)
        self.language.setCurrentIndex(0 if H.LANGUAGE == "zh" else 1)
        head.addWidget(self.language)
        self.about_button = button("about", self.about_dialog)
        head.addWidget(self.about_button)
        self.tabs = W.QTabWidget()
        layout.addWidget(self.tabs, 1)
        self.pages = []
        for index in range(5):
            page = PlotTab(self, index)
            self.pages.append(page)
            self.tabs.addTab(page, H.tr("tabs")[index])
        self.save_action = W.QAction(self)
        self.save_action.setShortcut(G.QKeySequence.Save)
        self.save_action.triggered.connect(
            lambda: self.pages[self.tabs.currentIndex()].save_code()
        )
        self.addAction(self.save_action)
        self.tabs.setCurrentIndex(0)
        self.statusBar().showMessage(H.tr("ready"))
        self.language.currentIndexChanged.connect(self.change_language)
        self.change_language()

    def change_language(self):
        H.set_language(self.language.currentData())
        self.setWindowTitle(H.tr("title"))
        self.brand.setText(H.tr("brand"))
        self.about_button.setText(H.tr("about"))
        self.language.setToolTip(H.tr("language"))
        for index, page in enumerate(self.pages):
            self.tabs.setTabText(index, H.tr("tabs")[index])
            page.retranslate()
        self.statusBar().showMessage(H.tr("ready"))

    def closeEvent(self, event):
        if any(getattr(p, "worker", None) and p.worker.isRunning() for p in self.pages):
            event.ignore()
            return
        super().closeEvent(event)

    def about_dialog(self):
        d = Dialog(self, "about")
        d.resize(500, 420)
        layout = W.QVBoxLayout(d)
        text = HelpBrowser()
        text.set_help(H.label(H.ABOUT_HTML))
        layout.addWidget(text)
        layout.addWidget(button("close", d.accept))
        d.exec_()


def create_application():
    W.QApplication.setAttribute(C.Qt.AA_EnableHighDpiScaling, True)
    W.QApplication.setAttribute(C.Qt.AA_UseHighDpiPixmaps, True)
    app = W.QApplication.instance() or W.QApplication(sys.argv)
    app.setWindowIcon(G.QIcon(str(Path(__file__).parent / "assets" / "betu.png")))
    app.setStyle("Fusion")
    app.setFont(
        G.QFont("PingFang SC" if sys.platform == "darwin" else "Microsoft YaHei UI", 9)
    )
    app.setStyleSheet(H.STYLE_SHEET)
    return app


def makefig():
    import matplotlib.pyplot as plt

    plt.switch_backend("Agg")
    app = create_application()
    window = MainWindow()
    window.show()
    C.QTimer.singleShot(0, window.showNormal)
    window.raise_()
    window.activateWindow()
    return app.exec_()


if __name__ == "__main__":
    makefig()
