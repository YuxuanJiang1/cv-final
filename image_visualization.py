import itertools
import re
from textwrap import wrap
import matplotlib.pyplot as plt


def get_n_rows(n_items, n_cols):
    return (n_items - 1) // n_cols + 1


def bf(s):
    return r'$\bf{' + s.replace(' ', '~') + r'}$'


def image_subplots(
    nrows=1, ncols=1,
    fig_width=8.,
    gridspec_kw={'wspace': 0.025, 'hspace': 0.25},
    aspect=1.,
    squeeze=False,
    **kwargs
):
    image_width = fig_width / (ncols + (ncols - 1) * gridspec_kw['wspace'])
    image_height = image_width / aspect
    fig_height = image_height * (nrows + (nrows - 1) * gridspec_kw['hspace'])
    fig, ax = plt.subplots(
        nrows, ncols,
        figsize=(fig_width, fig_height),
        squeeze=squeeze,
        gridspec_kw=gridspec_kw,
        **kwargs
    )
    return fig, ax, image_width


def get_wrap_width(fontsize, image_width, c=100.):
    return int(c * image_width / fontsize)


def add_caption(
    ax,
    caption,
    x=0.025, y=-0.05,
    fontsize=5.,
    wrap_width=None,
    image_width=None,
    **kwargs
):
    if wrap_width is None:
        wrap_width = get_wrap_width(fontsize, image_width)
    if isinstance(caption, str):
        caption = wrap(caption, wrap_width)
    elif isinstance(caption, list):
        caption = [wrap(caption_i, wrap_width) for caption_i in caption]
        caption = list(itertools.chain.from_iterable(caption))
    return ax.text(
        x, y,
        "\n".join(caption),
        ha='left', va='top',
        transform=ax.transAxes,
        fontsize=fontsize,
    )
