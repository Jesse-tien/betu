"""在已有分区结果上安排标签，不改变分区条件或采样精度。"""

import math
import numpy as np
from matplotlib.transforms import Bbox, blended_transform_factory


def connected_regions(mask):
    """用八邻接识别分块，斜向相连的边界采样点属于同一块。"""
    parents, runs, previous = [], [], []

    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    for row, line in enumerate(mask):
        edges = np.flatnonzero(np.diff(np.pad(line.astype(np.int8), (1, 1))))
        current = []
        start = 0
        for left, right in zip(edges[::2], edges[1::2]):
            index = len(parents)
            parents.append(index)
            runs.append((row, int(left), int(right)))
            current.append((left, right, index))
            while start < len(previous) and previous[start][1] < left:
                start += 1
            for pleft, pright, pindex in previous[start:]:
                if pleft > right:
                    break
                parents[find(index)] = find(pindex)
        previous = current
    groups = {}
    for index, run in enumerate(runs):
        groups.setdefault(find(index), []).append(run)
    for group in groups.values():
        r0, r1 = group[0][0], group[-1][0] + 1
        c0, c1 = min(run[1] for run in group), max(run[2] for run in group)
        component = np.zeros((r1 - r0, c1 - c0), dtype=bool)
        for row, left, right in group:
            component[row - r0, left - c0 : right - c0] = True
        yield component, slice(r0, r1), slice(c0, c1)


def filter_small_regions(mask, dropout):
    """按每个连通分块占整个采样网格的比例过滤碎块。"""
    if dropout == 0:
        return mask
    threshold = dropout * mask.size
    kept = np.zeros_like(mask, dtype=bool)
    if np.count_nonzero(mask) < threshold:
        return kept
    for component, rows, columns in connected_regions(mask):
        if np.count_nonzero(component) >= threshold:
            kept[rows, columns] |= component
    return kept


def label_disconnected_regions(ax, smart=True, preserve_offsets=False):
    regions = []
    for original, mask, xs, ys in getattr(ax, "_betu_regions", []):
        components = list(connected_regions(mask))
        offset = np.zeros(2)
        if preserve_offsets:
            rr, cc = np.nonzero(mask)
            offset = np.asarray(original.get_position()) - (
                xs[cc].mean(),
                ys[rr].mean(),
            )
        for index, (component, rows, columns) in enumerate(components):
            rr, cc = np.nonzero(component)
            cx, cy = xs[columns][cc], ys[rows][rr]
            distance = ((cx - cx.mean()) / max(np.ptp(xs), 1e-30)) ** 2 + (
                (cy - cy.mean()) / max(np.ptp(ys), 1e-30)
            ) ** 2
            closest = np.argmin(distance)
            position = np.asarray((cx[closest], cy[closest])) + offset
            if preserve_offsets and len(components) == 1:
                position = original.get_position()
            if index == 0:
                text = original
                text.set_position(position)
            else:
                text = ax.text(*position, original.get_text())
                text.update_from(original)
                text.set_position(position)
            text._betu_manual_label = preserve_offsets and bool(np.any(offset))
            regions.append((text, component, xs[columns], ys[rows]))
    ax._betu_regions = regions
    if smart:
        arrange_region_labels(ax)


def arrange_region_labels(ax):
    regions = getattr(ax, "_betu_regions", [])
    if not regions:
        return
    figure = ax.figure
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    occupied, external = [], []
    ax._betu_callouts = []
    # 大区域先占位，小区域在放不下文字时使用引导线。
    for text, mask, xs, ys in sorted(
        regions, key=lambda item: -np.count_nonzero(item[1])
    ):
        box = text.get_window_extent(renderer).expanded(1.12, 1.3)
        rows, columns = mask.shape
        indices = np.flatnonzero(mask)
        if not len(indices):
            continue
        indices = indices[
            np.linspace(0, len(indices) - 1, min(3000, len(indices)), dtype=int)
        ]
        rr, cc = np.unravel_index(indices, mask.shape)
        centers = ax.transData.transform(np.column_stack((xs[cc], ys[rr])))
        original = ax.transData.transform(text.get_position())
        candidates = np.argsort(np.sum((centers - original) ** 2, axis=1))
        if getattr(text, "_betu_manual_label", False):
            tx, ty = text.get_position()
            r, c = np.argmin(abs(ys - ty)), np.argmin(abs(xs - tx))
            contained = xs[0] <= tx <= xs[-1] and ys[0] <= ty <= ys[-1] and mask[r, c]
            if not contained:
                closest = candidates[0]
                anchor = (float(xs[cc[closest]]), float(ys[rr[closest]]))
                annotation = add_callout(ax, text, anchor, (tx, ty), "data")
                annotation._betu_external = False
            occupied.append(box)
            continue
        span = ax.transData.transform([(xs[0], ys[0]), (xs[-1], ys[-1])])
        dx = max(
            1,
            math.ceil(
                box.width / max(abs(span[1, 0] - span[0, 0]), 1e-9) * (columns - 1) / 2
            ),
        )
        dy = max(
            1,
            math.ceil(
                box.height / max(abs(span[1, 1] - span[0, 1]), 1e-9) * (rows - 1) / 2
            ),
        )
        integral = np.pad(mask.astype(np.int32), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        placed = False
        for index in candidates:
            r, c = rr[index], cc[index]
            if r - dy < 0 or c - dx < 0 or r + dy >= rows or c + dx >= columns:
                continue
            area = (
                integral[r + dy + 1, c + dx + 1]
                - integral[r - dy, c + dx + 1]
                - integral[r + dy + 1, c - dx]
                + integral[r - dy, c - dx]
            )
            if area != (2 * dy + 1) * (2 * dx + 1):
                continue
            cx, cy = centers[index]
            candidate = Bbox.from_bounds(
                cx - box.width / 2, cy - box.height / 2, box.width, box.height
            )
            if any(candidate.overlaps(other) for other in occupied):
                continue
            text.set_position((xs[c], ys[r]))
            occupied.append(candidate)
            placed = True
            break
        if not placed:
            index = candidates[0]
            anchor = (float(xs[cc[index]]), float(ys[rr[index]]))
            external.append((text, anchor, box.width, box.height))
    if not external:
        return
    external.sort(key=lambda item: (item[1][0], item[1][1]))
    width = max(item[2] for item in external) + 20
    columns = max(1, int(ax.bbox.width // width))
    rows = math.ceil(len(external) / columns)
    row_height = max(item[3] for item in external) / figure.dpi + 0.15
    ax._betu_label_rows = rows
    ax._betu_label_row_height = row_height
    for index, (text, anchor, _, _) in enumerate(external):
        row, col = divmod(index, columns)
        count = min(columns, len(external) - row * columns)
        annotation = add_callout(
            ax,
            text,
            anchor,
            ((col + 0.5) / count, 1),
            blended_transform_factory(ax.transAxes, figure.transFigure),
        )
        annotation._betu_label_row = row
        annotation._betu_external = True
        annotation.set_in_layout(False)
    band = rows * row_height + 0.2
    figure._betu_label_band = band
    figure.set_figheight(figure.get_figheight() + band)
    from ._plotting import layout_figure

    layout_figure(figure)


def add_callout(ax, text, anchor, position, coordinates):
    patch = text.get_bbox_patch()
    annotation = ax.annotate(
        text.get_text(),
        xy=anchor,
        xycoords="data",
        xytext=position,
        textcoords=coordinates,
        ha="center",
        va="center",
        fontproperties=text.get_fontproperties(),
        color=text.get_color(),
        bbox=dict(
            boxstyle="round,pad=0.22",
            fc=patch.get_facecolor() if patch else "white",
            ec="#555555",
            lw=0.5,
        ),
        arrowprops=dict(arrowstyle="->", color="#444444", lw=0.8, shrinkA=4, shrinkB=0),
        annotation_clip=False,
        zorder=8,
    )
    annotation._betu_region_label = text.get_text()
    ax._betu_callouts.append(annotation)
    text.set_visible(False)
    return annotation


def position_callouts(figure):
    """在标题或图例改变布局后，重新定位图外标签。"""
    band = getattr(figure, "_betu_label_band", 0)
    if not band:
        return
    for ax in figure.axes:
        callouts = [
            a
            for a in getattr(ax, "_betu_callouts", [])
            if getattr(a, "_betu_external", False)
        ]
        if not callouts:
            continue
        pos = ax.get_position()
        ax.set_position(
            [
                pos.x0,
                pos.y0,
                pos.width,
                max(0.12, pos.height - band / figure.get_figheight()),
            ]
        )
        title_space = (
            (ax.title.get_fontsize() / 72 + 0.12) if ax.title.get_text() else 0
        )
        bottom = ax.get_position().y1 * figure.get_figheight() + title_space + 0.2
        for annotation in callouts:
            x, _ = annotation.get_position()
            annotation.set_position(
                (
                    x,
                    (bottom + annotation._betu_label_row * ax._betu_label_row_height)
                    / figure.get_figheight(),
                )
            )
            annotation.set_in_layout(True)
