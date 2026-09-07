from .helpers import tr
from . import helpers as H
# Author: Yu-Xin Tian, 2026-09-07 Version 1.0.0

from sympy import *
from itertools import permutations, product
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import copy
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

import string
import re

# 设置 matplotlib 字体为支持中英文的字体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

config = {
    "font.family": ["Times New Roman", "SimSun"],
    "font.size": 14,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
    "mathtext.fallback": "stix",
}

rcParams.update(config)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

from ._default_setting import (
    DEFAULT_COLORS,
    DEFAULT_FILL_COLORS,
    DEFAULT_PATTERNS,
    LEGEND_DEFAULTS,
    DEFAULT_3D_COLORS,
    DEFAULT_LINESTYLES,
    DEFAULT_LINEWIDTHS,
    DEFAULT_MARKERS,
    DEFAULT_MARKERSIZES,
)

def check_hex_color(color):
    # 正则表达式检查是否为十六进制颜色（# 开头，后面跟 3 或 6 个十六进制字符）
    pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return bool(pattern.match(color))

def gen_letters(nums):
    # 生成大写字母
    uppercase_letters = string.ascii_uppercase

    # 列出36个大写字母
    letters = []
    for i in range(nums):
        if i < 26:
            letters.append(uppercase_letters[i])
        else:
            div, mod = divmod(i - 26, 26)
            letters.append(uppercase_letters[div] + uppercase_letters[mod])
    return letters

def gen_romans(nums):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_lists = []
    for num in range(1, nums+1):
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        roman_lists.append(roman_num)
    return roman_lists


def list_equivalent_relations(expr):
    # 去除开头和结尾的符号（如 $）
    equation = expr.strip('$')

    # 分离各部分
    parts = []
    temp = []
    for char in equation:
        if char in {'=', '>'}:
            if temp:
                parts.append(''.join(temp))
                temp = []
            parts.append(char)
        else:
            temp.append(char)
    if temp:
        parts.append(''.join(temp))

    # 组合相等的部分
    groups = []
    current_group = []
    for part in parts:
        if part == '=':
            continue
        elif part == '>':
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(part)
    if current_group:
        groups.append(current_group)

    # 生成等价关系式
    all_relations = []
    perms = [list(permutations(group)) for group in groups]
    for perm in product(*perms):
        result = []
        for i, group in enumerate(perm):
            result.append('='.join(group))
            if i < len(perm) - 1:
                result.append('>')
        all_relations.append('$' + ''.join(result) + '$')

    all_relations.remove(expr)
    return all_relations


def join_with_symbols(perm, symbols):
    # 确保排列和符号组合的长度匹配
    if len(perm) - 1 != len(symbols):
        raise ValueError("排列的长度减1应等于符号组合的长度")

    # 使用符号组合连接排列中的元素
    result = []
    for i in range(len(perm) - 1):
        result.append(perm[i])
        result.append(symbols[i])
    result.append(perm[-1])  # 添加最后一个元素

    return ''.join(result)


def get_max_names(expr):
    s = expr.replace('$', '')
    parts = s.split('>')
    if len(parts) > 1:
        return parts[0].split('=')
    else:
        return s.split('=')

def remove_duplicates(lst):
    seen = []
    result = []
    for sublist in lst:
        if sublist not in seen:
            seen.append(sublist)
            result.append(sublist)
    return result

def draw_lines(expressions,
               assigns,
               the_var,
               ranges,
               x_name='x',
               y_name='y',
               save_dir=None,
               fsize=14,
               figsize=[5, 4],
               xt_rotation=0, xrotation=0, yrotation=0,
               linestyles=DEFAULT_LINESTYLES,
               linewidth=DEFAULT_LINEWIDTHS,
               markers=DEFAULT_MARKERS,
               markersize=DEFAULT_MARKERSIZES,
               colors=DEFAULT_COLORS,
               isgrid=True,
               x_lim=None, y_lim=None, xpad=3, ypad=3, xlabelpad=10, ylabelpad=10,
               xlabelsize='auto', ylabelsize='auto',
               legend_options=LEGEND_DEFAULTS):
    if expressions is None:
        print(tr('message_11'))
        return None

    if the_var is None or ranges is None:
        print(
            tr('message_13'))
        return None

    fig, ax = plt.subplots(figsize=figsize)
    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    plt.xticks(fontsize=fsize, rotation=xt_rotation)
    plt.yticks(fontsize=fsize)

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    ranges_ = [ranges[0], ranges[1] + ranges[2], ranges[2]]
    if x_lim is None:
        plt.xlim(ranges[0], ranges[1])
    else:
        plt.xlim(x_lim[0], x_lim[1])

    if y_lim is not None:
        plt.ylim(y_lim[0], y_lim[1])

    # linewidth和markersize列表化：
    if isinstance(linewidth, list):
        linewidth_ = linewidth
    else:
        linewidth_ = [linewidth] * exp_num

    if isinstance(markersize, list):
        markersize_ = markersize
    else:
        markersize_ = [markersize]*exp_num


    if exp_num == 1:
        xs = []
        ys = []
        the_exp = expressions[exp_names[0]]
        if assigns is None:
            assigned_exp = the_exp
        else:
            assigned_exp = the_exp.subs(assigns)

        for i in np.arange(*ranges_):
            xs.append(i)
            ys.append(assigned_exp.subs({the_var:i}).evalf())

        ax.plot(xs, ys, linestyle=linestyles[0] if linestyles is not None else '-',
                c=colors[0], linewidth=linewidth_[0], marker=markers[0],
                markersize=markersize_[0], markevery=max(1, len(xs)//10), label=exp_names[0])
        y_min = np.min(ys)
        y_max = np.max(ys)
    else:
        for j, em in enumerate(exp_names):
            xs = []
            ys = []
            the_exp = expressions[exp_names[j]]
            if assigns is None:
                assigned_exp = the_exp
            else:
                assigned_exp = the_exp.subs(assigns)
            for i in np.arange(*ranges_):
                xs.append(i)
                ys.append(assigned_exp.subs({the_var: i}).evalf())

            if linestyles is None:
                the_ls = '-'
            else:
                the_ls = linestyles[j]

            if len(xs) > 10:
                markevery = int(len(xs)/10)
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth_[j], marker=markers[j],
                        markersize=markersize_[j], markevery = markevery, label=em)
            else:
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth_[j], marker=markers[j],
                        markersize=markersize_[j],label=em)


            y_min_now = np.min(ys)
            y_max_now = np.max(ys)
            if j ==0:
                y_max = y_max_now
                y_min = y_min_now
            else:
                if y_max_now > y_max:
                    y_max = y_max_now
                if y_min_now < y_min:
                    y_min = y_min_now

    judge_y = max(abs(y_max), abs(y_min))
    judge_x = max(abs(np.max(xs)), abs(np.min(xs)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0), useMathText=True)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    if isgrid:
        ax.grid(
            visible=True,  # 显示网格
            linestyle='--',  # 虚线样式，比实线更柔和
            alpha=0.3,  # 透明度，数值越小越淡
            color='lightgray',  # 浅灰色，不突兀
            axis='both'  # 同时显示x轴和y轴网格，也可只设 'x' 或 'y'
        )
    else:
        ax.grid(False)

    if exp_num > 1 and legend_options is not None:
        ax.legend(**legend_options)

    fig.tight_layout()

    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(
                save_dir,
                format="svg",
                bbox_inches="tight",  # 自动裁剪掉图周围多余的空白边距
                dpi=600,  # SVG 是矢量图，dpi 主要影响内部位图元素的渲染精度
                transparent=False  # 设为 True 可保存透明背景
            )
        else:
            plt.savefig(
                save_dir,
                dpi=600,
                bbox_inches="tight",
                transparent=False,)

    return plt

# ----------------------------------------片状型图-------------------------------------------

def order_types(exp_names, values, reverse=True):
    return_val = ""
    # 获取排序后元素的索引 reverse=True默认降序
    sorted_indices = sorted(range(len(values)), key=lambda x: values[x], reverse=reverse)
    for _i, em in enumerate(sorted_indices):
        if reverse:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" > " + exp_names[em][1:-1]
                last_value = cur_value
        else:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" < " + exp_names[em][1:-1]
                last_value = cur_value
    return return_val + r"$", sorted_indices


def covert_orders(expressions, assigns, the_var1, the_var2, X, Y, reverse=True):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)
    map_dict = {}  # value: relationship
    map_order = {}  # value: order

    res_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var1, the_var2), assigned_exp, 'numpy')
        exp_value = the_func(X, Y)
        if isinstance(exp_value, float):
            exp_value = np.ones(X.shape, dtype=float) * exp_value
        res_list.append(exp_value)

    value_ldata = []
    index_point = 0
    for ii in range(len(res_list[0])):
        tmp = []
        for jj in range(len(res_list[0][0])):
            compare_list = [em[ii][jj] for em in res_list]
            latex_res, the_order = order_types(exp_names, compare_list, reverse=reverse)
            if latex_res not in map_dict.values():
                map_dict[index_point] = latex_res
                map_order[index_point] = the_order
                tmp.append(index_point)
                index_point += 1
            else:
                reversed_dict = {v: k for k, v in map_dict.items()}
                tmp.append(reversed_dict[latex_res])
        value_ldata.append(tmp)

    return np.array(value_ldata), map_dict, map_order  # value: relationship


def draw_3D(expressions, assigns, the_var_x, start_end_x, the_var_y, start_end_y,
            x_name='x', y_name='y', z_name='z',
            save_dir=None, color_alpha=0.8,
            linestyles=DEFAULT_LINESTYLES, linewidth=0.2,
            fsize=14, figsize=[7, 5],
            precision=1000,
            xrotation=0, yrotation=0, zrotation=90,
            isgrid=True, density=100,
            colors=DEFAULT_3D_COLORS, edgecolor=None,
            x_lim=None, y_lim=None, z_lim=None,
            elevation=15, azimuth=45, roll=0,
            left_margin=0, bottom_margin=0, right_margin=1, top_margin=1,
            xpad=1, ypad=1, zpad=5,
            xlabelpad=2, ylabelpad=2, zlabelpad=12,
            xlabelsize='auto', ylabelsize='auto', zlabelsize='auto',
            legend_options=LEGEND_DEFAULTS
            ):

    if expressions is None:
        print(tr('message_11'))
        return None
    if assigns is None:
        print(tr('message_12'))
        return None
    if the_var_x is None or the_var_y is None or start_end_x is None or start_end_y is None:
        print(
            tr('message_13'))
        return None

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=left_margin, bottom=bottom_margin, right=right_margin, top=top_margin)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)

    ax.yaxis.set_rotate_label(False)
    ax.xaxis.set_rotate_label(False)
    ax.zaxis.set_rotate_label(False)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize
    if zlabelsize == 'auto':
        zlabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)
    ax.set_zlabel(z_name, fontsize=zlabelsize, fontweight='bold', rotation=zrotation, labelpad=zlabelpad)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)
    ax.tick_params(axis='z', direction='in', pad=zpad)

    # Define the range for x and y
    x_ = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_ = np.linspace(start_end_y[0], start_end_y[1], precision)
    x, y = np.meshgrid(x_, y_)

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if len(x_) > density:
        rstride = int(len(x_) / density)
    else:
        rstride = 1

    if len(y_) > density:
        cstride = int(len(y_) / density)
    else:
        cstride = 1

    # color_alpha 列表化：
    if isinstance(color_alpha, list):
        color_alpha_ = color_alpha
    else:
        color_alpha_ = [color_alpha] * exp_num


    if exp_num == 1:
        the_exp = expressions[exp_names[0]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
        z = the_func(x, y)
        if isinstance(z, float):
            z = np.ones(x.shape, dtype=float) * z
        ax.plot_surface(x, y, z, color=colors[0], edgecolor=None, alpha=color_alpha_[0])
        z_min = np.min(z)
        z_max = np.max(z)
    else:
        legend_elements = []
        his_zs = []

        get_order_func = lambda x_, y_: covert_orders(expressions=expressions, assigns=assigns,
                                              the_var1=the_var_x, the_var2=the_var_y,
                                              X=x_, Y=y_, reverse=False) # 越来越大
        Z_judge, _, map_order = get_order_func(x, y)  # value: relationship

        remove_values = []
        use_values = []
        dropout = 0.01
        for em in map_order.keys():
            count = np.count_nonzero(Z_judge == em)
            if count / (precision ** 2) <= dropout:
                remove_values.append(em)
            else:
                use_values.append(em)

        for em in remove_values:
            indices = np.where(Z_judge == em)
            rows, cols = indices
            for row, col in zip(rows, cols):
                if (col < precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, precision - col):
                        try_value = Z_judge[row, col + c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (col >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, col):
                        try_value = Z_judge[row, col - c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row < precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, precision - row):
                        try_value = Z_judge[row + r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, row):
                        try_value = Z_judge[row - r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break

        for j, em in enumerate(exp_names):
            the_exp = expressions[exp_names[j]]
            assigned_exp = the_exp.subs(assigns)
            the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
            z = the_func(x, y)
            if isinstance(z, float):
                z = np.ones(x.shape, dtype=float) * z

            legend_elements.append(Patch(facecolor=colors[j], edgecolor=edgecolor, alpha=color_alpha_[j],
                                         label=em, linestyle=linestyles[j], linewidth = linewidth))
            his_zs.append(z)

            z_min_now = np.min(z)
            z_max_now = np.max(z)
            if j == 0:
                z_max = z_max_now
                z_min = z_min_now
            else:
                if z_max_now > z_max:
                    z_max = z_max_now
                if z_min_now < z_min:
                    z_min = z_min_now

        for key_ in use_values:
            value_ = map_order[key_]
            #print(key_, value_)
            # 画图区域
            mask = (Z_judge==key_)
            for the_order in value_:
                # 按顺序画
                the_z = copy.deepcopy(his_zs[the_order])
                the_z = the_z.astype(float)
                the_z[~mask] = np.nan

                ax.plot_surface(x, y, the_z, color=colors[the_order], alpha=color_alpha_[the_order], edgecolor=edgecolor,
                                linestyle=linestyles[the_order], linewidth=linewidth, rstride=rstride, cstride=cstride)
                del the_z

    ax.view_init(elev=elevation, azim=azimuth, roll=roll)

    ax.set_zticks(np.linspace(z_min, z_max, 10))
    for label in ax.get_zticklabels():
        label.set_fontsize(fsize)

    judge = abs(z_max - z_min)
    if judge < 0.0001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.5f'))
    elif judge < 0.001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    elif judge < 0.01:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
    elif judge < 1:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    elif judge >= 1 and judge < 10:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    else:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))

    from ._plotting import distinguish_tick_labels
    distinguish_tick_labels(ax.zaxis)

    if x_lim is None:
        ax.set_xlim(start_end_x[1], start_end_x[0])
    else:
        ax.set_xlim(x_lim[0], x_lim[1])

    if y_lim is None:
        ax.set_ylim(start_end_y[0], start_end_y[1])
    else:
        ax.set_ylim(y_lim[0], y_lim[1])

    if z_lim is not None:
        ax.set_zlim(z_lim[0], z_lim[1])

    if isgrid:
        ax.grid(
            visible=True,  # 显示网格
            linestyle='--',  # 虚线样式，比实线更柔和
            alpha=0.3,  # 透明度，数值越小越淡
            color='lightgray',  # 浅灰色，不突兀
            axis='both'  # 同时显示x轴和y轴网格，也可只设 'x' 或 'y'
        )
    else:
        ax.grid(False)

    if exp_num > 1 and legend_options is not None:
        ax.legend(**legend_options)

    from ._plotting import complete_3d_bounds
    complete_3d_bounds(ax)
    fig.canvas.draw()
    fig.tight_layout() # 可以去掉

    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(
                save_dir,
                format="svg",
                bbox_inches="tight",  # 自动裁剪掉图周围多余的空白边距
                dpi=600,  # SVG 是矢量图，dpi 主要影响内部位图元素的渲染精度
                transparent=False  # 设为 True 可保存透明背景
            )
        else:
            plt.savefig(
                save_dir,
                dpi=600,
                bbox_inches="tight",
                transparent=False,)

    return plt


def draw_area(expressions=None, assigns=None,
              the_var_x=None, start_end_x=None, the_var_y=None, start_end_y=None,
              x_name='x', y_name='y', fsize=14, text_fsize_add=0, save_dir=None, precision=1000, figsize=[9, 5],
              colors=DEFAULT_FILL_COLORS, patterns=DEFAULT_PATTERNS, xrotation=0, yrotation=90,
              linewidths=0.1, xpad=3, ypad=3, xlabelpad=3, ylabelpad=5,
              prefix='Region', numbers='roman', xlabelsize='auto', ylabelsize='auto',
              pattern_colors='auto', pattern_moves='auto',
              mode='max', texts=None, dropout=0.01, switchcolor=112, legend_options=LEGEND_DEFAULTS):

    if not isinstance(dropout, (int, float)) or not np.isfinite(dropout) or not 0 <= dropout <= 1:
        raise ValueError(H.tr('invalid_dropout'))

    if expressions is None:
        print(tr('message_11'))
        return None
    if assigns is None:
        print(tr('message_12'))
        return None
    if the_var_x is None or the_var_y is None or start_end_x is None or start_end_y is None:
        print(
            tr('message_13'))
        return None

    hatches = patterns

    if numbers == 'roman':
        # 列出前40个罗马数字
        numerals = gen_romans(40)
    elif numbers == 'letter':
        numerals = gen_letters(40)
    else:
        numerals = [str(i + 1) for i in range(40)]

    exp_num = len(expressions.keys())
    if exp_num <= 1:
        print(tr('message_14'))
        return None

    # 替换表达式中的参数
    exprs = {}
    for name, expr in expressions.items():
        if assigns is None:
            assigned_exp = expr
        else:
            assigned_exp = expr.subs(assigns)
        exprs[name] = assigned_exp

    # 生成变量的取值网格
    vals_x = np.linspace(start_end_x[0], start_end_x[1], precision)
    vals_y = np.linspace(start_end_y[0], start_end_y[1], precision)
    X, Y = np.meshgrid(vals_x, vals_y)

    # 将 SymPy 表达式转换为数值函数
    funcs = {name: lambdify((the_var_x, the_var_y), expr, 'numpy') for name, expr in exprs.items()}

    # 计算每个点对应的表达式值
    vals = {name: func(X, Y) for name, func in funcs.items()}

    # 获取函数名称的自定义映射
    expressions_keys = expressions.keys()

    if mode == 'max':
        the_texts = {}
        if texts is None:
            for em in expressions_keys:
                the_texts[em.replace('$', '')] = em
        else:
            for i, em in enumerate(expressions_keys):
                the_texts[em.replace('$', '')] = texts[i]

    # 定义区域的条件和对应的表达式顺序（含等于）
    all_relas = product(['>', '='], repeat=exp_num - 1)
    relas = [em for em in all_relas]

    conditions = []
    bad_his = []
    for perm in permutations(expressions_keys):  # 表达式位置关系
        for _rela in relas:  # 连接符号列表
            condition = True
            for i in range(len(perm) - 1):
                if _rela[i] == '>':
                    condition &= (vals[perm[i]] > vals[perm[i + 1]])
                else:
                    condition &= (vals[perm[i]] == vals[perm[i + 1]])

            joined_string = join_with_symbols(perm, _rela)
            the_label = '$' + joined_string.replace('$', '') + '$'

            if (not np.all(condition == False)) and (the_label not in bad_his) and (
                    mode == 'max' or np.sum(condition) / (precision ** 2) >= dropout):
                conditions.append((condition, the_label))
                if '=' in the_label:
                    bad_label = list_equivalent_relations(the_label)  # '${\\Pi}_N>{\\Pi}_P>{\\Pi}_B={\\Pi}_D$'
                    # 等式去重
                    bad_his += bad_label

    case_num = len(conditions)

    if mode == 'max':
        max_cases = []
        for en in conditions:
            who_max = get_max_names(en[1])
            max_cases.append(who_max)
        unique_max_cases = remove_duplicates(max_cases)

        max_conditions = []
        for em in unique_max_cases:
            sum_condition = False
            for en in conditions:
                if get_max_names(en[1]) == em:
                    # 累或数组
                    sum_condition |= en[0]
            max_conditions.append((sum_condition, ', '.join([the_texts[enn] for enn in em])))
        conditions = max_conditions
        case_num = len(conditions)

    from .region_labels import filter_small_regions
    visible_conditions = []
    for condition, label in conditions:
        condition = filter_small_regions(np.broadcast_to(condition, X.shape), dropout)
        if np.any(condition):
            visible_conditions.append((condition, label))
    conditions = visible_conditions
    case_num = len(conditions)

    # 确保颜色和图案的数量足够
    if len(colors) < case_num:
        colors = colors * ((case_num // len(colors)) + 1)
    if len(patterns) < case_num:
        hatches = hatches * ((case_num // len(patterns)) + 1)

    # 创建图形
    fig, ax = plt.subplots(figsize=figsize)
    if not conditions:
        ax.set_xlim(start_end_x)
        ax.set_ylim(start_end_y)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)

    # 绘制区域、添加文本标记
    if mode != 'max':
        legend_elements = []

    ax._betu_regions = []

    for i, (condition, label) in enumerate(conditions):
        the_color = colors[i]
        the_pattern = hatches[i]
        ax.contourf(X, Y, condition, levels=[0.5, 1.5], colors=[the_color], alpha=1, hatches=[the_pattern])
        ax.contour(X, Y, condition, colors='k', linewidths=linewidths, alpha=1)

        x_center = np.mean(X[condition])
        y_center = np.mean(Y[condition])

        if mode != 'max':
            the_text = H.REGION_NAME_FORMAT.format(prefix=prefix.rstrip(), number=numerals[i]).strip()
            legend_text = H.REGION_LEGEND_FORMAT.format(name=the_text, relation=label)
        else:
            the_text = label

        if pattern_colors != 'auto':
            if pattern_colors[i] != 'auto':
                the_color = pattern_colors[i]

        try:
            # 尝试将十六进制颜色代码转换为RGB元组
            rgb = mcolors.hex2color(the_color)
        except ValueError:
            # 如果转换失败，则说明the_color是一个颜色单词
            rgb = mcolors.to_rgb(the_color)

        # 计算亮度
        brightness = rgb[0] * 255 * 0.299 + rgb[1] * 255 * 0.587 + rgb[2] * 255 * 0.114

        if pattern_moves != 'auto':
            ax.text(x_center + pattern_moves[i][0], y_center + pattern_moves[i][1], the_text, ha='center', va='center',
                    fontsize=fsize + text_fsize_add, color='white' if brightness < switchcolor else 'k',
                    backgroundcolor=the_color)
        else:
            ax.text(x_center, y_center, the_text, ha='center', va='center', fontsize=fsize + text_fsize_add,
                    color='white' if brightness < switchcolor else 'k',
                    backgroundcolor=the_color)

        ax._betu_regions.append((ax.texts[-1], condition, vals_x, vals_y))

        if mode != 'max':
            legend_elements.append(
                Patch(facecolor=the_color, linewidth=linewidths, edgecolor='k',
                      label=legend_text, hatch=the_pattern)
            )

    # 设置刻度
    ax.tick_params(axis='x', direction='out', pad=xpad)
    ax.tick_params(axis='y', direction='out', pad=ypad)

    judge_y = max(abs(np.max(vals_y)), abs(np.min(vals_y)))
    judge_x = max(abs(np.max(vals_x)), abs(np.min(vals_x)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0), useMathText=True)

    ax.grid(False)

    if mode != 'max':
        ax._betu_region_handles = legend_elements
    if mode != 'max' and legend_options is not None:
        fig.legend(handles=legend_elements, **legend_options,
                   prop=FontProperties(family=["Times New Roman", "SimSun"]))

    fig.tight_layout() # 可以去掉

    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(
                save_dir,
                format="svg",
                bbox_inches="tight",  # 自动裁剪掉图周围多余的空白边距
                dpi=600,  # SVG 是矢量图，dpi 主要影响内部位图元素的渲染精度
                transparent=False  # 设为 True 可保存透明背景
            )
        else:
            plt.savefig(
                save_dir,
                dpi=600,
                bbox_inches="tight",
                transparent=False,)

    return plt


def draw_max_area(expressions=None, assigns=None, the_var_x=None, start_end_x=None, the_var_y=None,
                  start_end_y=None, x_name='x', y_name='y', fsize=14, texts=None, text_fsize_add=0,
                  save_dir=None, precision=1000, figsize=[5, 4],
                  colors=DEFAULT_FILL_COLORS, patterns=DEFAULT_PATTERNS,
                  xrotation=0, yrotation=90, linewidths=0.1,
                  xpad=3, ypad=3, xlabelpad=3, ylabelpad=5,
                  xlabelsize='auto', ylabelsize='auto',
                  pattern_colors = 'auto', pattern_moves = 'auto',
                  switchcolor=112, dropout=0.001):

    return draw_area(expressions=expressions, assigns=assigns,
                     the_var_x=the_var_x, start_end_x=start_end_x,
                     the_var_y=the_var_y, start_end_y=start_end_y,
                     x_name=x_name, y_name=y_name,
                     fsize=fsize, text_fsize_add=text_fsize_add,
                     save_dir=save_dir, precision=precision, figsize=figsize,
                     colors=colors, patterns=patterns,
                     xrotation=xrotation, yrotation=yrotation,
                     linewidths=linewidths, xpad=xpad, ypad=ypad,
                     xlabelpad=xlabelpad, ylabelpad=ylabelpad,
                     prefix='Region', numbers='roman', xlabelsize=xlabelsize, ylabelsize=ylabelsize,
                     pattern_colors=pattern_colors, pattern_moves=pattern_moves,
                     mode='max', texts=texts, dropout=dropout, switchcolor=switchcolor,
                     legend_options=LEGEND_DEFAULTS)


tmp_legend_options = LEGEND_DEFAULTS.copy()
tmp_legend_options.update({'loc': 'outside right center'})
def draw_detail_area(expressions=None, assigns=None,
                     the_var_x=None, start_end_x=None, the_var_y=None, start_end_y=None,
                    x_name='x', y_name='y', fsize=14, text_fsize_add=0, save_dir=None,
                    precision=1000, figsize=[9, 5],
                    colors=DEFAULT_FILL_COLORS, patterns=DEFAULT_PATTERNS,
                    xrotation=0, yrotation=90, linewidths=0.1,
                    xpad=3, ypad=3, xlabelpad=3, ylabelpad=5,
                    prefix='Region', numbers='roman', dropout=0.001,
                    xlabelsize='auto', ylabelsize = 'auto',
                    pattern_colors = 'auto', pattern_moves = 'auto',
                    switchcolor=112, legend_options=tmp_legend_options):

    return draw_area(expressions=expressions, assigns=assigns,
                     the_var_x=the_var_x, start_end_x=start_end_x,
                     the_var_y=the_var_y, start_end_y=start_end_y,
                     x_name=x_name, y_name=y_name,
                     fsize=fsize, text_fsize_add=text_fsize_add,
                     save_dir=save_dir, precision=precision, figsize=figsize,
                     colors=colors, patterns=patterns,
                     xrotation=xrotation, yrotation=yrotation,
                     linewidths=linewidths, xpad=xpad, ypad=ypad,
                     xlabelpad=xlabelpad, ylabelpad=ylabelpad,
                     prefix=prefix, numbers=numbers, xlabelsize=xlabelsize, ylabelsize=ylabelsize,
                     pattern_colors=pattern_colors, pattern_moves=pattern_moves, mode='detail',
                     texts=None, dropout=dropout, switchcolor=switchcolor, legend_options=legend_options)

from .helpers import CORE_FUNCTION_DOCS
for _name, _help in CORE_FUNCTION_DOCS.items():
    globals()[_name].__doc__ = _help
