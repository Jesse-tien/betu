from betu import *

# 定义符号
x, y = symbols('x, y')

# 表达式
expressions = {
    '$A$': x,
    '$B$': y,
    '$C$': 0.88 + 0*x,
}

# 参数赋值
assigns = {}

# 横轴分析参数
the_var_x = x

# 横轴参数取值范围
start_end_x = [0, 1]

# 纵轴分析参数
the_var_y = y

# 纵轴参数取值范围
start_end_y = [0, 1]

# x 轴名称
x_name = '$x$'

# y 轴名称
y_name = '$y$'

# 整体字号
fsize = 14

# 区域文字字号增量
text_fsize_add = -2

# 自动保存图片
save_dir = None

# 采样点数（越高越细）
precision = 1000

# 图片尺寸（英寸）
figsize = [9, 5]

# 颜色
colors = ['#ffffff',
 '#E6E6E6',
 '#DCDCDC',
 '#D2D2D2',
 '#C8C8C8',
 '#C3C3C3',
 '#BEBEBE',
 '#B9B9B9',
 '#B4B4B4',
 '#AFAFAF',
 '#AAAAAA',
 '#A5A5A5',
 '#A0A0A0',
 '#9B9B9B',
 '#969696',
 '#919191',
 '#8C8C8C',
 '#878787',
 '#828282',
 '#7D7D7D',
 '#787878',
 '#6E6E6E',
 '#646464',
 '#646464',
 '#5F5F5F',
 '#5A5A5A',
 '#5A5A5A',
 '#565656',
 '#525252',
 '#4E4E4E',
 '#4A4A4A',
 '#464646',
 '#424242',
 '#3E3E3E',
 '#3A3A64']

# 区域填充纹理
patterns = [None,
 '--',
 'xx',
 '||',
 '..',
 'oo',
 '++',
 '**',
 '\\\\\\\\',
 '////',
 '-',
 'x',
 '|',
 '.',
 'o',
 '+',
 '*',
 '\\\\',
 '//',
 '---',
 'xxx',
 '|||',
 '...',
 'ooo',
 '+++',
 '***',
 '\\\\\\\\\\\\',
 '//////']

# x 轴标签旋转角度
xrotation = 0

# y 轴标签旋转角度
yrotation = 90

# 区域边界线粗
linewidths = 0.1

# x 轴刻度与轴线的距离
xpad = 3

# y 轴刻度与轴线的距离
ypad = 3

# x 轴名称与刻度的距离
xlabelpad = 3

# y 轴名称与刻度的距离
ylabelpad = 5

# 区域标注前缀
prefix = 'Region'

# 区域编号格式
numbers = 'roman'

# 小区域面积比例阈值：0.001=0.1%，0 不过滤；按每个独立分块判断
dropout = 0.001

# x 轴名称字号
xlabelsize = 'auto'

# y 轴名称字号
ylabelsize = 'auto'

# 区域标签背景颜色
pattern_colors = 'auto'

# 区域标签位置偏移
pattern_moves = 'auto'

# 区域文字黑白切换阈值
switchcolor = 112

# 图例精细设置（None 表示使用上面的图例参数）
legend_options = {'ncol': 1,
 'loc': 'outside right',
 'borderpad': 0.2,
 'labelspacing': 0.2,
 'handlelength': 1.5,
 'handletextpad': 0.2,
 'columnspacing': 0.3,
 'fontsize': 14}

# 是否显示图例
show_legend = True

# 小区域标记自动避让与引导线
smart_labels = True

# 图表标题
title = ''

the_plt = draw_detail_area(
    expressions=expressions,
    assigns=assigns,
    the_var_x=the_var_x,
    start_end_x=start_end_x,
    the_var_y=the_var_y,
    start_end_y=start_end_y,
    x_name=x_name,
    y_name=y_name,
    fsize=fsize,
    text_fsize_add=text_fsize_add,
    save_dir=save_dir,
    precision=precision,
    figsize=figsize,
    colors=colors,
    patterns=patterns,
    xrotation=xrotation,
    yrotation=yrotation,
    linewidths=linewidths,
    xpad=xpad,
    ypad=ypad,
    xlabelpad=xlabelpad,
    ylabelpad=ylabelpad,
    prefix=prefix,
    numbers=numbers,
    dropout=dropout,
    xlabelsize=xlabelsize,
    ylabelsize=ylabelsize,
    pattern_colors=pattern_colors,
    pattern_moves=pattern_moves,
    switchcolor=switchcolor,
    legend_options=legend_options,
    show_legend=show_legend,
    smart_labels=smart_labels
)

the_plt = plot_context(the_plt)

if title:
    the_plt.title(title, fontsize=fsize)

the_plt.show()
