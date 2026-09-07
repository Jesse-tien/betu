from betu import *

# 定义符号
E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e = symbols('E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e')

# 表达式
expressions = {
    '$\\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2),
    '$\\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2),
    '$\\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
    '$\\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# x 轴名称
x_name = '$\\alpha$'

# y 轴名称
y_name = '$b$'

# z 轴名称
z_name = '$\\pi_r$'

# 自动保存图片
save_dir = None

# 曲面不透明度（0～1）
color_alpha = 0.8

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
linewidth = 0.2

# 整体字号
fsize = 14

# 图片尺寸（英寸）
figsize = [7, 5]

# 采样点数（越高越细）
precision = 1000

# x 轴标签旋转角度
xrotation = 0

# y 轴标签旋转角度
yrotation = 0

# z 轴标签旋转角度
zrotation = 90

# 是否显示浅灰虚线网格
isgrid = False

# 曲面线网格密度
density = 100

# 颜色
colors = ['b', 'g', 'r', 'y', 'm', 'c', 'lime', 'lightcoral', 'orange', 'violet']

# 曲面网格线颜色
edgecolor = None

# 横轴显示范围
x_lim = None

# 纵轴显示范围
y_lim = None

# 竖轴显示范围
z_lim = None

# 视角：上下俯仰
elevation = 15

# 视角：左右旋转
azimuth = 45

# 视角：画面倾斜
roll = 0

# 绘图区左边距
left_margin = 0

# 绘图区下边距
bottom_margin = 0

# 绘图区右边界
right_margin = 1

# 绘图区上边界
top_margin = 1

# x 轴刻度与轴线的距离
xpad = 1

# y 轴刻度与轴线的距离
ypad = 1

# z 轴刻度与轴线的距离
zpad = 5

# x 轴名称与刻度的距离
xlabelpad = 2

# y 轴名称与刻度的距离
ylabelpad = 2

# z 轴名称与刻度的距离
zlabelpad = 12

# x 轴名称字号
xlabelsize = 'auto'

# y 轴名称字号
ylabelsize = 'auto'

# z 轴名称字号
zlabelsize = 'auto'

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
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, E: 2.0, e_n: 1.0, e_r: 0.6, k: 1.1, p_e: 0.1}

# 横轴分析参数
the_var_x = alpha

# 横轴参数取值范围
start_end_x = [0.7, 0.8]

# 纵轴分析参数
the_var_y = b

# 纵轴参数取值范围
start_end_y = [0, 0.08]

the_plt = draw_3D(
    expressions=expressions,
    x_name=x_name,
    y_name=y_name,
    z_name=z_name,
    save_dir=save_dir,
    color_alpha=color_alpha,
    linestyles=linestyles,
    linewidth=linewidth,
    fsize=fsize,
    figsize=figsize,
    precision=precision,
    xrotation=xrotation,
    yrotation=yrotation,
    zrotation=zrotation,
    isgrid=isgrid,
    density=density,
    colors=colors,
    edgecolor=edgecolor,
    x_lim=x_lim,
    y_lim=y_lim,
    z_lim=z_lim,
    elevation=elevation,
    azimuth=azimuth,
    roll=roll,
    left_margin=left_margin,
    bottom_margin=bottom_margin,
    right_margin=right_margin,
    top_margin=top_margin,
    xpad=xpad,
    ypad=ypad,
    zpad=zpad,
    xlabelpad=xlabelpad,
    ylabelpad=ylabelpad,
    zlabelpad=zlabelpad,
    xlabelsize=xlabelsize,
    ylabelsize=ylabelsize,
    zlabelsize=zlabelsize,
    legend_options=legend_options,
    show_legend=show_legend,
    assigns=assigns,
    the_var_x=the_var_x,
    start_end_x=start_end_x,
    the_var_y=the_var_y,
    start_end_y=start_end_y
)

the_plt = plot_context(the_plt)

if title:
    the_plt.title(title, fontsize=fsize)

the_plt.show()
