from betu import *

# 绘图数据
data = {'Score': [45,
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
           96]}

# 横轴数据列
x = None

# 数据系列列
series = ['Score']

# 图形类型
kind = 'hist'

# 直方图分箱数
bins = 6

# x 轴名称
x_name = None

# y 轴名称
y_name = None

# 自动保存图片
save_dir = None

# 图例的方位
location = 'best'

# 图例的列数
ncol = 1

# 整体字号
fsize = 14

# 图片尺寸（英寸）
figsize = [6, 5]

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

# 图例字号
legendsize = 'auto'

# 图例精细设置（None 表示使用上面的图例参数）
legend_options = {'ncol': 1,
 'loc': 'best',
 'borderpad': 0.2,
 'labelspacing': 0.2,
 'handlelength': 1.5,
 'handletextpad': 0.2,
 'columnspacing': 0.3,
 'fontsize': 14}

# y 轴刻度旋转角度
yt_rotation = 0

# 是否显示图例
show_legend = True

# 图表标题
title = ''

the_plt = plot_table(
    data=data,
    x=x,
    series=series,
    kind=kind,
    bins=bins,
    x_name=x_name,
    y_name=y_name,
    save_dir=save_dir,
    location=location,
    ncol=ncol,
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
    xpad=xpad,
    ypad=ypad,
    xlabelpad=xlabelpad,
    ylabelpad=ylabelpad,
    xlabelsize=xlabelsize,
    ylabelsize=ylabelsize,
    legendsize=legendsize,
    legend_options=legend_options,
    yt_rotation=yt_rotation,
    show_legend=show_legend
)

the_plt = plot_context(the_plt)

if title:
    the_plt.title(title, fontsize=fsize)

the_plt.show()
