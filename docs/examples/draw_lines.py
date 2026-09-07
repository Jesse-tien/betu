from betu import *

# 定义符号
a, t, x, y = symbols('a, t, x, y')

# 中间变量
p_n = a + x

# 表达式
expressions = {
    '$A$': (a-x)**2 + y,
    '$B$': x + 2*y,
    '$C$': 2-x + y**2,
    '$D$': integrate(p_n*t, (t, 0, y)),
}

# x 轴名称
x_name = '$x$'

# y 轴名称
y_name = '$y$'

# 自动保存图片
save_dir = None

# 整体字号
fsize = 14

# 图片尺寸（英寸）
figsize = [5, 4]

# x 轴刻度旋转角度
xt_rotation = 0

# x 轴标签旋转角度
xrotation = 0

# y 轴标签旋转角度
yrotation = 0

# 线型
linestyles = ['solid',
 'dashed',
 'dotted',
 'dashdot',
 (0, (1, 10)),
 (0, (5, 10)),
 (0, (3, 10, 1, 10, 1, 10)),
 (5, (10, 3)),
 (0, (5, 5)),
 (0, (5, 1)),
 'solid',
 'dashed',
 'dotted',
 'dashdot',
 (0, (1, 10)),
 (0, (5, 10)),
 (0, (3, 10, 1, 10, 1, 10)),
 (5, (10, 3)),
 (0, (5, 5)),
 (0, (5, 1))]

# 线宽
linewidth = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]

# 标记形状
markers = ['o',
 's',
 '*',
 'P',
 'X',
 'D',
 'p',
 'x',
 '8',
 '2',
 'H',
 '+',
 '|',
 '<',
 '>',
 '^',
 'v',
 'd',
 None,
 '3']

# 标记大小
markersize = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]

# 颜色
colors = ['navy',
 'teal',
 'brown',
 'purple',
 'olivedrab',
 'orangered',
 'g',
 'r',
 'c',
 'm',
 'y',
 'k',
 'dodgerblue',
 'forestgreen',
 'b',
 'mediumvioletred',
 'goldenrod',
 'crimson',
 'gray']

# 是否显示浅灰虚线网格
isgrid = True

# 横轴显示范围
x_lim = None

# 纵轴显示范围
y_lim = None

# x 轴刻度与轴线的距离
xpad = 3

# y 轴刻度与轴线的距离
ypad = 3

# x 轴名称与刻度的距离
xlabelpad = 10

# y 轴名称与刻度的距离
ylabelpad = 10

# x 轴名称字号
xlabelsize = 'auto'

# y 轴名称字号
ylabelsize = 'auto'

# 图例精细设置（None 表示使用上面的图例参数）
legend_options = {'ncol': 1,
 'loc': 'best',
 'borderpad': 0.2,
 'labelspacing': 0.2,
 'handlelength': 1.5,
 'handletextpad': 0.2,
 'columnspacing': 0.3,
 'fontsize': 14}

# 是否显示图例
show_legend = True

# 图表标题
title = ''

# 参数赋值
assigns = {a: 2, y: 0.5}

# 要分析的参数
the_var = x

# 参数取值范围：起点、终点、步长
ranges = [0, 2, 0.025]

the_plt = draw_lines(
    expressions=expressions,
    x_name=x_name,
    y_name=y_name,
    save_dir=save_dir,
    fsize=fsize,
    figsize=figsize,
    xt_rotation=xt_rotation,
    xrotation=xrotation,
    yrotation=yrotation,
    linestyles=linestyles,
    linewidth=linewidth,
    markers=markers,
    markersize=markersize,
    colors=colors,
    isgrid=isgrid,
    x_lim=x_lim,
    y_lim=y_lim,
    xpad=xpad,
    ypad=ypad,
    xlabelpad=xlabelpad,
    ylabelpad=ylabelpad,
    xlabelsize=xlabelsize,
    ylabelsize=ylabelsize,
    legend_options=legend_options,
    show_legend=show_legend,
    assigns=assigns,
    the_var=the_var,
    ranges=ranges
)

the_plt = plot_context(the_plt)

if title:
    the_plt.title(title, fontsize=fsize)

the_plt.show()
