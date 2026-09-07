"""Supplementary plotting code with Documents-relative save paths."""

import ast
import os
from pathlib import Path
from ._plotting import layout_figure


def documents_dir():
    """Respect Windows' redirected Documents folder (including OneDrive)."""
    if os.name == "nt":
        import ctypes

        buffer = ctypes.create_unicode_buffer(32768)
        if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buffer) == 0:
            return Path(buffer.value)
    return Path.home() / "Documents"


def resolve_save_path(filename):
    path = Path(filename).expanduser()
    if not path.is_absolute():
        path = documents_dir() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def check_advanced_syntax(code):
    """Compile without execution; report line/column through SyntaxError."""
    return compile(code or "", "<BeTu>", "exec")


def _fit_titles(figure):
    """Reserve a little extra height once, before either preview or save."""
    titles = (
        [ax._left_title for ax in figure.axes]
        + [ax.title for ax in figure.axes]
        + [ax._right_title for ax in figure.axes]
    )
    if figure._suptitle is not None:
        titles.append(figure._suptitle)
    titles = [title for title in titles if title.get_text()]
    if not titles:
        return
    signature = tuple((title.get_text(), title.get_fontsize()) for title in titles)
    if signature == getattr(figure, "_betu_title_signature", None):
        return
    width, height = figure.get_size_inches()
    base_height = getattr(figure, "_betu_title_base_height", height)
    figure._betu_title_base_height = base_height
    extra = max(
        0.35,
        max(
            title.get_fontsize() * (title.get_text().count("\n") + 1)
            for title in titles
        )
        / 72
        * 1.6
        + 0.1,
    )
    figure.set_size_inches(width, max(height, base_height + extra), forward=True)
    layout_figure(figure, pad=1.2)
    if any(getattr(ax, "name", "") == "3d" for ax in figure.axes):
        figure.subplots_adjust(
            top=min(figure.subplotpars.top, 1 - extra / figure.get_figheight())
        )
    figure._betu_title_signature = signature


class _PlotProxy:
    def __init__(self, pyplot):
        self._pyplot = pyplot

    def __getattr__(self, name):
        return getattr(self._pyplot, name)

    def title(self, *args, **kwargs):
        result = self._pyplot.title(*args, **kwargs)
        _fit_titles(self._pyplot.gcf())
        return result

    def suptitle(self, *args, **kwargs):
        result = self._pyplot.suptitle(*args, **kwargs)
        _fit_titles(self._pyplot.gcf())
        return result

    def savefig(self, fname, *args, **kwargs):
        _fit_titles(self._pyplot.gcf())
        if isinstance(fname, (str, os.PathLike)):
            fname = resolve_save_path(fname)
        return self._pyplot.savefig(fname, *args, **kwargs)


def run_advanced(the_plt, code="", namespace=None):
    """Execute the user's Python code after plotting and before display.

    This is ordinary Python execution, not a sandbox. The local proxy only
    changes relative paths passed to the_plt.savefig, without changing cwd.
    """
    compiled = check_advanced_syntax(code)
    scope = dict(namespace or {})
    scope["the_plt"] = _PlotProxy(the_plt)
    exec(compiled, scope)
    _fit_titles(the_plt.gcf())
    return scope


def plot_context(pyplot):
    return _PlotProxy(pyplot)
