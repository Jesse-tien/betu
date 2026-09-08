"""公共格式、逐系列样式和图例的统一编辑窗口。"""

import ast
from copy import deepcopy
from PyQt5 import QtCore as C, QtGui as G, QtWidgets as W
from matplotlib.colors import to_rgba
from . import helpers as H
from .qt_widgets import Dialog, NumberInput, ComboBox, button, error


def color_icon(value):
    pixmap = G.QPixmap(24, 18)
    pixmap.fill(C.Qt.transparent)
    if value not in (None, "auto"):
        r, g, b, a = to_rgba(value)
        painter = G.QPainter(pixmap)
        painter.setPen(G.QColor("#8d99a4"))
        painter.setBrush(G.QColor.fromRgbF(r, g, b, a))
        painter.drawRect(1, 1, 21, 15)
        painter.end()
    return G.QIcon(pixmap)


class ValueField(W.QWidget):
    def __init__(self, name, value, parent=None):
        super().__init__(parent)
        self.name, self.original = name, value
        layout = W.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.controls = []
        if name in ("figsize", "pattern_moves", "x_lim", "y_lim", "z_lim"):
            if name in ("x_lim", "y_lim", "z_lim"):
                self.auto = W.QCheckBox(H.tr("auto_option"))
                self.auto.setChecked(value is None)
                layout.addWidget(self.auto)
            for index, number in enumerate(value or [0, 1]):
                field = self.spin(number, 0.1 if name == "figsize" else -1e12)
                self.controls.append(field)
                if name == "figsize":
                    layout.addWidget(
                        W.QLabel(H.tr("width" if index == 0 else "height"))
                    )
                layout.addWidget(field)
            if name == "figsize":
                for field, key in zip(self.controls, ["figure_width", "figure_height"]):
                    field.setToolTip(H.tr(key))
            elif name != "pattern_moves":
                self.auto.toggled.connect(self.toggle_auto)
                self.toggle_auto(self.auto.isChecked())
        elif isinstance(value, bool):
            self.field = W.QCheckBox()
            self.field.setChecked(value)
        elif name == "numbers":
            self.field = ComboBox()
            for pair, key in H.STYLE_NUMBER_CHOICES:
                self.field.addItem(H.label(pair), key)
            self.field.setCurrentIndex(max(0, self.field.findData(value)))
        elif name in ("xlabelsize", "ylabelsize", "zlabelsize"):
            self.field = ComboBox()
            self.field.setEditable(True)
            self.field.addItem(H.tr("follow_font_size"), "auto")
            for size in (8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32):
                self.field.addItem(str(size), size)
            index = self.field.findData(value)
            if index >= 0:
                self.field.setCurrentIndex(index)
            else:
                self.field.setEditText(str(value))
        elif name in ("edgecolor", "pattern_colors"):
            self.field = ComboBox()
            self.field.setEditable(True)
            self.field.addItem(
                H.tr("none_option") if name == "edgecolor" else H.tr("auto_option"),
                None if name == "edgecolor" else "auto",
            )
            for color in H.STYLE_COLOR_CHOICES:
                self.field.addItem(color_icon(color), color, color)
            index = self.field.findData(value)
            if index >= 0:
                self.field.setCurrentIndex(index)
            else:
                self.field.setEditText(str(value))
            choose = button("pick_color", self.choose_color)
            layout.addWidget(choose)
        elif isinstance(value, (int, float)):
            minimum = (
                0.1
                if name in ("fsize", "precision", "density", "fontsize")
                else (
                    0
                    if name
                    in (
                        "ncol",
                        "borderpad",
                        "labelspacing",
                        "handlelength",
                        "handletextpad",
                        "columnspacing",
                        "linewidth",
                        "linewidths",
                        "markersize",
                        "color_alpha",
                        "dropout",
                    )
                    else -1e12
                )
            )
            self.field = self.spin(value, minimum)
            if name in ("precision", "density", "ncol"):
                self.field.setDecimals(0)
                self.field.setMinimum(1)
            if name in ("color_alpha", "dropout"):
                self.field.setMaximum(1)
            if name == "dropout":
                self.field.setDecimals(6)
                self.field.setSingleStep(0.001)
                self.field.setValue(value)
                self.setToolTip(H.tr("dropout_hint"))
        else:
            self.field = W.QLineEdit(
                ""
                if value is None
                else value if isinstance(value, str) else repr(value)
            )
            if name == "title":
                self.field.setPlaceholderText(H.tr("title_hint"))
            if name == "save_dir":
                self.field.setPlaceholderText(H.tr("no_auto_save"))
                layout.addWidget(button("browse", self.browse))
                layout.addWidget(button("clear", self.field.clear))
        if hasattr(self, "field"):
            layout.addWidget(self.field)

    def choose_color(self):
        color = W.QColorDialog.getColor(parent=self, title=H.tr("pick_color"))
        if color.isValid():
            self.field.addItem(color_icon(color.name()), color.name(), color.name())
            self.field.setCurrentIndex(self.field.count() - 1)

    def browse(self):
        from .advanced import documents_dir

        path, _ = W.QFileDialog.getSaveFileName(
            self,
            H.tr("save_picture"),
            str(documents_dir() / "figure.svg"),
            H.tr("image_filter"),
        )
        if path:
            self.field.setText(path)

    def spin(self, value, minimum):
        field = NumberInput()
        field.setLocale(C.QLocale.c())
        field.setDecimals(4)
        field.setRange(minimum, 1e12)
        field.setValue(value)
        field.setKeyboardTracking(False)
        return field

    def toggle_auto(self, checked):
        for field in self.controls:
            field.setEnabled(not checked)

    def value(self):
        if self.controls:
            if hasattr(self, "auto") and self.auto.isChecked():
                return None
            values = [field.value() for field in self.controls]
            if self.name in ("x_lim", "y_lim", "z_lim") and values[0] >= values[1]:
                raise ValueError(
                    H.tr(
                        "invalid_value", name=H.parameter_label(self.name), value=values
                    )
                )
            return values
        if isinstance(self.field, W.QCheckBox):
            return self.field.isChecked()
        if isinstance(self.field, W.QComboBox):
            index = self.field.currentIndex()
            if index >= 0 and self.field.currentText() == self.field.itemText(index):
                return self.field.currentData()
            raw = self.field.currentText().strip()
            if self.name.endswith("size"):
                value = float(raw)
                if value <= 0:
                    raise ValueError(H.tr("invalid_value", name=self.name, value=raw))
                return value
            to_rgba(raw)
            return raw
        if isinstance(self.field, W.QDoubleSpinBox):
            value = self.field.value()
            return (
                int(value) if self.name in ("ncol", "precision", "density") else value
            )
        raw = self.field.text().strip()
        if self.name in ("title", "x_name", "y_name", "z_name", "save_dir", "prefix"):
            return raw if raw or self.name in ("title", "prefix") else None
        if self.name in ("xlabelsize", "ylabelsize", "zlabelsize"):
            if raw == "auto":
                return raw
            value = float(raw)
            if value <= 0:
                raise ValueError(H.tr("invalid_value", name=self.name, value=raw))
            return value
        try:
            return ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return raw or None


class StyleDialog(Dialog):
    def __init__(self, parent, values, names, function, kind=None):
        super().__init__(parent, "style")
        self.resize(760, 600)
        self.values = deepcopy(values)
        if function == "draw_detail_area":
            self.values.pop("texts", None)
        self.names = list(names)
        self.function, self.kind = function, kind
        defaults = H.default_parameters(function)
        self.defaults = {k: deepcopy(defaults.get(k, v)) for k, v in self.values.items()}
        layout = W.QVBoxLayout(self)
        self.tabs = W.QTabWidget()
        layout.addWidget(self.tabs, 1)
        self.build_pages()
        bottom = W.QHBoxLayout()
        layout.addLayout(bottom)
        bottom.addWidget(button("reset", self.reset))
        bottom.addStretch()
        bottom.addWidget(button("cancel", self.reject))
        ok = button("ok", self.save)
        ok.setDefault(True)
        bottom.addWidget(ok)

    def page(self, key):
        scroll = W.QScrollArea()
        scroll.setWidgetResizable(True)
        body = W.QWidget()
        form = W.QFormLayout(body)
        form.setSpacing(10)
        scroll.setWidget(body)
        self.tabs.addTab(scroll, H.tr(key))
        return form

    def build_pages(self):
        while self.tabs.count():
            page = self.tabs.widget(0)
            self.tabs.removeTab(0)
            page.deleteLater()
        self.common_fields = {}
        self.series_fields = {}
        self.series_index = 0
        common = self.page("style_common")
        series = self.page("style_series")
        legend = self.page("style_legend")
        extra = self.page("style_more")
        self.series_keys = [
            key
            for key in H.STYLE_SERIES_KEYS
            if key in self.values
            and (
                isinstance(self.values[key], list)
                or key in ("texts", "pattern_colors", "pattern_moves")
            )
        ]
        if self.kind and self.kind not in ("line", "scatter"):
            self.series_keys = [key for key in self.series_keys if key == "colors"]
        elif self.kind == "scatter":
            self.series_keys = [
                key
                for key in self.series_keys
                if key not in ("linestyles", "linewidth")
            ]
        for key, value in self.values.items():
            if (
                key in H.STYLE_SERIES_KEYS
                and isinstance(value, list)
                or key
                in (
                    "texts",
                    "pattern_colors",
                    "pattern_moves",
                    "legend_options",
                    "show_legend",
                )
            ):
                continue
            field = ValueField(key, value)
            self.common_fields[key] = field
            (common if key in H.STYLE_COMMON_KEYS else extra).addRow(
                H.parameter_label(key), field
            )
        hint = W.QLabel(
            H.tr(
                "style_hint"
                if self.names
                else (
                    "style_regions_pending"
                    if self.function == "draw_detail_area"
                    else "style_empty"
                )
            )
        )
        hint.setWordWrap(True)
        series.addRow(hint)
        self.selector = ComboBox()
        self.selector.addItems(self.names)
        self.selector.setEnabled(bool(self.names))
        series.addRow(H.tr("style_select"), self.selector)
        for key in self.series_keys if self.names else []:
            field = self.series_field(key, self.item_value(key, 0))
            self.series_fields[key] = field
            series.addRow(H.parameter_label(key), field)
        self.selector.currentIndexChanged.connect(self.switch_series)
        self.legend_enabled = W.QCheckBox(H.tr("show_legend"))
        self.legend_enabled.setChecked(self.values.get("show_legend", True))
        legend.addRow(self.legend_enabled)
        self.legend_fields = {}
        for key, value in self.values["legend_options"].items():
            if key == "loc":
                field = ComboBox()
                for name, pair in H.LOC_LABELS.items():
                    field.addItem(H.label(pair), name)
                field.setCurrentIndex(max(0, field.findData(value)))
            else:
                field = ValueField(key, value)
            self.legend_fields[key] = field
            legend.addRow(H.label(H.LEGEND_LABELS[key]), field)
        self.legend_enabled.toggled.connect(
            lambda checked: [
                field.setEnabled(checked) for field in self.legend_fields.values()
            ]
        )
        for field in self.legend_fields.values():
            field.setEnabled(self.legend_enabled.isChecked())

    def item_value(self, key, index):
        values = self.values[key]
        if key == "texts":
            return (values[index] or "") if values and index < len(values) else ""
        if key == "pattern_colors" and values == "auto":
            return "auto"
        if key == "pattern_moves" and values == "auto":
            return [0, 0]
        if not values:
            return None
        return values[index % len(values)]

    def series_field(self, key, value):
        if key in ("linewidth", "markersize", "pattern_colors", "pattern_moves"):
            return ValueField(key, value)
        if key == "texts":
            field = W.QLineEdit(value or "")
            field.setPlaceholderText(H.tr("region_text_hint"))
            return field
        if key == "colors":
            row = W.QWidget()
            layout = W.QHBoxLayout(row)
            layout.setContentsMargins(0, 0, 0, 0)
            row.entry = ComboBox()
            row.entry.setEditable(True)
            for color in H.STYLE_COLOR_CHOICES:
                row.entry.addItem(color_icon(color), color, color)
            row.entry.setCurrentText(value)
            row.swatch = W.QPushButton(H.tr("pick_color"))
            row.swatch.clicked.connect(lambda: self.pick_color(row))
            row.entry.currentTextChanged.connect(
                lambda text: self.color_swatch(row, text)
            )
            layout.addWidget(row.entry, 1)
            layout.addWidget(row.swatch)
            self.color_swatch(row, value)
            return row
        field = ComboBox()
        if key == "linestyles":
            field.setIconSize(C.QSize(48, 22))
            for pair, data in H.STYLE_LINE_CHOICES:
                field.addItem(self.line_icon(data), H.label(pair), data)
            for data in self.values[key]:
                if field.findData(data) < 0:
                    field.addItem(
                        self.line_icon(data),
                        H.tr("line_style_custom", number=field.count() - 3),
                        data,
                    )
        elif key == "markers":
            for data in H.STYLE_MARKER_CHOICES:
                field.addItem(
                    self.marker_icon(data), H.label(H.MARKER_NAMES[data]), data
                )
        elif key == "patterns":
            field.setIconSize(C.QSize(56, 26))
            for pair, data in H.STYLE_PATTERN_CHOICES:
                field.addItem(self.pattern_icon(data), H.label(pair), data)
            for data in self.values[key]:
                if field.findData(data) < 0:
                    field.addItem(self.pattern_icon(data), H.tr("pattern_custom", pattern=data), data)
        if field.findData(value) < 0:
            field.addItem(str(value), value)
        field.setCurrentIndex(max(0, field.findData(value)))
        return field

    def pattern_icon(self, pattern):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.patches import Rectangle

        fig = Figure(figsize=(0.56, 0.26), dpi=100, facecolor="none")
        fig.add_artist(Rectangle((0.02, 0.04), 0.96, 0.92, transform=fig.transFigure,
                                 facecolor="#eef3f7", edgecolor="#344655",
                                 linewidth=0.7, hatch=pattern))
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        pixels = canvas.buffer_rgba()
        picture = G.QImage(pixels, 56, 26, 56 * 4, G.QImage.Format_RGBA8888).copy()
        return G.QIcon(G.QPixmap.fromImage(picture))

    def line_icon(self, style):
        pixmap = G.QPixmap(48, 22)
        pixmap.fill(C.Qt.transparent)
        painter = G.QPainter(pixmap)
        painter.setRenderHint(G.QPainter.Antialiasing)
        pen = G.QPen(G.QColor("#137c98"), 1.6)
        if isinstance(style, (tuple, list)):
            offset, dashes = style
            if dashes:
                pen.setDashPattern([float(n) for n in dashes])
                pen.setDashOffset(float(offset))
        else:
            pen.setStyle(
                {
                    "solid": C.Qt.SolidLine,
                    "-": C.Qt.SolidLine,
                    "dashed": C.Qt.DashLine,
                    "--": C.Qt.DashLine,
                    "dotted": C.Qt.DotLine,
                    ":": C.Qt.DotLine,
                    "dashdot": C.Qt.DashDotLine,
                    "-.": C.Qt.DashDotLine,
                }.get(style, C.Qt.SolidLine)
            )
        painter.setPen(pen)
        painter.drawLine(2, 11, 46, 11)
        painter.end()
        return G.QIcon(pixmap)

    def marker_icon(self, marker):
        from matplotlib.markers import MarkerStyle
        from matplotlib.path import Path as MplPath

        pixmap = G.QPixmap(28, 24)
        pixmap.fill(C.Qt.transparent)
        if marker is None:
            return G.QIcon(pixmap)
        style = MarkerStyle(marker)
        path = style.get_path().transformed(style.get_transform())
        drawing = G.QPainterPath()
        for vertices, code in path.iter_segments(curves=False):
            if code == MplPath.CLOSEPOLY:
                drawing.closeSubpath()
            else:
                point = C.QPointF(14 + vertices[0] * 18, 12 - vertices[1] * 18)
                if code == MplPath.MOVETO:
                    drawing.moveTo(point)
                else:
                    drawing.lineTo(point)
        painter = G.QPainter(pixmap)
        painter.setRenderHint(G.QPainter.Antialiasing)
        painter.setPen(G.QPen(G.QColor("#137c98"), 1.4))
        painter.setBrush(G.QColor("#137c98") if style.is_filled() else C.Qt.NoBrush)
        painter.drawPath(drawing)
        painter.end()
        return G.QIcon(pixmap)

    def color_swatch(self, row, text):
        try:
            r, g, b, a = to_rgba(text)
            color = G.QColor.fromRgbF(r, g, b, a)
            row.swatch.setIcon(self.color_icon(color))
        except ValueError:
            row.swatch.setIcon(G.QIcon())

    def color_icon(self, color):
        pixmap = G.QPixmap(22, 18)
        pixmap.fill(color)
        return G.QIcon(pixmap)

    def pick_color(self, row):
        try:
            r, g, b, a = to_rgba(row.entry.currentText())
            initial = G.QColor.fromRgbF(r, g, b, a)
        except ValueError:
            initial = G.QColor("white")
        color = W.QColorDialog.getColor(initial, self, H.tr("pick_color"))
        if color.isValid():
            row.entry.setCurrentText(color.name())

    def commit_series(self):
        changes = {}
        for key, field in self.series_fields.items():
            if key == "colors":
                value = field.entry.currentText()
                to_rgba(value)
            elif isinstance(field, ValueField):
                value = field.value()
            elif isinstance(field, W.QComboBox):
                value = field.currentData()
            else:
                value = field.text()
            if key == "texts":
                value = value.strip()
            if value == self.item_value(key, self.series_index):
                continue
            count = max(len(self.names), len(self.values[key]) if isinstance(self.values[key], list) else 0)
            values = [self.item_value(key, i) for i in range(count)]
            values[self.series_index] = value
            if key == "texts":
                values = [text or None for text in values]
                if not any(values):
                    values = None
            changes[key] = values
        self.values.update(changes)

    def switch_series(self, index):
        try:
            self.commit_series()
        except Exception as exc:
            self.selector.blockSignals(True)
            self.selector.setCurrentIndex(self.series_index)
            self.selector.blockSignals(False)
            error(self, exc)
            return
        self.series_index = index
        for key, field in self.series_fields.items():
            value = self.item_value(key, index)
            if key == "colors":
                field.entry.setCurrentText(value)
            elif isinstance(field, ValueField):
                if field.controls:
                    for control, number in zip(field.controls, value):
                        control.setValue(number)
                elif isinstance(field.field, W.QComboBox):
                    index = field.field.findData(value)
                    if index < 0:
                        field.field.addItem(str(value), value)
                        index = field.field.count() - 1
                    field.field.setCurrentIndex(index)
                else:
                    field.field.setValue(value)
            elif isinstance(field, W.QComboBox):
                field.setCurrentIndex(max(0, field.findData(value)))
            else:
                field.setText(str(value))

    def reset(self):
        index = self.tabs.currentIndex()
        self.values = deepcopy(self.defaults)
        self.build_pages()
        self.tabs.setCurrentIndex(index)

    def save(self):
        try:
            from ._plotting import validate_legend

            self.commit_series()
            values = {key: field.value() for key, field in self.common_fields.items()}
            options = {
                key: (
                    field.currentData()
                    if isinstance(field, W.QComboBox)
                    else field.value()
                )
                for key, field in self.legend_fields.items()
            }
            values["legend_options"] = validate_legend(options)
            values["show_legend"] = self.legend_enabled.isChecked()
            if values.get("edgecolor") is not None:
                to_rgba(values["edgecolor"])
            self.values.update(values)
            self.accept()
        except Exception as exc:
            error(self, exc)
