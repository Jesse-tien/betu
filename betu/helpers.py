"""中英文资源。键名对应界面控件、对话框和状态消息；修改文案无需改 UI。"""

LANGUAGE = "zh"

# 编辑器工具条、文件保存和参数切换的界面文案。
EDITOR_TEXT = {
    "wrap": ("自动换行", "Word wrap"),
    "edit_code": ("编辑代码", "Edit code"),
    "edit_code_hint": (
        "勾选后，出图、复制和保存使用下方编辑的代码；取消勾选会按代码恢复界面控件。",
        "When checked, Plot, Copy and Save use the code below. Uncheck to restore the controls from your code.",
    ),
    "save_new": ("保存代码(&S)...", "Save Code (&S)..."),
    "save_update": ("更新代码(&S)", "Update Code (&S)"),
    "manual_code": (
        "代码编辑已解锁；Ctrl+S 保存当前代码。",
        "Code editing unlocked. Ctrl+S saves the current code.",
    ),
    "code_locked": (
        "代码已锁定，界面控件已同步。",
        "Code locked; controls synchronized.",
    ),
    "invalid_assignments": (
        "参数赋值请写成 a=2, b=0.5，每项用逗号或换行分隔。",
        "Use a=2, b=0.5, separated by commas or new lines.",
    ),
    "assignment_memory": (
        "分析参数已切换，固定赋值已更新；之前的值会临时保留。",
        "Analysis parameters changed; fixed assignments updated and previous values retained.",
    ),
    "analysis_symbols": (
        "可分析参数：{symbols}；中间变量 {count} 个。",
        "Analysis parameters: {symbols}; {count} intermediates.",
    ),
    "no_analysis_symbols": (
        "表达式中没有可用于坐标分析的自由参数。",
        "No free parameter is available for axis analysis.",
    ),
    "latex_hint_mathematica": (
        "Mathematica：选定公式后右键，选择“复制为 → LaTeX”，再粘贴到这里。",
        "Mathematica: select the formula, right-click, choose Copy As → LaTeX, then paste it here.",
    ),
    "latex_hint_matlab": (
        "MATLAB：粘贴表达式右侧；支持将 .^、.*、./ 转为标准 Python 运算符。",
        "MATLAB: paste the right-hand expression. Element-wise .^, .* and ./ are converted to Python operators.",
    ),
    "latex_hint_general": (
        "通用 LaTeX：不同来源的写法可能不规范或存在歧义，转换不保证 100% 准确；请核对结果。",
        "General LaTeX: nonstandard or ambiguous notation may be misinterpreted. Conversion is not guaranteed to be 100% accurate; check the result.",
    ),
    "latex_verify": (
        "转换后请核对变量、上下标、乘方和积分上下限。",
        "Check variables, subscripts, powers and integration limits after conversion.",
    ),
    "smart_labels": (
        "小区域标记自动避让与引导线",
        "Avoid small-region label overlap with leader arrows",
    ),
}
# 主窗口、标签页、菜单、按钮与状态栏。
TEXT = {
    "title": (
        "彼图 BeTu 1.0.0 · 科研仿真与 Excel 数据绘图",
        "BeTu 1.0.0 · Scientific Simulation & Excel Plotting",
    ),
    "about": ("关于...", "About..."),
    "author": (
        "作者：田雨鑫｜东北大学 博士｜tianyuxin@mail.neu.edu.cn",
        "Yu-Xin Tian, PhD | Northeastern University | tianyuxin@mail.neu.edu.cn",
    ),
    "brand": ("彼图 BeTu", "BeTu"),
    "slogan": ("Be better tool for U!", "Be better tool for U!"),
    "tabs": (
        ["公式到曲线", "模式比较", "关系区域比较", "公式到三维图", "数据到绘图"],
        [
            "Formula to Curves",
            "Mode Comparison",
            "Region Relationships",
            "Formula to 3D",
            "Data to Plots",
        ],
    ),
    "recognize": ("公式识别", "Recognize formulas"),
    "symbols": ("Ω...", "Ω..."),
    "latex": ("LaTex转换...", "LaTeX conversion..."),
    "clear": ("清空", "Clear"),
    "example": ("加载案例", "Load example"),
    "help": ("使用帮助", "Help"),
    "draw": ("出图...", "Plot..."),
    "save": ("保存代码...", "Save code..."),
    "open": ("打开代码...", "Open code..."),
    "style": ("通用样式...", "Plot styles..."),
    "legend": ("设置图例...", "Legend settings..."),
    "advanced": ("高级设置...", "Advanced settings..."),
    "show_legend": ("显示图例", "Show legend"),
    "grid": ("显示浅灰虚线网格", "Show light dashed grid"),
    "expression": ("表达式输入", "Formula input"),
    "parameters": ("参数与分析范围", "Parameters & ranges"),
    "assigns": ("参数赋值（如 a=2, b=1）", "Parameter values (e.g., a=2, b=1)"),
    "x_variable": ("横轴分析参数", "X parameter"),
    "y_variable": ("纵轴分析参数", "Y parameter"),
    "x_range": ("横轴范围", "X range"),
    "y_range": ("纵轴范围", "Y range"),
    "step": ("步长", "Step"),
    "output": (
        "运行信息 / 可直接运行的Python代码",
        "Status / Executable Python code",
    ),
    "ready": ("就绪", "Ready"),
    "recognized": (
        "公式识别成功：{symbols}；中间赋值 {count} 条",
        "Formulas recognized: {symbols}; {count} intermediate assignments",
    ),
    "working": ("正在计算并绘图，请稍候...", "Calculating and plotting..."),
    "complete": ("绘图完成", "Plot ready"),
    "saved": ("代码已保存", "Code saved"),
    "loaded": ("代码与控件已恢复", "Code and controls restored"),
    "error": ("请检查输入", "Please check input"),
    "ok": ("确定", "OK"),
    "cancel": ("取消", "Cancel"),
    "reset": ("恢复默认", "Reset defaults"),
    "check": ("语法检查", "Check syntax"),
    "syntax_ok": ("语法检查通过", "Syntax check passed"),
    "advanced_hint": (
        "对象为 the_plt；补充代码将在绘图后执行。默认留空。",
        "Use the_plt; this code runs after plotting. Leave blank by default.",
    ),
    "advanced_note": (
        "相对保存路径默认位于 Documents。这里执行本机 Python 代码；语法检查不会执行。",
        "Relative save paths use Documents. This runs local Python; syntax checking does not execute it.",
    ),
    "add_title": ("设置标题", "Add title"),
    "add_text": ("文字标注", "Add annotation"),
    "add_save": ("自动保存 SVG", "Save SVG"),
    "plot_window": ("彼图 · 绘图预览", "BeTu · Plot Preview"),
    "close": ("关闭", "Close"),
    "import_data": ("导入Excel/CSV...", "Import Excel/CSV..."),
    "paste": ("粘贴数据", "Paste data"),
    "add_row": ("增加行", "Add row"),
    "add_column": ("增加列", "Add column"),
    "column_name": ("列名", "Column name"),
    "kind": ("图形类型", "Chart type"),
    "x_column": ("横轴/分类列", "X / category column"),
    "series": ("系列（可多选）", "Series (multiple selection)"),
    "row_numbers": ("使用行号", "Use row numbers"),
    "bins": ("直方图分箱数", "Histogram bins"),
    "table_hint": (
        "双击列名可改名；Ctrl+V 从选中单元格粘贴；Ctrl+滚轮缩放。",
        "Double-click a column name to rename it; Ctrl+V pastes at the selected cell; Ctrl+wheel zooms.",
    ),
    # 数据导入预览：用于“粘贴数据”和“导入 Excel/CSV”的首行判断与确认。
    "table_preview": ("数据导入预览", "Data Import Preview"),
    # 帮助 HTML：图片文件缺失或损坏时显示文件名，便于定位替换问题。
    "help_image_missing": (
        "图片暂时无法加载：{name}。请检查该图片后重新打开帮助。",
        "Image could not be loaded: {name}. Check the image and reopen Help.",
    ),
    "first_row_header": ("首行是列名", "First row contains column names"),
    "table_preview_hint": (
        "已自动判断首行用途，请核对预览。勾选时首行用作列名；取消勾选时保留首行数据，并自动生成列名。",
        "Check the detected first-row setting in the preview. When checked, the first row supplies column names; otherwise, it stays in the data and column names are generated.",
    ),
    "table_preview_count": (
        "共 {rows} 行数据，{columns} 列；预览前 {shown} 行。",
        "{rows} data rows, {columns} columns; showing the first {shown} rows.",
    ),
    "table_import_confirm": ("导入数据", "Import Data"),
    "table_imported": (
        "已导入 {rows} 行数据、{columns} 列。请选择横轴和系列。",
        "Imported {rows} data rows and {columns} columns. Select the X column and series.",
    ),
    # 绘图风格设置 → 坐标与其他设置：模式比较和关系区域比较的碎块过滤。
    "dropout_hint": (
        "按单个分块占整个绘图区的面积比例过滤。0.001 = 0.1%，0.01 = 1%；越大过滤越多，0 表示不过滤。低于阈值的分块不绘制、不标注，也不生成引导线。",
        "Filter each connected component by its fraction of the full plot area. 0.001 = 0.1%, 0.01 = 1%; larger values remove more, and 0 disables filtering. Components below the threshold have no fill, label or arrow.",
    ),
    "invalid_dropout": (
        "dropout 必须是 0 到 1 之间的有限数值。",
        "dropout must be a finite number between 0 and 1.",
    ),
    "sheet": ("选择工作表", "Choose worksheet"),
    "tutorial": ("图形教程...", "Chart guide..."),
    "code_filter": (
        "Python 代码 (*.py);;文本文件 (*.txt)",
        "Python code (*.py);;Text files (*.txt)",
    ),
    "data_filter": (
        "表格 (*.xlsx *.xlsm *.xls *.csv *.tsv)",
        "Tables (*.xlsx *.xlsm *.xls *.csv *.tsv)",
    ),
    "convert": ("转换", "Convert"),
    "copy": ("复制结果", "Copy result"),
    "latex_input": (
        "输入公式右侧的 LaTeX / Matlab 文本",
        "Enter LaTeX / Matlab for the right-hand expression",
    ),
    "latex_output": (
        "标准 SymPy 表达式（**、lamda）",
        "Standard SymPy expression (**, lamda)",
    ),
    "latex_modes": (
        ["通用 LaTeX", "Mathematica LaTeX", "Matlab"],
        ["General LaTeX", "Mathematica LaTeX", "Matlab"],
    ),
    "overwrite": (
        "加载案例会替换本页内容，是否继续？",
        "Replace this tab with the example?",
    ),
    "invalid_line": (
        "第 {line} 行需要“名称 = 表达式”或“变量 := 表达式”。",
        "Line {line}: expected name = expression or variable := expression.",
    ),
    "invalid_name": (
        "无效中间变量名：{name}。仅允许字母、下划线和数字，且不能以数字开头，也不能与函数或关键字重名。",
        "Invalid intermediate name: {name}. Use letters, underscores and digits; no leading digit, reserved function or keyword.",
    ),
    "cycle": (
        "中间变量存在循环引用或引用了尚无初值的自身：{names}",
        "Cyclic intermediate dependency or self-reference without an initial value: {names}",
    ),
    "empty_formula": (
        "请先输入至少一个绘图表达式。",
        "Enter at least one plot expression.",
    ),
    "duplicate_label": ("表达式名称重复：{name}", "Duplicate plot label: {name}"),
    "label_ref": (
        "绘图名称不能作为未定义符号引用：{name}。请用 := 定义中间变量。",
        "A plot label cannot be used as an undefined symbol: {name}. Define an intermediate with :=.",
    ),
    "unsupported_code": (
        "无法恢复该代码的绘图参数。请打开 BeTu 导出的代码。",
        "Cannot restore plot parameters. Open code exported by BeTu.",
    ),
    "invalid_value": (
        "参数 {name} 的值无效：{value}",
        "Invalid value for {name}: {value}",
    ),
    "param_required": (
        "请选择分析参数，并给其他自由参数赋值：{names}",
        "Choose analysis parameters and assign the remaining free parameters: {names}",
    ),
    "table_empty": (
        "请导入、粘贴数据或加载案例，并选择系列。",
        "Import/paste data or load an example, then select series.",
    ),
    "example_missing": ("可用案例：{names}", "Available examples: {names}"),
    "language": ("界面语言", "Interface language"),
}
TEXT.update(EDITOR_TEXT)

# 公式转换窗口：列表显示顺序、内部模式值与说明。
CONVERSION_MODES = [
    (("Mathematica", "Mathematica"), 1, "latex_hint_mathematica"),
    (("MATLAB", "MATLAB"), 2, "latex_hint_matlab"),
    (("通用 LaTeX", "General LaTeX"), 0, "latex_hint_general"),
]

# 标记形状下拉列表：名称；内部仍传 Matplotlib 标记值。
MARKER_NAMES = {
    None: ("无标记", "No marker"),
    "o": ("圆形", "Circle"),
    "s": ("方形", "Square"),
    "*": ("星形", "Star"),
    "P": ("实心加号", "Filled plus"),
    "X": ("实心叉号", "Filled X"),
    "D": ("菱形", "Diamond"),
    "p": ("五边形", "Pentagon"),
    "x": ("叉号", "X"),
    "8": ("八边形", "Octagon"),
    "2": ("三向上箭头", "Tri-up"),
    "H": ("六边形（横向）", "Horizontal hexagon"),
    "+": ("加号", "Plus"),
    "|": ("竖线", "Vertical line"),
    "<": ("左三角", "Left triangle"),
    ">": ("右三角", "Right triangle"),
    "^": ("上三角", "Up triangle"),
    "v": ("下三角", "Down triangle"),
    "d": ("瘦菱形", "Thin diamond"),
    "3": ("三向左箭头", "Tri-left"),
    ".": ("圆点", "Point"),
}
# 下拉框显示名称；内部始终使用英文代码。
CHART_LABELS = {
    "line": ("折线图", "Line"),
    "bar": ("条形图", "Bar"),
    "barh": ("水平条形图", "Horizontal bar"),
    "box": ("箱型图", "Box plot"),
    "pie": ("饼状图", "Pie"),
    "hist": ("直方图", "Histogram"),
    "scatter": ("散点图", "Scatter"),
}
LOC_LABELS = {
    "best": ("自动选择", "Best"),
    "outside right": ("图外右侧", "Outside right"),
    "upper right": ("右上", "Upper right"),
    "upper left": ("左上", "Upper left"),
    "lower right": ("右下", "Lower right"),
    "lower left": ("左下", "Lower left"),
    "center": ("居中", "Center"),
    "upper center": ("上方居中", "Upper center"),
    "lower center": ("下方居中", "Lower center"),
    "center left": ("左侧居中", "Center left"),
    "center right": ("右侧居中", "Center right"),
}
# 精细图例对话框字段。
LEGEND_LABELS = {
    "ncol": ("图例列数", "Columns"),
    "loc": ("图例位置", "Location"),
    "borderpad": ("边框内边距", "Border padding"),
    "labelspacing": ("行间距", "Row spacing"),
    "handlelength": ("符号长度", "Handle length"),
    "handletextpad": ("符号与文字间距", "Handle/text gap"),
    "columnspacing": ("列间距", "Column spacing"),
    "fontsize": ("图例字号", "Font size"),
}


def tr(key, **values):
    result = TEXT[key][0 if LANGUAGE == "zh" else 1]
    return result.format(**values) if isinstance(result, str) else result


def label(pair):
    return pair[0 if LANGUAGE == "zh" else 1]


def set_language(language):
    global LANGUAGE
    LANGUAGE = language


# 公式输入框占位引导语；中文完整说明与英文译文。
FORMULA_GUIDE = (
    r"""逐行写表达式，格式为：      表达式名称 = 表达式
                           例如        $p_a$ = 2*a*x + b*x**2
○ 表达式名称可以用$包裹的LaTex书写，例如$\pi_M^{NN}$
○ 表达式由变量名和运算符号（+-*/，次方**）、函数（如积分∫，可通过“Ω...”符号面板键入）组成

若有中间变量，用“:=”赋值，格式为：    变量名 := 表达式
                       例如                                p_n := 2*a + b -  (1/2)*c**3
                                                             $\pi_R$ = integrate(p_n*t+b-3*t**2, (t, p_n-c, p_n+a*b))
第一行是中间变量，第二行是含有定积分的绘图表达式
注意：变量名不可以是LaTex，只能由大小写字母、下划线和数字，且数字不能开头，例如p_n。

表达式中的希腊字母和函数可以通过“Ω...”符号面板键入。""",
    r"""Write one expression per line:     Plot name = expression
                       Example:     $p_a$ = 2*a*x + b*x**2
○ Plot names may use LaTeX enclosed in $, e.g. $\pi_M^{NN}$.
○ Expressions contain variables, operators (+-*/, powers **) and functions (e.g. integrals ∫, available in “Ω...”).

Define intermediate variables with := :    variable := expression
Example:     p_n := 2*a + b - (1/2)*c**3
             $\pi_R$ = integrate(p_n*t+b-3*t**2, (t, p_n-c, p_n+a*b))
The first line defines an intermediate; the second is a plot expression containing a definite integral.
Variable names must use letters, underscores and digits, with no leading digit (e.g. p_n), not LaTeX.

Insert Greek letters and functions using the “Ω...” panel.""",
)

PACKAGE_DOC = """彼图（BeTu）科研仿真与 Excel 数据绘图工具。
BeTu — Be better tool for U!
作者：田雨鑫，东北大学 博士；邮箱：tianyuxin@mail.neu.edu.cn。
makefig() 打开 Qt5 中英文界面；安装后运行 betu 即可启动。
公式可用 := 定义中间变量，支持积分、数组索引和前向引用。
data_lines、draw_lines、draw_max_area、draw_detail_area、draw_3D、plot_table 提供绘图接口。
make_example('draw_lines') 打印带中文注释、独立参数变量的完整版示例，只接收一个参数。
数据示例名称为 data_line、data_bar、data_barh、data_box、data_pie、data_hist、data_scatter。
区域标注示例为 disconnected_modes（分块标注）、smart_regions（小区域引导线）。
代码默认保存为 .py；图例参数传给绘图函数，高级代码直接位于绘图调用后。
"""
DESCRIPTION = (
    "彼图（BeTu）科研仿真与Excel数据绘图工具，支持图形界面、符号公式计算、数值仿真、论文标准绘图风格和Python扩展。"
    "BeTu——Be better tool for U! BeTu scientific simulation and Excel data plotting tool, supporting graphical user interface, "
    "symbolic formula calculation, numerical simulation, paper-standard plotting styles, and Python extension."
)
# 高级设置快捷按钮插入的代码。
TITLE_CODE = (
    'the_plt.title("图表标题", fontsize=14)\n',
    'the_plt.title("Chart title", fontsize=14)\n',
)
TEXT_CODE = (
    'the_plt.text(0.5, 0.95, "文字标注", transform=the_plt.gca().transAxes, ha="center", va="top")\n',
    'the_plt.text(0.5, 0.95, "Annotation", transform=the_plt.gca().transAxes, ha="center", va="top")\n',
)
SAVE_CODE = 'the_plt.savefig("filename.svg", format="svg", bbox_inches="tight", dpi=300, transparent=False)\n'
# 符号面板及识别器保留名。cse 为公共子表达式消除函数。
SYMPY_NAMES = [
    "symbols",
    "Symbol",
    "Abs",
    "exp",
    "oo",
    "sqrt",
    "root",
    "log",
    "ln",
    "integrate",
    "diff",
    "limit",
    "summation",
    "product",
    "sin",
    "cos",
    "tan",
    "csc",
    "sec",
    "cot",
    "sinh",
    "cosh",
    "tanh",
    "coth",
    "acos",
    "acosh",
    "acot",
    "acoth",
    "acsc",
    "acsch",
    "asec",
    "asech",
    "asin",
    "asinh",
    "atan",
    "atan2",
    "atanh",
    "csch",
    "cse",
    "Mod",
    "pi",
    "sech",
    "sinc",
    "floor",
    "ceiling",
    "Piecewise",
    "Rational",
    "Number",
]
GREEK_NAMES = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lamda",
    "mu",
    "nu",
    "xi",
    "omicron",
    "pi",
    "rho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega",
]
SYMBOL_TEMPLATES = {
    "integrate": "integrate(f, (x, a, b))",
    "diff": "diff(f, x)",
    "limit": "limit(f, x, 0)",
    "summation": "summation(f, (k, 1, n))",
    "product": "product(f, (k, 1, n))",
    "Piecewise": "Piecewise((x, x > 0), (0, True))",
    "Rational": "Rational(1, 2)",
    "symbols": "symbols('x y')",
    "Symbol": "Symbol('x')",
    "root": "root(x, 3)",
    "cse": "cse([f, g])",
}

# 仿真案例的表达式与参数；Qt 界面和 make_example 共享。
SIMULATION_FORMULAS = r"""$A$ = (a-x)**2 + y
$B$ = x + 2*y
$C$ = 2-x + y**2
p_n := a + x
$D$ = integrate(p_n*t, (t, 0, y))"""
SIMULATION_ASSIGNMENTS = "a=2, y=0.5"
# core_functions.draw_area：图内区域编号与图例中的关系说明。
REGION_NAME_FORMAT = "{prefix} {number}"
REGION_LEGEND_FORMAT = "{name}: {relation}"
# Jupyter 教程：说明单元格、高清设置和绘图代码。
JUPYTER_INTRO = "# 彼图 BeTu：在 Jupyter 中绘图\n\n先安装 `betu`，按顺序运行单元格。比较 NW、BW、NS、BS 四种模式的利润。"
JUPYTER_IMPORT = "%config InlineBackend.figure_format = 'retina' # 在 Jupyter 中显示高清图片\nfrom betu import *"
JUPYTER_FORMULAS = "## 定义公式和固定参数\n\n使用符号 E 表示模型参数；乘方写为 `**`。"
JUPYTER_PLOT_INTRO = "## 绘制关系区域图\n\n横轴为 alpha（0.7～0.8），纵轴为 b（0～0.08）。图例放在图外，标明各区域的利润排序。"
JUPYTER_PLOT_CODE = r"""%config InlineBackend.figure_format = 'retina' # 在 Jupyter 中显示高清图片
pattern_moves = [[0, 0], [-0.018, -0.007], [0.004, -0.013], [0, 0], [0, 0], [0, 0]]
the_plt = draw_detail_area(
    expressions, assigns, alpha, [0.7, 0.8], b, [0, 0.08],
    x_name=r'$\alpha$', y_name='$b$', precision=1000, figsize=[8, 5],
    pattern_moves=pattern_moves,
)
the_plt.show()"""
JUPYTER_EXAMPLE_INTRO = "## 生成带注释的完整示例\n\n下一个单元格打印完整代码，按需复制并修改参数。其他图形可用 `make_example('draw_lines')`、`make_example('data_pie')` 等。"
JUPYTER_EXAMPLE_CODE = "make_example('draw_detail_area')"
# 图形教程：各数据类型的用途和数据组织规则。
CHART_GUIDES = {
    "line": (
        "折线图适合观察数据随时间或其他横轴值变化的趋势。每行对应一个横轴值，每个数值系列绘制成一条线。选择年份、时间或其他横轴列，再选择需要比较的数值列。",
        "Line charts show trends over time or another X variable. Each row supplies one X value, and each numeric series becomes a line. Select the year, time, or other X column, then choose the numeric columns to compare.",
    ),
    "bar": (
        "条形图适合比较不同类别的数值。每行对应一个类别，横轴列选择类别名称，数值系列选择要比较的数值列。选择多个系列时，同一类别的条形会并排显示。",
        "Bar charts compare values across categories. Use one category per row, select the category names as the X column, and choose the numeric columns to compare. With multiple series, bars for the same category appear side by side.",
    ),
    "barh": (
        "水平条形图适合类别名称较长的情况。在界面的横轴列选项中选择类别名称，再选择数值系列。绘图时，类别显示在纵轴上，条形沿水平方向延伸，其长度表示数值大小。",
        "Horizontal bar charts work well with long category names. Select the category column in the interface's X-column selector, then choose the numeric series. In the plot, categories appear on the vertical axis and horizontal bar lengths represent their values.",
    ),
    "pie": (
        "饼状图适合展示各部分占总体的比例。每行对应一个扇区，在横轴列选项中选择扇区名称，数值系列只选择一列。数值不能为负，且总和必须大于零。扇区内的百分比文字会根据背景深浅自动使用黑色或白色。",
        "Pie charts show how parts contribute to a whole. Each row corresponds to a slice. Select the slice names as the X column and choose exactly one numeric series. Values must be nonnegative and their total must be positive. Percentage labels use black or white according to the slice color.",
    ),
    "box": (
        "箱型图适合比较数据的分布和离散程度。每行填写一次原始观测值，无需预先求平均。选择分类列后，同一类别的观测会归为一组；不选择分类列时，每个数值系列单独绘制一个箱体。箱体表示第 25 百分位数到第 75 百分位数之间的范围，中线表示中位数。",
        "Box plots compare distributions and variability. Enter individual observations without averaging them first. If a category column is selected, observations with the same category are grouped together; otherwise, each numeric series forms one box. A box spans the 25th to 75th percentiles, and its center line marks the median.",
    ),
    "hist": (
        "直方图适合观察数值在不同区间内的分布。每行填写一个原始观测值，选择需要统计的数值系列，无需指定横轴列。程序会将数值范围划分为若干区间，并统计各区间的数据数量；可通过“分箱数”调整区间数量。",
        "Histograms show how observations are distributed across value intervals. Enter one raw observation per row and select the numeric series to summarize; no X column is required. The program divides the value range into intervals and counts observations in each. Adjust the bin count to change the number of intervals.",
    ),
    "scatter": (
        "散点图适合观察两个数值变量之间的关系。横轴列和数值系列都应选择数值列，每行的一对数值对应一个点。选择多个数值系列时，每个系列分别与同一横轴列配对绘制。",
        "Scatter plots show relationships between numeric variables. Select numeric columns for both X and the series; each row contributes a point from its pair of values. If you select multiple series, each is plotted against the same X column.",
    ),
}


def table_example(kind):
    from copy import deepcopy

    annual = {
        "Year": [2020, 2021, 2022, 2023, 2024, 2025],
        "A": [10, 13, 16, 19, 22, 25],
        "B": [13, 15, 17, 19, 21, 23],
    }
    samples = {
        "line": (annual, "Year", ["A", "B"]),
        "bar": (annual, "Year", ["A", "B"]),
        "barh": (
            {
                "Department": ["R&D", "Production", "Sales", "Service"],
                "Current": [36, 52, 45, 29],
                "Previous": [30, 48, 39, 26],
            },
            "Department",
            ["Current", "Previous"],
        ),
        "pie": (
            {
                "Category": ["Materials", "Labor", "Equipment", "Transport", "Other"],
                "Amount": [40, 25, 15, 12, 8],
            },
            "Category",
            ["Amount"],
        ),
        "box": (
            {
                "Group": ["Control"] * 8 + ["Treatment"] * 8,
                "A": [10, 11, 12, 10, 13, 11, 12, 22, 17, 18, 19, 20, 18, 21, 19, 20],
                "B": [13, 14, 15, 13, 16, 14, 15, 14, 19, 20, 22, 21, 23, 20, 21, 22],
            },
            "Group",
            ["A", "B"],
        ),
        "hist": (
            {
                "Score": [
                    45,
                    48,
                    50,
                    52,
                    54,
                    55,
                    57,
                    58,
                    59,
                    60,
                    61,
                    62,
                    63,
                    64,
                    65,
                    65,
                    66,
                    67,
                    68,
                    69,
                    70,
                    70,
                    71,
                    72,
                    73,
                    74,
                    75,
                    76,
                    78,
                    80,
                    82,
                    84,
                    87,
                    90,
                    93,
                    96,
                ]
            },
            None,
            ["Score"],
        ),
        "scatter": (
            {
                "Input": [1, 2, 3, 4, 5, 6, 7, 8],
                "A": [2, 4, 5, 7, 9, 10, 13, 14],
                "B": [3, 3, 6, 6, 8, 11, 11, 13],
            },
            "Input",
            ["A", "B"],
        ),
    }
    data, x, series = deepcopy(samples[kind])
    return dict(data=data, x=x, series=series, kind=kind, bins=6)


# 通用样式对话框和导出代码中的参数说明。
PARAMETER_COMMENTS = {
    "data": "绘图数据",
    "expressions": "表达式",
    "assigns": "参数赋值",
    "the_var": "要分析的参数",
    "ranges": "参数取值范围：起点、终点、步长",
    "the_var_x": "横轴分析参数",
    "the_var_y": "纵轴分析参数",
    "start_end_x": "横轴参数取值范围",
    "start_end_y": "纵轴参数取值范围",
    "label_x": "横轴刻度标签",
    "x": "横轴数据列",
    "series": "数据系列列",
    "kind": "图形类型",
    "bins": "直方图分箱数",
    "x_name": "x 轴名称",
    "y_name": "y 轴名称",
    "z_name": "z 轴名称",
    "save_dir": "图片保存路径、文件名",
    "location": "图例的方位",
    "ncol": "图例的列数",
    "fsize": "图片中字号的大小",
    "figsize": "图片大小（英寸）",
    "xt_rotation": "x 轴刻度旋转角度",
    "yt_rotation": "y 轴刻度旋转角度",
    "xrotation": "x 轴标签旋转角度",
    "yrotation": "y 轴标签旋转角度",
    "zrotation": "z 轴标签旋转角度",
    "linestyles": "线的风格",
    "linewidth": "线粗",
    "linewidths": "区域边界线粗",
    "markers": "线上的标记符号",
    "markersize": "标记符号的大小",
    "colors": "绘图颜色",
    "isgrid": "是否显示浅灰虚线网格",
    "xpad": "x 轴刻度与轴线的距离",
    "ypad": "y 轴刻度与轴线的距离",
    "zpad": "z 轴刻度与轴线的距离",
    "xlabelpad": "x 轴名称与刻度的距离",
    "ylabelpad": "y 轴名称与刻度的距离",
    "zlabelpad": "z 轴名称与刻度的距离",
    "xlabelsize": "x 轴名称字号",
    "ylabelsize": "y 轴名称字号",
    "zlabelsize": "z 轴名称字号",
    "legendsize": "图例字号",
    "legend_options": "图例精细设置（None 表示使用上面的图例参数）",
    "color_alpha": "曲面透明度",
    "edgecolor": "曲面网格线颜色",
    "precision": "计算采样精度",
    "density": "曲面网格密度",
    "elevation": "三维视角仰角",
    "azimuth": "三维视角方位角",
    "roll": "三维视角滚转角",
    "x_lim": "x 轴显示范围",
    "y_lim": "y 轴显示范围",
    "z_lim": "z 轴显示范围",
    "left_margin": "绘图区左边距",
    "right_margin": "绘图区右边界",
    "bottom_margin": "绘图区下边距",
    "top_margin": "绘图区上边界",
    "texts": "区域文字标注",
    "text_fsize_add": "区域文字字号增量",
    "patterns": "区域填充纹理",
    "pattern_colors": "区域标注文字颜色",
    "pattern_moves": "区域标注位置偏移",
    "switchcolor": "标注黑白配色阈值",
    "prefix": "区域标注前缀",
    "numbers": "区域编号格式",
    "dropout": "忽略小区域（面积比例）",
    "show_legend": "是否显示图例",
    "symbols": "定义符号",
    "intermediates": "中间变量",
    "advanced": "补充的高级设置代码",
}
PLOT_FUNCTIONS = (
    "data_lines",
    "draw_lines",
    "draw_max_area",
    "draw_detail_area",
    "draw_3D",
    "plot_table",
)
TAB_FUNCTIONS = (
    "draw_lines",
    "draw_max_area",
    "draw_detail_area",
    "draw_3D",
    "plot_table",
)
PARAMETER_ENGLISH = {
    key: key.replace("_", " ").capitalize() for key in PARAMETER_COMMENTS
}
PARAMETER_ENGLISH.update(
    fsize="Global font size",
    figsize="Figure size (inches)",
    xt_rotation="X tick rotation",
    yt_rotation="Y tick rotation",
    xrotation="X label rotation",
    yrotation="Y label rotation",
    zrotation="Z label rotation",
    ncol="Legend columns",
    xlabelpad="X label padding",
    ylabelpad="Y label padding",
    xpad="X tick padding",
    ypad="Y tick padding",
    text_fsize_add="Region label font size offset",
    dropout="Minimum region area fraction",
    symbols="Define symbols",
    intermediates="Intermediate variables",
    expressions="Plot expressions",
    assigns="Parameter values",
    the_var="Analysis parameter",
    ranges="Range: start, end, step",
)


def parameter_label(name):
    if name == "smart_labels":
        return tr("smart_labels")
    return (
        PARAMETER_COMMENTS.get(name, name)
        if LANGUAGE == "zh"
        else PARAMETER_ENGLISH.get(name, name)
    )


def code_comment(name):
    if name == "dropout":
        return "# " + label(REGION_DROPOUT_COMMENT)
    return "# " + parameter_label(name)


# 完整示例中 dropout 参数上方的注释。
REGION_DROPOUT_COMMENT = (
    "小区域面积比例阈值：0.001=0.1%，0 不过滤；按每个独立分块判断",
    "Minimum area fraction per connected component: 0.001=0.1%; 0 disables filtering",
)


def default_parameters(function):
    import inspect
    from copy import deepcopy
    import betu as core_functions
    from .table import plot_table
    from ._default_setting import DEFAULT_LINESTYLES, LEGEND_DEFAULTS, UI_3D_COLORS

    fn = plot_table if function == "plot_table" else getattr(core_functions, function)
    result = {
        name: deepcopy(p.default)
        for name, p in inspect.signature(fn).parameters.items()
        if p.default is not inspect.Parameter.empty
    }
    if result.get("linestyles", "absent") is None:
        result["linestyles"] = list(DEFAULT_LINESTYLES)
    result["legend_options"] = dict(LEGEND_DEFAULTS)
    if function == "draw_detail_area":
        result["legend_options"]["loc"] = "outside right"
    if "isgrid" in result and function == "draw_3D":
        result["isgrid"] = False
    if function == "draw_3D":
        result.update(precision=1000)
    if function in ("draw_max_area", "draw_detail_area"):
        result.update(precision=1000, text_fsize_add=-2)
    result["title"] = ""
    return result


def build_code(function, formula="", parameters=None, advanced="", data=None):
    """生成逐项参数的完整脚本；图例直接传入绘图函数。"""
    from .formula import parse_formulas
    from pprint import pformat
    import ast

    parameters = dict(parameters or {})
    sections = ["from betu import *"]
    if function not in ("plot_table", "data_lines"):
        sections.append(parse_formulas(formula).source())
    else:
        sections.append(
            code_comment("data")
            + "\ndata = "
            + pformat(data, sort_dicts=False, width=100)
        )
    for key, value in parameters.items():
        if key in ("expressions", "data"):
            continue
        if key in ("the_var", "the_var_x", "the_var_y"):
            rendered = str(value)
        elif key == "assigns":
            rendered = (
                "{" + ", ".join(str(k) + ": " + repr(v) for k, v in value.items()) + "}"
            )
        else:
            rendered = pformat(value, sort_dicts=False, width=100)
        sections.append(code_comment(key) + "\n" + key + " = " + rendered)
    primary = "data" if function in ("plot_table", "data_lines") else "expressions"
    args = [primary + "=" + primary] + [
        key + "=" + key
        for key in parameters
        if key not in ("data", "expressions", "title")
    ]
    sections.append("the_plt = " + function + "(\n    " + ",\n    ".join(args) + "\n)")
    sections.append("the_plt = plot_context(the_plt)")
    if "title" in parameters:
        sections.append("if title:\n    the_plt.title(title, fontsize=fsize)")
    if advanced.strip():
        sections.append(code_comment("advanced") + "\n" + advanced.strip())
    if parameters.get("save_dir") is not None and (
        parameters.get("title") or advanced.strip()
    ):
        sections.append(SAVE_FINAL_CODE)
    sections.append("the_plt.show()")
    code = "\n\n".join(sections) + "\n"
    ast.parse(code)
    return code


# 导出程序：标题和高级操作完成后更新自动保存的图片。
SAVE_FINAL_CODE = (
    'the_plt.savefig(save_dir, bbox_inches="tight", dpi=600, transparent=False)'
)


def example_code(name="draw_lines"):
    if name in REGION_EXAMPLES:
        function, formula = REGION_EXAMPLES[name]
        parameters = default_parameters(function)
        parameters.update(
            assigns={},
            the_var_x="x",
            start_end_x=[0, 1],
            the_var_y="y",
            start_end_y=[0, 1],
            x_name="$x$",
            y_name="$y$",
        )
        return build_code(function, formula, parameters)
    function = name
    parameters = None
    if name.startswith("data_") and name not in ("data_lines",):
        kind = name[5:]
        if kind in CHART_LABELS:
            sample = table_example(kind)
            parameters = default_parameters("plot_table")
            parameters.update({k: v for k, v in sample.items() if k != "data"})
            return build_code("plot_table", parameters=parameters, data=sample["data"])
    if name == "plot_table":
        return example_code("data_bar")
    if function not in PLOT_FUNCTIONS:
        raise ValueError(
            tr(
                "example_missing",
                names=", ".join(PLOT_FUNCTIONS)
                + ", "
                + ", ".join("data_" + k for k in CHART_LABELS),
            )
        )
    parameters = default_parameters(function)
    if function == "data_lines":
        parameters.update(
            label_x=["2024", "2025", "2026"], x_name="Year", y_name="Value"
        )
        return build_code(
            function, parameters=parameters, data={"A": [10, 13, 16], "B": [12, 14, 15]}
        )
    if function in ("draw_detail_area", "draw_3D"):
        assigns = dict(PAPER_ASSIGNS)
        assigns.pop("alpha")
        parameters.update(
            assigns=assigns,
            the_var_x="alpha",
            start_end_x=[0.7, 0.8],
            the_var_y="b",
            start_end_y=[0, 0.08],
            x_name=r"$\alpha$",
            y_name="$b$",
        )
        if function == "draw_detail_area":
            parameters["pattern_moves"] = [list(move) for move in PAPER_LABEL_MOVES]
        else:
            parameters["z_name"] = r"$\pi_r$"
        return build_code(function, PAPER_FORMULAS, parameters)
    parameters.update(assigns={"a": 2}, x_name="$x$", y_name="$y$")
    if function == "draw_lines":
        parameters.update(assigns={"a": 2, "y": 0.5}, the_var="x", ranges=[0, 2, 0.025])
    else:
        parameters.update(
            the_var_x="x", start_end_x=[0, 2], the_var_y="y", start_end_y=[0, 2]
        )
    return build_code(function, SIMULATION_FORMULAS, parameters)


def make_example(fun_name="draw_lines"):
    """打印完整绘图代码，只接收示例名称。"""
    print(example_code(fun_name))


# 分块标注与小区域引导线的完整可加载案例。
REGION_EXAMPLES = {
    "disconnected_modes": (
        "draw_max_area",
        "NC = (x-0.4)*(x-0.6) + 0*y\nNP = 0*x + 0*y",
    ),
    "smart_regions": (
        "draw_detail_area",
        "$A$ = x\n$B$ = y\n$C$ = 0.88 + 0*x",
    ),
}


# 使用帮助窗口：HTML 正文。math 标签由帮助控件渲染为数学公式。
HELP_HTML = (
    r"""
<h1>彼图 BeTu 使用帮助</h1>
<p>作者：田雨鑫｜东北大学｜博士｜tianyuxin@mail.neu.edu.cn</p>
<p>彼图支持根据公式进行数值仿真，也支持从 Excel 或数据表直接绘图。第一次使用时，可在相应标签页点击“加载案例”，再点击“出图...”查看结果。</p>
<p>公式绘图的基本顺序是：<b>输入表达式 → 公式识别 → 设置分析参数、范围和固定值 → 调整绘图风格 → 出图</b>。数据表绘图的方法见第 5 节。</p>
<h2>1. 输入表达式和中间变量</h2>
<p>每行输入一个绘图表达式，格式为 <code>名称 = 表达式</code>。左侧名称用于标识曲线或模式，可使用由 <code>$</code> 包裹的 LaTeX；右侧计算式使用 Python 语法，乘法写成 <code>*</code>，乘方写成 <code>**</code>。</p>
<pre>$p_a$ = 2*a*x + b*x**2
p_n := 2*a + b - c**3/2
$\pi_R$ = integrate(p_n*t+b-3*t**2, (t, p_n-c, p_n+a*b))</pre>
<p>其中，<code>p_n := ...</code> 定义中间变量，其余两行是绘图表达式。对应的数学形式为：</p>
<p><math>p_a = 2ax + bx^2</math></p>
<p><math>p_n = 2a+b-\frac{c^3}{2}</math></p>
<p><math>\pi_R = \int_{p_n-c}^{p_n+ab}(p_n t+b-3t^2)\,\mathrm{d}t</math></p>
<p>中间变量可定义在绘图表达式之前或之后，名称只能包含大小写字母、下划线和数字，且不能以数字开头，例如 <code>p_n</code>。中间变量和绘图表达式左侧的名称不会列入生成代码的 <code>symbols</code> 符号定义。积分变量会列入符号定义，<code>integrate</code>、<code>sin</code> 等函数名称则不会被当成待赋值参数。</p>
<p>中间变量支持重复赋值，也支持对数组、列表或元组等对象进行索引。普通的 <code>integrate(...)</code> 通常返回一个表达式，不能直接在后面添加 <code>[0]</code>；使用索引前，请确认结果支持按位置取值。</p>
<p>点击“Ω...”可打开符号面板，选择符号后会插入对应的 Python 写法。面板保持在主窗口上方，打开时仍可继续编辑表达式；插入符号名称时会自动补充必要的空格。</p>
<p>已有公式可通过“LaTex转换...”转换。来源列表依次为 Mathematica、MATLAB、通用 LaTeX，选择后会显示相应提示。在 Mathematica 中，选中公式后右键选择“复制为 → LaTeX”；在 MATLAB 中，复制赋值语句右侧的表达式。将内容粘贴到转换窗口，点击“转换”后即可复制结果。</p>
<p>转换结果使用 <code>**</code> 表示乘方，并将变量 <code>lambda</code> 写成 <code>lamda</code>，以符合 Python 和 SymPy 的语法要求。不同来源的 LaTeX 可能存在不规范写法或歧义，转换无法保证完全准确；使用前请核对变量、上下标、乘方和积分上下限。</p>
<p><img src="help/04-latex.png" width="640" alt="LaTeX 转换窗口"></p>
<h2>2. 选择分析参数</h2>
<p>输入表达式后，点击“公式识别”。“公式到曲线”需要选择一个横轴分析参数；“模式比较”“关系区域比较”和“公式到三维图”需要为横轴、纵轴选择两个不同的参数。分别填写范围的“开始”值和“结束”值。单参数曲线的步长会根据范围自动计算，也可手动调整。</p>
<p>在“参数赋值”中填写其余参数的固定值，各项用逗号或换行分隔，例如：</p>
<pre>a=2, b=1, c=0.3</pre>
<p>正在分析的参数无需赋固定值。如果某个变量只在定积分内使用，积分后已被消去，它会保留在 <code>symbols</code> 中，但不会出现在横轴、纵轴的分析参数列表中，也无需赋固定值。</p>
<p>切换分析参数时，赋值框会自动更新，并临时记住每个参数上次使用的固定值。例如，已有 <code>y=0.5</code>，改为分析 <code>y</code> 时，该项会隐藏；改为分析其他参数后，<code>y=0.5</code> 会恢复。各标签页分别保留自己的赋值记录。没有历史赋值的参数会先填入 <code>1.0</code>，请按模型需要修改。</p>
<p><img src="help/02-formula.png" width="680" alt="公式识别、分析范围与参数赋值"></p>
<p>模式比较、关系区域比较和三维图的默认采样精度为 <code>1000</code>，即横、纵两个方向各取 1000 个采样点。可在“绘图风格设置 → 坐标与其他设置”中调整。采样精度控制计算网格的密度，与保存图片的 DPI 不同。</p>
<p>在“关系区域比较”中点击“加载案例”，可载入 NW、BW、NS、BS 四种模式的利润表达式和固定参数。横轴为 <code>alpha</code>，范围为 0.7～0.8；纵轴为 <code>b</code>，范围为 0～0.08。</p>
<p><img src="help/08-detail.png" width="680" alt="四模式利润关系区域图"></p>
<p>“公式到三维图”使用同一组表达式、固定参数和分析范围，z 轴表示利润。点击“加载案例”后再点击“出图...”，即可通过四个曲面观察两项参数对各模式利润的影响。</p>
<p><img src="help/09-surface.png" width="680" alt="四模式利润三维曲面图"></p>
<h2>3. 调整绘图风格</h2>
<p>点击“绘图风格设置...”，在同一窗口中调整公共样式、各曲线或区域的样式，以及图例。修改后点击“确定”保存设置。</p>
<table border="1" cellpadding="8" cellspacing="0">
<tr><th>设置页</th><th>主要内容</th></tr>
<tr><td>公共设置</td><td>标题、坐标轴名称、整体字号、图片宽高和文字旋转角度。标题留空时不显示标题。</td></tr>
<tr><td>曲线／区域样式</td><td>先选择曲线或区域，再调整其颜色、线型、线宽、标记或填充纹理。列表不包含中间变量。</td></tr>
<tr><td>图例设置</td><td>图例的显示开关、位置、列数、字号和间距。默认显示为 1 列。</td></tr>
<tr><td>坐标与其他设置</td><td>坐标范围、文字间距、采样精度、小区域过滤、三维视角和图片保存位置等，具体选项随图形类型变化。</td></tr>
</table>
<p>颜色列表提供色块，线型列表提供线条预览，标记列表提供形状图标和名称。选择一条曲线或一个区域后，可以单独修改其样式；切换选择时，已做的修改会保留。</p>
<p><img src="help/05-style-series.png" width="600" alt="逐条设置曲线或区域的样式"></p>
<p>所有标签页都可通过“显示图例”控制图例是否显示。模式比较默认关闭图例，关系区域比较默认将图例放在图外右侧。模式比较、关系区域比较和三维图不显示坐标背景网格。</p>
<p>模式比较和关系区域比较的样式列表使用“区域 1、区域 2……”编号。模式比较的顺序与绘图表达式一致；关系区域比较的列表则根据实际出图结果更新。</p>
<p><b>过滤细碎区域：</b>在“坐标与其他设置”中调整“忽略小区域（面积比例）”，对应的代码参数为 <code>dropout</code>。模式比较和关系区域比较均默认使用 <code>0.001</code>，即忽略面积小于整个绘图区 0.1% 的独立分块；设为 <code>0.01</code> 表示 1%，设为 <code>0</code> 则关闭过滤。</p>
<p>面积比例按采样网格估算，每个分块分别判断。低于阈值的分块不显示填色、边界、标签或引导线，其余分块正常保留。同一模式分布在多个互不相连的区域时，符合阈值的分块会分别标注，图例中只保留一项。<code>dropout</code> 越大，被隐藏的区域越多。</p>
<p><b>安排标签位置：</b>对保留的区域，程序会先尝试在区域内放置文字；如果空间不足，就将标签移到图外并添加箭头。手动将标签移出所属区域时，也会用箭头标明对应关系。可在“坐标与其他设置”中关闭自动避让，或在区域样式中调整标签的位置偏移。</p>
<h2>4. 高级设置</h2>
<p>需要进一步调整图形时，点击“高级设置...”，从“常用操作”中选择功能，再点击“插入模板”。模板包括标题、文字标注、箭头、参考线、坐标范围、刻度间隔、对数坐标和图片保存等操作。</p>
<p>补充代码通过 <code>the_plt</code> 操作当前图形，并在绘图完成后执行。修改模板内容后，可点击“语法检查”检查写法，再点击“确定”保存；点击“取消”则放弃本次修改。无需补充操作时，保持空白即可。</p>
<pre>the_plt.title("利润比较 Profit comparison", fontsize=14)
the_plt.axhline(y=0, color="gray", linestyle="--")
the_plt.savefig("figure.svg", format="svg",
                bbox_inches="tight", dpi=300, transparent=False)</pre>
<p>在高级设置中，只填写文件名或相对保存路径时，图片会保存到用户的 Documents 文件夹下；填写绝对路径时，则保存到指定位置。添加标题后，程序会为其预留高度。语法检查不会执行代码；点击“出图...”后，补充代码才会运行，运行错误也会在此时提示。</p>
<p><img src="help/06-advanced.png" width="640" alt="高级设置与代码模板"></p>
<h2>5. Excel 和数据表</h2>
<p><b>导入数据：</b>在“数据到绘图”中点击“导入Excel/CSV...”并选择文件，或先从 Excel 复制数据，再点击“粘贴数据”。程序会打开导入预览，并自动判断首行是否为列名。</p>
<p>如果首行是表头，请勾选“首行是列名”；如果首行已经是数据，请取消勾选，程序会保留这一行并自动生成列名。自动判断可能有误，请核对预览和数据行数，再点击“导入数据”。点击“取消”则保留当前表格。</p>
<p><b>选择绘图内容：</b>选择图形类型，再选择横轴列和数值系列。“数值系列”是要绘制的数值列，不能与横轴使用同一列。每种图形都提供“加载案例”和“类型教程”，可先查看示例，再整理自己的数据。</p>
<p>饼状图只使用一个非负数值系列，且数值总和必须大于零；箱型图和直方图使用原始观测值，无需预先求平均。直方图无需指定横轴列，可以通过“分箱数”调整区间数量。饼状图扇区内的文字和区域图标签会根据背景深浅自动使用黑色或白色。</p>
<p><img src="help/10-data.png" width="680" alt="数据表、图形类型和数值系列选择"></p>
<p><b>编辑表格：</b>直接编辑单元格，双击列标题可修改列名，按住 Ctrl 并滚动鼠标滚轮可缩放表格。在选中的单元格处按 Ctrl+V，会从该位置开始粘贴全部行，不将首行提取为列名。</p>
<p>选中单元格后点击“删除行”或“删除列”，可删除其所在的整行或整列。删除前会显示待删除数量，并默认选中“取消”；确认后才执行删除。完成数据和样式设置后，点击“出图...”查看结果。</p>
<h2>6. 编辑、保存与重复使用</h2>
<p><b>阅读和编辑代码：</b>表达式、运行信息、LaTeX 转换和高级设置中的代码编辑区支持行号、语法高亮、Ctrl+鼠标滚轮缩放和“自动换行”。自动换行只影响显示，不改变代码内容。参数赋值框始终自动换行，不显示行号，也无需单独开启换行。出现语法错误时，程序会提示并标记出错行；底部状态栏显示当前操作状态。</p>
<p>“运行信息”区域中的代码默认锁定。勾选“编辑代码”后可以直接修改，此时出图、复制和保存都会使用编辑区中的代码。取消勾选后，程序会根据代码更新界面控件；如果无法恢复设置，会保留编辑状态并提示检查。</p>
<p><b>保存和复用代码：</b>按 Ctrl+S 或点击保存按钮即可保存。首次保存时，选择 <code>.py</code> 文件的位置和名称；已打开或保存过的代码会直接更新原文件。按钮会相应显示“保存代码(S)...”或“更新代码(S)”。加载案例后，再次保存时会按新文件处理。</p>
<p>“打开代码...”可恢复对应标签页中的表达式、中间变量、参数、样式和高级代码。“复制程序代码”可将完整脚本复制到剪贴板，供其他 Python 程序使用。</p>
<p><img src="help/02-formula.png" width="680" alt="运行信息中的代码编辑与保存"></p>
<p><b>保存图片：</b>出图后，使用预览窗口的工具栏缩放、平移或保存图片。关闭预览窗口后即可继续操作主界面。代码文件用于继续编辑和重复绘图，图片文件用于展示或论文排版。</p>
<h2>7. Python 与 Jupyter</h2>
<p>彼图也可以作为 Python 包使用。导入时会显示快速上手提示，列出常用函数及完整示例的生成方法：</p>
<pre>from betu import *
make_example('draw_lines')</pre>
<p><code>make_example</code> 接受一个示例名称，并打印带注释的完整代码。复制代码后即可运行或修改。支持的名称还包括 <code>draw_3D</code>、<code>draw_max_area</code>、<code>draw_detail_area</code>、<code>data_lines</code>、<code>plot_table</code>、<code>data_pie</code>、<code>data_box</code> 和 <code>data_hist</code> 等。</p>
<p>使用 <code>make_example('disconnected_modes')</code> 可查看同一模式的独立分块如何分别标注；使用 <code>make_example('smart_regions')</code> 可查看小区域引导线的用法。</p>
<p>如果使用 Jupyter，可在绘图前运行以下魔法命令，以提高单元格内图片的显示清晰度。该命令仅用于 Jupyter，不要写入普通的 <code>.py</code> 文件：</p>
<pre>%config InlineBackend.figure_format = 'retina' # 在 Jupyter 中显示高清图片</pre>
<p>下面以四模式利润比较为例：先导入彼图并设置高清显示，再定义表达式和参数。</p>
<p><img src="help/14-jupyter-setup.png" width="680" alt="在 Jupyter 中导入彼图并设置高清显示"></p>
<p>调用 <code>draw_detail_area</code> 并运行 <code>the_plt.show()</code> 后，图形会显示在单元格下方。下图展示了 <code>alpha</code> 与 <code>b</code> 变化时的利润大小关系，图例位于图外，小区域使用箭头标注。</p>
<p><img src="help/15-jupyter-plot.png" width="760" alt="Jupyter 中的关系区域图代码与运行结果"></p>
""",
    r"""
<h1>BeTu User Guide</h1>
<p>Yu-Xin Tian, PhD | Northeastern University | tianyuxin@mail.neu.edu.cn</p>
<p>BeTu supports numerical simulations from formulas and plots from Excel or tabular data. To get started, choose a tab, click “Load example”, then click “Plot...” to see the result.</p>
<p>For formula plots, follow this sequence: <b>Enter expressions → Recognize formulas → Set analysis parameters, ranges, and fixed values → Adjust plot styles → Plot</b>. For tabular data, see Section 5.</p>
<h2>1. Expressions and intermediate variables</h2>
<p>Enter one plot expression per line in the form <code>name = expression</code>. The name identifies a curve or mode and may use LaTeX enclosed in <code>$</code>. The expression uses Python syntax: <code>*</code> for multiplication and <code>**</code> for powers.</p>
<pre>$p_a$ = 2*a*x + b*x**2
p_n := 2*a + b - c**3/2
$\pi_R$ = integrate(p_n*t+b-3*t**2, (t, p_n-c, p_n+a*b))</pre>
<p>The line beginning with <code>p_n :=</code> defines an intermediate variable; the other two lines define plot expressions. Their mathematical forms are:</p>
<p><math>p_a = 2ax + bx^2</math></p>
<p><math>p_n = 2a+b-\frac{c^3}{2}</math></p>
<p><math>\pi_R = \int_{p_n-c}^{p_n+ab}(p_n t+b-3t^2)\,\mathrm{d}t</math></p>
<p>Define intermediate variables before or after the plot expressions that use them. Their names may contain uppercase and lowercase letters, underscores, and digits, but cannot begin with a digit; <code>p_n</code> is a valid name. Intermediate variables and plot names are excluded from the generated <code>symbols</code> declaration. Integration variables are included, while function names such as <code>integrate</code> and <code>sin</code> are not treated as parameters.</p>
<p>Intermediate variables support reassignment and indexing of arrays, lists, tuples, and other indexable objects. An ordinary call to <code>integrate(...)</code> usually returns an expression, so you cannot simply append <code>[0]</code>. Check the result type before using an index.</p>
<p>Click “Ω...” to open the symbol panel, then select a symbol to insert its Python syntax. The panel stays above the main window while allowing you to continue editing. Spaces are added where needed to keep inserted names separate from adjacent variables.</p>
<p>To convert an existing formula, click “LaTeX conversion...”. The source options are Mathematica, MATLAB, and General LaTeX, each with its own instructions. In Mathematica, select the formula and right-click “Copy As → LaTeX”. In MATLAB, copy the expression on the right side of an assignment. Paste it into the conversion window, convert it, and copy the result.</p>
<p>The output uses <code>**</code> for powers and changes the variable name <code>lambda</code> to <code>lamda</code> to comply with Python and SymPy syntax. LaTeX from different sources may be nonstandard or ambiguous, so conversion is not guaranteed to be fully accurate. Check variables, subscripts, superscripts, powers, and integration limits before using the result.</p>
<p><img src="help/04-latex.png" width="640" alt="LaTeX conversion window"></p>
<h2>2. Parameters and ranges</h2>
<p>After entering expressions, click “Recognize formulas”. For “Formula to Curves”, select one X parameter. For “Mode Comparison”, “Region Relationships”, and “Formula to 3D”, select two different parameters for the X and Y axes. Enter each range's start and end values separately. The curve step is calculated from the range and can also be adjusted manually.</p>
<p>In “Parameter values”, assign fixed values to the remaining parameters, separated by commas or new lines. For example:</p>
<pre>a=2, b=1, c=0.3</pre>
<p>Do not assign fixed values to the parameters selected for analysis. A variable used only within a definite integral and eliminated by integration remains in <code>symbols</code>, but does not appear in the axis parameter lists or require a fixed value.</p>
<p>Changing the analysis parameters updates the assignment box while temporarily retaining each parameter's last fixed value. For example, if <code>y=0.5</code> was assigned, selecting <code>y</code> for analysis hides that assignment. It returns when you choose another parameter to analyze. Each tab keeps its own assignment history. Parameters without a saved value start at <code>1.0</code>; adjust them to suit your model.</p>
<p><img src="help/02-formula.png" width="680" alt="Formula recognition, analysis ranges, and fixed parameter values"></p>
<p>Mode, relationship, and 3D plots default to <code>1000</code> samples along each axis. Change this in “Plot Style Settings → Axes and More”. Sampling precision controls the calculation grid and is separate from the DPI used when saving an image.</p>
<p>In “Region Relationships”, click “Load example” to populate the profit expressions and fixed parameters for four modes: NW, BW, NS, and BS. The X parameter is <code>alpha</code>, ranging from 0.7 to 0.8; the Y parameter is <code>b</code>, ranging from 0 to 0.08.</p>
<p><img src="help/08-detail.png" width="680" alt="Profit relationship regions for four modes"></p>
<p>“Formula to 3D” uses the same expressions, fixed parameters, and ranges, with profit on the Z axis. Click “Load example”, then “Plot...” to see how the two parameters affect each mode's profit.</p>
<p><img src="help/09-surface.png" width="680" alt="Profit surfaces for four modes"></p>
<h2>3. Plot Style Settings</h2>
<p>Click “Plot Style Settings...” to adjust general settings, individual curves or regions, and the legend in one window. Click “OK” to apply your changes.</p>
<table border="1" cellpadding="8" cellspacing="0">
<tr><th>Page</th><th>Settings</th></tr>
<tr><td>General</td><td>Title, axis labels, overall font size, figure dimensions, and text rotation. Leave the title field blank to omit the title.</td></tr>
<tr><td>Series / Regions</td><td>Select a curve or region, then adjust its color, line style, line width, marker, or hatch. Intermediate variables are excluded.</td></tr>
<tr><td>Legend</td><td>Visibility, position, number of columns, font size, and spacing. The default is one column.</td></tr>
<tr><td>Axes and More</td><td>Axis limits, text spacing, sampling precision, small-region filtering, 3D view, and image destination. Available options depend on the plot type.</td></tr>
</table>
<p>The color list shows swatches, the line-style list shows stroke previews, and the marker list shows shapes and names. Select a curve or region to edit its style. Your changes are retained when you select another item.</p>
<p><img src="help/05-style-series.png" width="600" alt="Individual curve and region styles"></p>
<p>Every tab provides a “Show legend” checkbox. Mode Comparison hides the legend by default; Region Relationships places it outside the plot on the right. Mode, relationship, and 3D plots do not display a background coordinate grid.</p>
<p>Mode and relationship style lists use “Region 1”, “Region 2”, and so on. Mode regions follow the order of the plot expressions; relationship regions are updated from the actual plot result.</p>
<p><b>Filter small fragments:</b> In “Axes and More”, set “Minimum region area fraction”, corresponding to the Python parameter <code>dropout</code>. Both mode and relationship plots default to <code>0.001</code>, which hides individual components smaller than 0.1% of the full plot area. Use <code>0.01</code> for 1%, or <code>0</code> to disable filtering.</p>
<p>Area fractions are estimated from the sampling grid, with each disconnected component checked separately. Components below the threshold have no fill, boundary, label, or leader arrow; the rest remain visible. If a mode occupies several disconnected components, each retained component receives a label, with one legend entry for the mode. Higher <code>dropout</code> values hide more regions.</p>
<p><b>Position labels:</b> For retained regions, the program first tries to place each label inside its region. If it will not fit, the label is moved outside the plot and connected with an arrow. An arrow also appears when you manually offset a label beyond its region. Disable automatic placement in “Axes and More”, or adjust label offsets in the region style settings.</p>
<h2>4. Advanced Settings</h2>
<p>For further customization, open “Advanced settings...”, choose a function from “Common actions”, and click “Insert template”. Templates cover titles, text annotations, arrows, reference lines, axis limits, tick intervals, logarithmic axes, and image saving.</p>
<p>Use <code>the_plt</code> to work with the current figure. This code runs after the plot is created. Edit the template, click “Check syntax” if needed, then click “OK” to save. “Cancel” discards your changes. Leave the editor blank if no additional operations are needed.</p>
<pre>the_plt.title("Profit comparison", fontsize=14)
the_plt.axhline(y=0, color="gray", linestyle="--")
the_plt.savefig("figure.svg", format="svg",
                bbox_inches="tight", dpi=300, transparent=False)</pre>
<p>In Advanced Settings, a filename or relative save path is resolved under your Documents folder; an absolute path saves to the specified location. Extra space is reserved when you add a title. Syntax checks do not execute the code. The code runs when you click “Plot...”, and any runtime errors are reported then.</p>
<p><img src="help/06-advanced.png" width="640" alt="Advanced settings and code templates"></p>
<h2>5. Excel and tables</h2>
<p><b>Import data:</b> In “Data to Plots”, click “Import Excel/CSV...” and select a file, or copy cells from Excel and click “Paste data”. An import preview opens and automatically estimates whether the first row contains column names.</p>
<p>Check “First row contains column names” if the first row is a header. If it contains data, uncheck this option to retain the row and generate column names. Automatic detection can be wrong, so check the preview and data row count before clicking “Import Data”. “Cancel” leaves the current table unchanged.</p>
<p><b>Choose what to plot:</b> Select a chart type, an X column, and the numeric series to plot. A numeric series is a column of values; it cannot also be the selected X column. Every chart type provides an example and a guide to help you organize your own data.</p>
<p>Pie charts require exactly one nonnegative numeric series with a positive total. Box plots and histograms use raw observations without averaging them first. Histograms do not require an X column; adjust the bin count to change the number of intervals. Text inside pie slices and region labels automatically uses black or white for contrast.</p>
<p><img src="help/10-data.png" width="680" alt="Data table, chart type, and numeric series selection"></p>
<p><b>Edit the table:</b> Edit cells directly, double-click a column heading to rename it, and use Ctrl+mouse wheel to zoom. Pressing Ctrl+V at a selected cell pastes all copied rows from that position without extracting the first row as column names.</p>
<p>Use “Delete Rows” or “Delete Columns” to remove the entire rows or columns containing selected cells. A confirmation dialog shows how many will be deleted and defaults to “Cancel”. Once your data and styles are ready, click “Plot...” to view the result.</p>
<h2>6. Editing and saving</h2>
<p><b>Read and edit code:</b> The formula, output, LaTeX conversion, and advanced editors provide line numbers, syntax highlighting, Ctrl+mouse wheel zoom, and a “Word wrap” option. Wrapping changes the display, not the code. The assignment box always wraps and has no line numbers or wrap switch. Syntax errors identify and highlight the affected line; the status bar shows the current operation.</p>
<p>Generated code in the output area is locked by default. Check “Edit code” to modify it; plotting, copying, and saving will then use the editor's content. Uncheck the option to update the interface controls from the code. If the settings cannot be restored, editing remains enabled and a message asks you to check the code.</p>
<p><b>Save and reuse code:</b> Press Ctrl+S or click the save button. When saving for the first time, choose a filename and location for the <code>.py</code> file. Code that has already been opened or saved updates the same file. The button changes between “Save Code (S)...” and “Update Code (S)” accordingly. After loading an example, the next save is treated as a new file.</p>
<p>“Open code...” restores the corresponding tab's expressions, intermediate variables, parameters, styles, and advanced code. “Copy Python code” copies the complete script to the clipboard for use in another Python program.</p>
<p><img src="help/02-formula.png" width="680" alt="Editing and saving generated code"></p>
<p><b>Save images:</b> Use the plot preview toolbar to zoom, pan, or save the image. Close the preview to continue working in the main window. Save code to edit or reproduce a plot later; save an image to share the result or include it in a paper.</p>
<h2>7. Python and Jupyter</h2>
<p>BeTu can also be used as a Python package. Importing it displays quick-start tips, common functions, and instructions for generating complete examples:</p>
<pre>from betu import *
make_example('draw_lines')</pre>
<p><code>make_example</code> accepts an example name and prints the full commented code, ready to copy, run, or modify. Other supported names include <code>draw_3D</code>, <code>draw_max_area</code>, <code>draw_detail_area</code>, <code>data_lines</code>, <code>plot_table</code>, <code>data_pie</code>, <code>data_box</code>, and <code>data_hist</code>.</p>
<p>Use <code>make_example('disconnected_modes')</code> to see how disconnected components of a mode are labeled, or <code>make_example('smart_regions')</code> to explore leader arrows for small regions.</p>
<p>In Jupyter, run the following magic command before plotting to improve the resolution of inline figures. This command is for Jupyter only; do not place it in an ordinary <code>.py</code> file:</p>
<pre>%config InlineBackend.figure_format = 'retina' # High-resolution Jupyter figures</pre>
<p>The example below compares profits for four modes. First import BeTu, enable high-resolution output, and define the expressions and parameters.</p>
<p><img src="help/14-jupyter-setup.png" width="680" alt="Importing BeTu and enabling high-resolution output in Jupyter"></p>
<p>Call <code>draw_detail_area</code>, then <code>the_plt.show()</code> to display the figure below the cell. The result shows how profit rankings vary with <code>alpha</code> and <code>b</code>, with a legend outside the plot and arrows identifying small regions.</p>
<p><img src="help/15-jupyter-plot.png" width="760" alt="Relationship plot code and output in Jupyter"></p>
""",
)
HELP_CSS = "body { color:#263445; font-family: sans-serif; font-size:11pt; } h1 { color:#175b88; } h2 { color:#137c98; margin-top:18px; } pre { background-color:#edf3f8; font-family:Consolas,monospace; white-space:pre-wrap; } code { color:#8b3e69; font-family:Consolas,monospace; } th { background-color:#e8f0f6; }"
ABOUT_HTML = (
    "<h1>彼图 BeTu</h1><p><b>版本 1.0.0</b></p><p>Be better tool for U!</p><p>科研仿真与 Excel 数据绘图工具</p><p><b>作者：</b>田雨鑫<br><b>单位：</b>东北大学<br><b>学位：</b>博士<br><b>邮箱：</b>tianyuxin@mail.neu.edu.cn</p>",
    "<h1>BeTu</h1><p><b>Version 1.0.0</b></p><p>Be better tool for U!</p><p>Scientific simulation and Excel data plotting</p><p><b>Author:</b> Yu-Xin Tian<br><b>Affiliation:</b> Northeastern University<br><b>Degree:</b> PhD<br><b>Email:</b> tianyuxin@mail.neu.edu.cn</p>",
)
CHART_HELP_TEMPLATE = (
    "<h1>{name}：用途与数据准备</h1><p>{guide}</p><h2>加载并运行案例</h2><p>点击下方的“加载案例”，程序会填入示例数据，并选好横轴列和数值系列。返回主界面后，点击“出图...”查看结果，再按需要修改数据或样式。</p><p>如果使用 Python，可运行以下代码，生成带注释的完整绘图示例：</p><pre>from betu import *\nmake_example('data_{kind}')</pre>",
    "<h1>{name}: purpose and data preparation</h1><p>{guide}</p><h2>Load and run an example</h2><p>Click “Load example” below to populate sample data and select the X column and numeric series. Back in the main window, click “Plot...” to view the result, then adjust the data or styles as needed.</p><p>In Python, run the following code to generate a complete commented plotting example:</p><pre>from betu import *\nmake_example('data_{kind}')</pre>",
)

# 绘图风格设置窗口：分页名称、系列选择提示和控件选项。
TEXT.update(
    {
        "style": ("绘图风格设置...", "Plot Style Settings..."),
        "style_common": ("公共设置", "General"),
        "style_series": ("曲线／区域样式", "Series / Regions"),
        "style_legend": ("图例设置", "Legend"),
        "style_more": ("坐标与其他设置", "Axes and More"),
        "style_select": ("选择曲线／区域", "Select series / region"),
        "style_hint": (
            "先选中一条曲线或一个区域，再修改它的样式；切换后会保留修改。",
            "Select a series or region, then edit its style. Changes are retained when switching.",
        ),
        "title_hint": ("留空则不显示标题", "Leave blank for no title"),
        "figure_width": ("图片宽度（英寸）", "Width (inches)"),
        "figure_height": ("图片高度（英寸）", "Height (inches)"),
        "series_number": ("第 {number} 条", "Series {number}"),
        "region_number": ("区域 {number}", "Region {number}"),
        "none_option": ("无", "None"),
        "auto_option": ("自动", "Auto"),
        "pick_color": ("选择颜色...", "Choose Color..."),
        "line_style_custom": ("自定义虚线 {number}", "Custom dashes {number}"),
        "series_preview": ("样式预览", "Style preview"),
        "width": ("宽", "Width"),
        "height": ("高", "Height"),
        "follow_font_size": ("跟随整体字号", "Use global font size"),
        "browse": ("选择文件...", "Choose File..."),
        "save_picture": ("选择图片保存位置", "Choose image destination"),
        "no_auto_save": (
            "留空则不自动保存图片",
            "Leave blank to skip automatic saving",
        ),
        "image_filter": (
            "SVG 矢量图 (*.svg);;PNG 图片 (*.png);;PDF 矢量图 (*.pdf);;JPEG 图片 (*.jpg)",
            "SVG vector image (*.svg);;PNG image (*.png);;PDF vector image (*.pdf);;JPEG image (*.jpg)",
        ),
        "style_empty": (
            "输入绘图表达式或选择数据系列后，这里会自动显示对应名称。中间变量不列入。",
            "Enter plot expressions or select data series to populate this list. Intermediate variables are excluded.",
        ),
        "style_regions_pending": (
            "先出图一次，列表就会按实际生成的关系区域显示。修改公式或分析范围后，请重新出图。",
            "Plot once to list the actual relationship regions. Plot again after changing formulas or analysis ranges.",
        ),
        "delete_rows": ("删除行", "Delete Rows"),
        "delete_columns": ("删除列", "Delete Columns"),
        "select_cells_first": (
            "请先选中要删除的行、列或其中的单元格。",
            "Select the rows, columns or their cells first.",
        ),
        "confirm_delete": ("确认删除", "Delete"),
        "confirm_delete_rows": (
            "将删除选中的 {count} 行及其中全部数据。确定删除吗？",
            "Delete the {count} selected rows and all their data?",
        ),
        "confirm_delete_columns": (
            "将删除选中的 {count} 列及其中全部数据。确定删除吗？",
            "Delete the {count} selected columns and all their data?",
        ),
    }
)
PARAMETER_COMMENTS["title"] = "图表标题"
PARAMETER_ENGLISH["title"] = "Chart title"
PARAMETER_COMMENTS.update(
    fsize="整体字号",
    figsize="图片尺寸（英寸）",
    linestyles="线型",
    linewidth="线宽",
    markers="标记形状",
    markersize="标记大小",
    colors="颜色",
    save_dir="自动保存图片",
    precision="采样点数（越高越细）",
    density="曲面线网格密度",
    color_alpha="曲面不透明度（0～1）",
    x_lim="横轴显示范围",
    y_lim="纵轴显示范围",
    z_lim="竖轴显示范围",
    elevation="视角：上下俯仰",
    azimuth="视角：左右旋转",
    roll="视角：画面倾斜",
    pattern_moves="区域标签位置偏移",
    pattern_colors="区域标签背景颜色",
    switchcolor="区域文字黑白切换阈值",
)
STYLE_LINE_CHOICES = [
    (("实线 ━━━", "Solid ━━━"), "solid"),
    (("虚线 ┅┅┅", "Dashed ┅┅┅"), "dashed"),
    (("点线 ·····", "Dotted ·····"), "dotted"),
    (("点划线 ┅·┅", "Dash-dot ┅·┅"), "dashdot"),
]
STYLE_MARKER_CHOICES = [
    None,
    "o",
    "s",
    "*",
    "P",
    "X",
    "D",
    "p",
    "x",
    "8",
    "2",
    "H",
    "+",
    "|",
    "<",
    ">",
    "^",
    "v",
    "d",
    "3",
    ".",
]
STYLE_COLOR_CHOICES = [
    "navy",
    "blue",
    "teal",
    "green",
    "brown",
    "purple",
    "crimson",
    "orange",
    "gray",
    "black",
    "white",
]
STYLE_NUMBER_CHOICES = [
    (("罗马数字", "Roman numerals"), "roman"),
    (("字母", "Letters"), "letter"),
    (("阿拉伯数字", "Numbers"), "number"),
]
STYLE_COMMON_KEYS = [
    "title",
    "x_name",
    "y_name",
    "z_name",
    "fsize",
    "figsize",
    "xt_rotation",
    "yt_rotation",
    "xrotation",
    "yrotation",
    "zrotation",
]
STYLE_SERIES_KEYS = [
    "colors",
    "linestyles",
    "linewidth",
    "markers",
    "markersize",
    "patterns",
    "texts",
    "pattern_colors",
    "pattern_moves",
]
# Qt 全局外观；选中框使用原生对勾，避免叉号。
STYLE_SHEET = """
QMainWindow, QDialog { background: #f4f7fb; }
QWidget { color: #263445; }
QLabel#brand { color: #175b88; font-size: 26px; font-weight: 700; }
QLabel#slogan { color: #63768a; font-size: 14px; }
QTabWidget::pane { background: white; border: 1px solid #d6e0ea; border-radius: 8px; padding: 12px; }
QTabBar::tab { padding: 12px 20px; background: #e8eef5; border: 0; margin-right: 3px; }
QTabBar::tab:selected { background: white; color: #126aa0; border-top: 3px solid #168ba2; }
QPushButton { background: white; border: 1px solid #bfcfdd; border-radius: 6px; padding: 9px 13px; }
QPushButton:hover { background: #eaf5fc; border-color: #439bbf; }
QPushButton:pressed { background: #d7ecf6; }
QPushButton#primary { background: #137c98; border-color: #137c98; color: white; font-weight: 600; padding: 13px; }
QPushButton:disabled { color: #9cabb9; background: #f4f6f8; }
QLineEdit, QPlainTextEdit, QTextBrowser, QListWidget, QTableWidget { background: white; border: 1px solid #cbd7e2; border-radius: 5px; selection-background-color: #cbe6f5; selection-color: #163047; padding: 5px; }
QComboBox, QSpinBox { background: white; border: 1px solid #cbd7e2; border-radius: 4px; padding: 6px; }
QHeaderView::section { background: #e8f0f6; padding: 7px; border: 1px solid #d2dfe9; }
QTableWidget { gridline-color: #c7d4df; alternate-background-color: #f4f8fc; }
QStatusBar { color: #526679; }
QScrollArea { border: none; }
"""
TEXT["color_index"] = (
    "选择要修改的颜色序号（从 1 开始）",
    "Color index to edit (starting at 1)",
)
GENERAL_GUIDE = (
    """操作顺序：输入公式 → 公式识别 → 选择分析参数和范围 → 参数赋值 → 调整样式 → 出图。
:= 定义的中间变量可在绘图表达式前后书写；依赖会自动排序，重复赋值保留先后顺序。
数组索引只适用于可索引对象。普通 integrate 返回表达式，不能直接取 [0]；cse 等函数可返回元组或列表。
模式比较、关系区域比较、三维图不显示坐标网格。所有图形都可控制图例显示。
图例和高级窗口点击“确定”才保存修改；出图窗口独占，关闭后返回主界面。
保存默认生成 .py，打开后恢复表达式、中间变量、参数、样式和高级代码。
数据表支持 Excel/CSV 导入、粘贴、直接编辑，Ctrl+滚轮缩放；每种图形都有案例和教程。
高级代码使用 the_plt；相对图片路径默认在 Documents。代码在本机执行，请仅运行可信代码。""",
    """Workflow: Enter formulas → Recognize → Choose analysis parameters and ranges → Set fixed values → Adjust styles → Plot.
Intermediates use := and may appear before or after plot expressions. Dependencies are sorted; repeated assignments retain order.
Indexing requires an indexable object. integrate normally returns an expression, not a list; cse can return tuples/lists.
Mode, relationship and 3D plots have no coordinate grid. Every tab can toggle the legend.
Confirm settings with OK. Plot previews are modal; close the preview to return to the main window.
Save creates a .py script; Open restores formulas, intermediates, parameters, styles and advanced code.
Import Excel/CSV, paste or edit cells, and zoom with Ctrl+wheel. Every chart type has a sample and guide.
Advanced code uses the_plt. Relative image paths use Documents. Python runs locally; execute only trusted code.""",
)
# 包导入时的快速上手提示（终端、Jupyter）。
IMPORT_TIPS = """
彼图 BeTu 1.0.0 — Be better tool for U!
科研仿真与 Excel 数据绘图，快速上手：
  makefig()                         打开中英文图形界面
  make_example('draw_lines')         公式到曲线（单参数仿真）
  make_example('draw_max_area')      模式比较（最大值区域）
  make_example('draw_detail_area')   关系区域比较
  make_example('draw_3D')            公式到三维图
  make_example('data_lines')         根据数据绘制曲线
  make_example('plot_table')         Excel/表格数据绘图
  make_example('data_pie')           饼图；另有 data_bar、data_barh、data_box、data_hist、data_scatter、data_line
  make_example('disconnected_modes') 同一模式被分隔后逐块标注
  make_example('smart_regions')      小区域标记自动避让与引导线
以上命令打印带注释的完整代码，可复制后修改；read_table(path) 可读取 Excel/CSV。
在 Jupyter 单元格开头加入以下魔法命令，高清显示图形：
%config InlineBackend.figure_format = 'retina' # 在 Jupyter 中显示高清图片
普通 .py 脚本中不要使用上述魔法命令。
"""

# 绘图核心、表格校验与图例校验提示。
TEXT.update(
    {
        "message_0": (
            "排列的长度减1应等于符号组合的长度",
            "Permutation length minus one must equal the symbol combination length.",
        ),
        "message_1": (
            "请至少提供一个非空数据系列。",
            "Provide at least one nonempty data series.",
        ),
        "message_2": (
            "系列 {v0} 没有可绘制的有效数值。",
            "Series {v0} has no valid values to plot.",
        ),
        "message_3": (
            "请提供表达式、分析变量和 [起点, 终点, 步长]。",
            "Provide expressions, an analysis variable and [start, end, step].",
        ),
        "message_4": (
            "范围必须为有限数值，步长不能为零且方向必须与起止点一致。",
            "Use a finite range and a nonzero step in the direction of the range.",
        ),
        "message_5": (
            "采样点超过一百万，请增大步长。",
            "Over one million samples requested; increase the step.",
        ),
        "message_6": (
            "系列 {v0} 存在未赋值参数：{v1}",
            "Series {v0} has unassigned parameters: {v1}",
        ),
        "message_7": (
            "系列 {v0} 在所选范围内没有有效数值。",
            "Series {v0} has no valid values in the selected range.",
        ),
        "message_8": (
            "注意：请输入表达式！ Note: Please enter expressions!",
            "Enter expressions.",
        ),
        "message_9": (
            "注意：请输入参数及赋值！ Note: Please input parameters and assign values!",
            "Provide parameter assignments.",
        ),
        "message_10": (
            "注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!",
            "Provide analysis variables and their ranges.",
        ),
        "message_11": (
            "注意：请输入表达式！ Note: Please enter expressions!",
            "Enter expressions.",
        ),
        "message_12": (
            "注意：请输入参数及赋值！ Note: Please input parameters and assign values!",
            "Provide parameter assignments.",
        ),
        "message_13": (
            "注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!",
            "Provide analysis variables and their ranges.",
        ),
        "message_14": (
            "表达式个数必须大于2！ The number of expressions must be greater than 2!",
            "At least two expressions are required.",
        ),
        "message_15": (
            "没有可用数据，请先导入或粘贴数据，并核对首行是否为列名。",
            "Import or paste data and check whether the first row contains column names.",
        ),
        "message_16": ("表格为空。", "The table is empty."),
        "message_17": ("列{v0}", "Column {v0}"),
        "message_18": ("列{v0}", "Column {v0}"),
        "message_19": ("剪贴板没有表格数据。", "The clipboard contains no table data."),
        "message_20": (
            "请选择 Excel (.xlsx/.xlsm/.xls)、CSV 或 TSV 文件。",
            "Select an Excel (.xlsx/.xlsm/.xls), CSV or TSV file.",
        ),
        "message_21": (
            "第 {v0} 行「{v1}」不是有效数字：{v2!r}。请修改该单元格或取消此系列。",
            "Row {v0}, column {v1}: invalid number {v2!r}. Edit the cell or deselect the series.",
        ),
        "message_22": ("不支持的图形类型。", "Unsupported chart type."),
        "message_23": (
            "表格必须有数据行，且所有列长度相同。",
            "The table needs data rows and equally sized columns.",
        ),
        "message_24": ("所选横轴列不存在。", "The selected X column does not exist."),
        "message_25": (
            "请至少选择一个数据系列；系列不能重复，也不能与横轴相同。",
            "Choose at least one series, with no duplicates or X column.",
        ),
        "message_26": (
            "饼状图只能选择一个数值系列；横轴列用作扇区名称。",
            "Pie charts require one numeric series; the X column supplies slice names.",
        ),
        "message_27": (
            "散点图需要选择一列数值作为横轴。",
            "Scatter plots require a numeric X column.",
        ),
        "message_28": (
            "直方图分箱数必须是正整数。",
            "Histogram bins must be a positive integer.",
        ),
        "message_29": (
            "系列「{v0}」没有有效数值。",
            "Series {v0} has no valid values.",
        ),
        "message_30": (
            "饼状图数据不能为负数，且总和必须大于零。",
            "Pie values must be nonnegative with a positive total.",
        ),
        "message_31": (
            "系列「{v0}」没有横轴和纵轴同时有效的数据点。",
            "Series {v0} has no points with both valid X and Y values.",
        ),
        "message_32": ("数值", "Value"),
        "message_33": ("序号", "Index"),
        "message_34": ("类别", "Category"),
        "message_35": ("频数", "Frequency"),
        "message_36": ("数值", "Value"),
        "message_37": ("样式列表不能为空。", "Style lists must not be empty."),
        "message_38": ("请选择有效的图例位置。", "Choose a valid legend location."),
        "message_39": (
            "{v0} 必须是有效的正数或非负间距。",
            "{v0} must be positive or a nonnegative spacing.",
        ),
        "message_40": (
            "图例列数必须是正整数。",
            "Legend columns must be a positive integer.",
        ),
    }
)

# 原说明书论文案例的四种模式；用于第 3 章教程。
PAPER_FORMULAS = "$\\pi_r^{NW}$ = E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2)\n$\\pi_r^{BW}$ = E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2)\n$\\pi_r^{NS}$ = E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2)\n$\\pi_r^{BS}$ = E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2)"
PAPER_ASSIGNS = dict(
    alpha=0.9, c_n=0.2, c_r=0.1, delta=0.8, E=2.0, e_n=1.0, e_r=0.6, k=1.1, p_e=0.1
)
# 论文案例的区域 II、III 向图内移动，其余区域使用零偏移。
PAPER_LABEL_MOVES = ((0, 0), (-0.018, -0.007), (0.004, -0.013), (0, 0), (0, 0), (0, 0))

# 符号浮窗的紧凑按钮间距。
SYMBOL_STYLE = "QPushButton { padding: 4px 5px; min-width: 45px; }"
TEXT["editor_tip"] = (
    "Ctrl+鼠标滚轮缩放；左侧显示行号，错误行以红色标记。",
    "Ctrl+wheel zooms. Line numbers appear on the left; errors are marked in red.",
)
TEXT["line_error"] = ("第 {line} 行：{message}", "Line {line}: {message}")
# 主界面紧凑尺寸；对话框编辑区域仍可放大。
STYLE_SHEET += """
QMainWindow QPushButton { padding: 6px 9px; }
QMainWindow QPushButton#primary { padding: 8px 9px; }
QMainWindow QTabBar::tab { padding: 6px 10px; }
QMainWindow QComboBox, QMainWindow QSpinBox { padding: 4px; }
QComboBox#languageChoice { padding: 4px 30px 4px 12px; min-width: 104px; }
QComboBox QAbstractItemView { background: white; color: #263445; padding: 4px; border: 1px solid #bfcfdd; selection-background-color: #dceef8; selection-color: #175b88; }
QComboBox QAbstractItemView::item { min-height: 30px; padding: 3px 8px; }
QLabel#brand { font-size: 22px; }
"""
TEXT["insert"] = ("插入模板", "Insert template")
TEXT["more_templates"] = ("常用操作", "Common actions")
# 高级设置“更多常用操作”下拉框：名称（中英文）及插入代码。
ADVANCED_SNIPPETS = [
    (("设置坐标范围", "Axis limits"), "the_plt.xlim(0, 1)\nthe_plt.ylim(0, 10)\n"),
    (
        ("设置刻度间隔", "Tick intervals"),
        "from matplotlib.ticker import MultipleLocator\nthe_plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))\n",
    ),
    (
        ("添加水平参考线", "Horizontal reference"),
        'the_plt.axhline(y=0, color="gray", linestyle="--", linewidth=1)\n',
    ),
    (
        ("添加竖直参考线", "Vertical reference"),
        'the_plt.axvline(x=0.5, color="gray", linestyle="--", linewidth=1)\n',
    ),
    (
        ("添加箭头标注", "Arrow annotation"),
        'the_plt.annotate("Note", xy=(0.5, 0.5), xytext=(0.7, 0.8), xycoords="axes fraction", textcoords="axes fraction", arrowprops=dict(arrowstyle="->", color="black"))\n',
    ),
    (("纵轴使用对数坐标", "Logarithmic Y axis"), 'the_plt.yscale("log")\n'),
    (
        ("隐藏上方和右侧边框（二维图）", "Hide top/right spines (2D)"),
        'the_plt.gca().spines["top"].set_visible(False)\nthe_plt.gca().spines["right"].set_visible(False)\n',
    ),
    (
        ("图例放到图外右侧", "Legend outside right"),
        'apply_legend(the_plt.gca(), loc="outside right", ncol=1, fontsize=14)\n',
    ),
    (
        ("调整坐标轴名称", "Axis labels"),
        'the_plt.xlabel("X", fontsize=14)\nthe_plt.ylabel("Y", fontsize=14)\n',
    ),
    (
        ("保存高清 PNG", "Save high-resolution PNG"),
        'the_plt.savefig("filename.png", format="png", bbox_inches="tight", dpi=300, transparent=False)\n',
    ),
    (
        ("保存 PDF 矢量图", "Save vector PDF"),
        'the_plt.savefig("filename.pdf", format="pdf", bbox_inches="tight", transparent=False)\n',
    ),
    (
        ("设置图形背景颜色", "Figure background"),
        'the_plt.gcf().set_facecolor("white")\nthe_plt.gca().set_facecolor("#f8fafc")\n',
    ),
]

# 原符号面板的按钮文字原样保留；右侧内容为点击后插入的代码。
SYMBOL_BUTTONS = [
    ("+", "+"),
    ("-", "-"),
    ("×", "*"),
    ("÷", "/"),
    ("_", "_"),
    ("^", "**"),
    ("(", "("),
    (")", ")"),
    ("=", "="),
    ("α", "alpha"),
    ("β", "beta"),
    ("γ", "gamma"),
    ("δ", "delta"),
    ("ε", "epsilon"),
    ("ζ", "zeta"),
    ("η", "eta"),
    ("θ", "theta"),
    ("ι", "iota"),
    ("κ", "kappa"),
    ("λ", "lamda"),
    ("μ", "mu"),
    ("ν", "nu"),
    ("ξ", "xi"),
    ("ο", "omicron"),
    ("π", "pi"),
    ("ρ", "rho"),
    ("σ", "sigma"),
    ("τ", "tau"),
    ("υ", "upsilon"),
    ("φ", "phi"),
    ("χ", "chi"),
    ("ψ", "psi"),
    ("ω", "omega"),
    ("Α", "Alpha"),
    ("Β", "Beta"),
    ("Γ", "Gamma"),
    ("Δ", "Delta"),
    ("Ε", "Epsilon"),
    ("Ζ", "Zeta"),
    ("Η", "Eta"),
    ("Θ", "Theta"),
    ("Ι", "Iota"),
    ("Κ", "Kappa"),
    ("Λ", "Lambda"),
    ("Μ", "Mu"),
    ("Ν", "Nu"),
    ("Ξ", "Xi"),
    ("Ο", "Omicron"),
    ("Π", "Pi"),
    ("Ρ", "Rho"),
    ("Σ", "Sigma"),
    ("Τ", "Tau"),
    ("Υ", "Upsilon"),
    ("Φ", "Phi"),
    ("Χ", "Chi"),
    ("Ψ", "Psi"),
    ("Ω", "Omega"),
    ("e", "exp(1)"),
    ("e^x", "exp(x)"),
    ("|x|", "Abs(x)"),
    ("∞", "oo"),
    ("√", "sqrt(x)"),
    ("n√", "root(x,n)"),
    ("ln", "log(x)"),
    ("log", "log(x, b)"),
    ("lg", "log(x, 10)"),
    ("∫", "integrate(f, (x, a, b))"),
    ("∂", "diff(f, x)"),
    ("lim", "limit(f, x, x0)"),
    ("∑", "summation(f, (i, a, b))"),
    ("∏", "product(f, (i, a, b))"),
    ("sin", "sin(x)"),
    ("cos", "cos(x)"),
    ("tan", "tan(x)"),
    ("csc", "csc(x)"),
    ("sec", "sec(x)"),
    ("cot", "cot(x)"),
    ("sinh", "sinh(x)"),
    ("cosh", "cosh(x)"),
    ("tanh", "tanh(x)"),
    ("coth", "coth(x)"),
    ("分段", "Piecewise((f1, con1), (f2, cons), ...)"),
    ("x/y", "Rational(x,y)"),
    ("⌊x⌋", "floor(x)"),
    ("⌈x⌉", "ceiling(x)"),
    ("取模", "Mod(x, n)"),
]
SYMBOL_STYLE = "QPushButton { padding: 3px 2px; min-width: 28px; font-size: 12px; }"

TEXT["copy_code"] = ("复制程序代码", "Copy Python code")
TEXT["code_copied"] = ("完整程序代码已复制", "Complete Python code copied")

# 占位引导语仅压缩对齐空格，不改变文字内容。
import re as _re

FORMULA_GUIDE = tuple(_re.sub(r" {8,}", "    ", text) for text in FORMULA_GUIDE)
# 表达式框内的简短提示；详细规则见 FORMULA_GUIDE 和使用帮助。
FORMULA_PLACEHOLDER = (
    """逐行输入：名称 = 表达式
例如：$p_a$ = 2*a*x + b*x**2
中间变量：p := a+b，位置不限。
变量名只用字母、数字和下划线，不能以数字开头。
“Ω...”插入符号与函数；Ctrl+滚轮缩放。""",
    """One expression per line: name = expression
Example: $p_a$ = 2*a*x + b*x**2
Intermediate: p := a+b (may appear anywhere).
Use letters, digits and underscores; no leading digit.
“Ω...” inserts symbols/functions. Ctrl+wheel zooms.""",
)

# core_functions.py 各函数的原始参数说明。
CORE_FUNCTION_DOCS = {
    "draw_detail_area": '\n        - expressions: Symbol表达式，字典形式传入。\n        - assigns: 表达式参数赋值，字典形式。\n        - the_var_x/the_var_y: 要分析的参数1/2；\n        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]\n        - x_name: x轴名称标签。\n        - y_name: y轴名称标签。\n        - fsize: 图片中字号的大小，默认值为14。\n        - text_fsize_add: 区域标记文本字体大小相对于其他部分字体字号增加量，默认0，范围[-fsize+1, oo]。\n        - save_dir=None: 图片保存路径，字符串。默认None，不保存。\n        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。\n        - figsize: 图片的大小，写成`[宽, 高]`的形式。\n        - colors: 各区域的配色。\n        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。\n        - linewidth: 线粗。\n        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。\n        - prefix: 前缀。可以是"区域"也可以是"Region"，默认"Region"。\n        - numbers: 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。默认"roman"。\n        - switchcolor=112, 根据背景颜色的亮度，自动切换字体黑白色。默认：如果背景亮度低于112，字体用白色。\n        - legend_options: Matplotlib图例参数字典。\n    ',
    "draw_max_area": "\n        - expressions: Symbol表达式，字典形式传入。\n        - assigns: 表达式参数赋值，字典形式。\n        - the_var_x/the_var_y: 要分析的参数1/2；\n        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]\n        - x_name: x轴名称标签，默认'x。\n        - y_name: y轴名称标签，默认'y'。\n        - fsize: 图片中字号的大小，默认值为14。\n        - texts: 表达式expressions中的函数值若分别达到最大，则相应区域应分别标记的文本，以`[]`形式写。默认None，按照expressions提供的名字标记。注意：标签个数和expressions中的函数顺序要对应。\n        - text_fsize_add: 区域标记文本字体大小相对于其他部分字体字号增加量，默认0，范围[-fsize+1, oo]。\n        - save_dir=None: 图片保存路径，字符串。默认None，不保存。\n        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。\n        - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。\n        - colors: 各区域的配色。\n        - patterns: 为每个区域设置填充图案（例如斜线、网格等），以列表形式提供，例如['/', '\\', 'x', 'o']。\n        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。\n        - linewidth: 线粗，默认0.1。\n        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。\n        - switchcolor=112, 根据背景颜色的亮度，自动切换字体黑白色。默认：如果背景亮度低于112，字体用白色。\n    ",
    "draw_3D": "\n    - expressions: Symbol表达式，字典形式传入。（必须）\n    - assigns: 表达式参数赋值，字典形式。\n    - the_var_x/the_var_y: 要分析的参数1/2；\n    - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]\n    - x_name: x轴名称标签，默认'x'。\n    - y_name: y轴名称标签，默认'y'。\n    - z_name: z轴名称标签，默认'z'。\n    - save_dir=None: 图片保存路径，字符串。默认None，不保存。\n    - color_alpha: 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。默认取0.8。可以是列表。\n    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。\n    - linewidth: 线粗，默认值为0.2。\n    - fsize: 图片中字号的大小，默认值为14。\n    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[7, 5]`。\n    - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。\n    - xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。\n    - zrotation: Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴。\n    - isgrid: 是否要网格。\n    - density: 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。\n    - colors: 一组颜色，`[]`列表形式去写，在多面图中用于按顺序制定每个面的颜色（包含标记符号的颜色）。\n    - edgecolor: 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。\n    - x_lim,y_lim,z_lim: x/y/z轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。\n    - elevation: 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。当elevation为正值时，观察者向上倾斜，负值则表示向下倾斜。默认15度。可根据美观与否微调。\n    - azimuth: 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。azim 的角度范围是 −180 到 180 度，其中正值表示逆时针旋转，负值表示顺时针。默认45度。可根据美观与否微调。\n    - roll: 滚动角 (roll)。 定义了绕观察者视线方向旋转的角度。它决定了观察者的头部倾斜程。默认0度，不需要动。\n    - left_margin=0, bottom_margin=0, right_margin=1, top_margin=1: 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。\n    - xpad=1, ypad=1, zpad=5, xlabelpad=2, ylabelpad=2, ylabelpad=12: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。如果挤了不好看了，再微调此参数，一般不用动。\n    - legend_options: Matplotlib图例参数字典。\n    ",
    "draw_lines": "\n    - expressions: Symbol表达式，字典形式传入。（必须）\n    - assigns: 表达式参数赋值，字典形式。\n    - the_var: 要分析的参数；\n    - ranges: 要分析的参数的取值。[初始,结束,间隔]\n    - x_name: 横轴名称标签，默认'x'。\n    - y_name: 纵轴名称标签，默认'y'。\n    - save_dir=None: 图片保存路径，字符串。默认None，不保存。\n    - fsize: 图片中字号的大小，默认值为14。\n    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。\n    - xt_rotation: 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。\n    - xrotation: 横轴名字标签旋转角度，默认值0，基本不需要动。\n    - yrotation: 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴。\n    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。\n    - linewidth: 线粗，默认1.5。\n    - markers: 一组标记符号，`[]`列表形式去写，在多线图中用于按顺序制定每个线的标记符号。\n    - markersize: 标记符号的大小，默认5。可以传入列表，分别为每条线设置。\n    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。\n    - isgrid: 是否要网格，默认True。\n    - x_lim: 横轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。\n    - y_lim: 纵轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。\n    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。\n    - legend_options: Matplotlib图例参数字典。\n    ",
    "list_equivalent_relations": "\n    解析关系式并生成所有等价的关系式。\n\n    参数:\n        equation (str): 输入的关系式，格式类似 '${\\Pi}_M={\\Pi}_N>{\\Pi}_P>{\\Pi}_B={\\Pi}_D={\\Pi}_E$'\n\n    返回:\n        list[str]: 所有等价的关系式\n    ",
}

TEXT["start"] = ("开始", "Start")
TEXT["end"] = ("结束", "End")

for _region_function in ("draw_max_area", "draw_detail_area"):
    CORE_FUNCTION_DOCS[_region_function] += (
        "\n        - dropout=0.001: 每个独立分块占整个绘图区的最小面积比例；"
        "0.001 为 0.1%，0.01 为 1%，0 表示不过滤。"
        "低于阈值的分块不绘制填色、边界、文字或引导线。\n"
    )
