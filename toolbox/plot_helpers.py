## Brian Blaylock
## March 23, 2020    COVID-19 Era

"""
==================
Matplotlib Helpers
==================

Some helpers for plotting

This was a good primer on Matplotlib:
https://dev.to/skotaro/artist-in-matplotlib---something-i-wanted-to-know-before-spending-tremendous-hours-on-googling-how-tos--31oo

"""
import pickle
import os
import string
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms

# Sometimes it is useful to put this at the top of your scripts to
# format the date axis formatting.
# - plt.rcParams['date.autoformatter.day'] = '%b %d\n%H:%M'
# - plt.rcParams['date.autoformatter.hour'] = '%b %d\n%H:%M'


BB_mplstyle_path = Path(os.path.abspath(__file__)).parent / "BB.mplstyle"


def list_fonts():
    fonts = sorted([f.name for f in mpl.font_manager.fontManager.ttflist])
    return np.unique(fonts)


def copy_fig(fig):
    """
    Copy a figure

    See comment by jmetz: https://stackoverflow.com/a/45812071/2383070
    """
    return pickle.loads(pickle.dumps(fig))


def date_axis_ticks(ax=None, locator="day", major=3, minor=1, fmt=None, minor_fmt=None):
    """
    Set tick intervals for a date axis.

    I always forget how to do this, so I hope this will jog my memory.
    For reference: https://matplotlib.org/stable/api/dates_api.html

    Parameters
    ----------
    locator : {'day', 'hour'}
        Place ticks on every day or every hour.
    major, minor : int
        Tick interval for major and minor ticks.
    fmt : str
        String format for the dates. Default is None.
        A popular dateformat is ``"%b %d\n%H:%M"``.
    """
    if ax is None:
        ax = plt.gca()

    # Where ticks should be placed
    if locator.lower() == "day":
        if major is not None:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=major))
        if minor is not None:
            ax.xaxis.set_minor_locator(mdates.DayLocator(interval=minor))
    elif locator.lower() == "hour":
        if major is not None:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=major))
        if minor is not None:
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=minor))

    # Format Date Tick String
    if fmt is not None:
        ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    if minor_fmt is not None:
        ax.xaxis.set_minor_formatter(mdates.DateFormatter(minor_fmt))


def scatter_density(x, y, ax=None, **kwargs):
    """
    Plot a scatter density plot

    See example here: https://gist.github.com/blaylockbk/3190e0c21e11b5a25e09731c7ae46ad3
    """
    if ax is None:
        ax = plt.gca()

    kwargs.setdefault("c", "tab:blue")
    kwargs.setdefault("lw", 0)
    kwargs.setdefault("alpha", 0.25)
    kwargs.setdefault("s", 40)
    kwargs.setdefault("zorder", 10)

    ax.scatter(
        x, y, s=kwargs["s"], zorder=kwargs["zorder"] - 1, color="0.2", lw=1
    )  # dark grey outline
    ax.scatter(
        x, y, s=kwargs["s"], zorder=kwargs["zorder"] - 1, color="1.0", lw=0
    )  # cover overlapping edges
    ax.scatter(x, y, **kwargs)  # fill color


def _infer_interval_breaks(coord):
    """
    Infer grid spacing interval for plotting pcolormesh as center points.

    Adapted from xarray: (github/pydata/xarray/plot/utils)

    If you want to plot with pcolormesh, it will chop off the last
    row/column because pcolormesh uses the box edges as the vertices,
    and not the center of the box. This function infers the gridpoints
    to position the dat points in the center of the plotted box pixel.

    This is slightly different from the xarray code in that this
    performs the infering on both axes (if available) before returning
    the final product.

    Parameters
    ----------
    coord : array_like
        Array of x or y coordinate values.

    Returns
    -------
    Array of coordinates that allow pcolormesh to show box centered on
    the data point.


    Examples
    --------
    >>> LON, LAT = np.meshgrid(np.arange(-120, -110), np.arange(30, 40))
    >>> DATA = LON*LAT
    >>> pLON = utils.gridded_data._infer_interval_breaks(LON)
    >>> pLAT = utils.gridded_data._infer_interval_breaks(LAT)
    >>> plt.pcolormesh(LON, LAT, DATA, alpha=.5)   # grid color data at bottom-left corner
    >>> plt.pcolormesh(pLON, pLAT, DATA, alpha=.5) # grid color data at center
    """
    axis = 0
    deltas = 0.5 * np.diff(coord, axis=axis)
    first = np.take(coord, [0], axis=axis) - np.take(deltas, [0], axis=axis)
    last = np.take(coord, [-1], axis=axis) + np.take(deltas, [-1], axis=axis)
    trim_last = tuple(
        slice(None, -1) if n == axis else slice(None) for n in range(coord.ndim)
    )

    coord = np.concatenate([first, coord[trim_last] + deltas, last], axis=axis)

    if coord.ndim == 1:
        return coord

    axis = 1
    deltas = 0.5 * np.diff(coord, axis=axis)
    first = np.take(coord, [0], axis=axis) - np.take(deltas, [0], axis=axis)
    last = np.take(coord, [-1], axis=axis) + np.take(deltas, [-1], axis=axis)
    trim_last = tuple(
        slice(None, -1) if n == axis else slice(None) for n in range(coord.ndim)
    )

    coord = np.concatenate([first, coord[trim_last] + deltas, last], axis=axis)

    return coord


def center_axis_on_zero(x=True, y=False, ax=None):
    """
    Center a plot on zero along the x and/or y axis.

    Parameters
    ----------
    x, y: bool
        Center the figure for the x and/or y axis.
    """
    if ax is None:
        ax = plt.gca()

    if x:
        left, right = ax.get_xlim()
        lr_max = np.maximum(np.abs(left), np.abs(right))
        ax.set_xlim(-lr_max, lr_max)

    if y:
        down, up = ax.get_ylim()
        du_max = np.maximum(np.abs(down), np.abs(up))
        ax.set_ylim(-du_max, du_max)


def add_fig_letters(axes, bbox={}, **kwargs):
    """Add a figure letter to top-left corner for all axes.

    This is useful for publication figure; all axes are labeled with a
    letter so individual axes can be referred to from the text.

    https://matplotlib.org/stable/gallery/text_labels_and_annotations/label_subplots.html

    Parameters
    ----------
    axes : dict, array, or list of matplotlib axes
        matplotlib axes to label

    Examples
    --------

    .. code-block: python

        fig, axes = plt.subplots(4,4)
        add_fig_letters(axes)

    .. code-block: python

        axd = plt.figure().subplot_mosaic(
            '''
            AAAA
            BBCC
            BBCC
            DDCC
            '''
        )
        add_labels(axd)

    """

    # Style the label
    bbox.setdefault("boxstyle", "round")
    bbox.setdefault("facecolor", "#f9ecd2")
    bbox.setdefault("alpha", 1)
    bbox.setdefault("linewidth", 0.5)
    bbox.setdefault("pad", 0.35)

    # Position the label
    kwargs.setdefault("fontfamily", "monospace")
    kwargs.setdefault("va", "top")
    kwargs.setdefault("ha", "left")
    kwargs.setdefault("zorder", 100_000)

    def add_label(ax, label):
        fig = ax.get_figure()

        # These numbers adjust the position of the label (in and down)
        trans = mtransforms.ScaledTranslation(6 / 72, -6 / 72, fig.dpi_scale_trans)

        ax.text(
            0.0, 1.0, f"{label}", transform=ax.transAxes + trans, bbox=bbox, **kwargs
        )

    if isinstance(axes, dict):
        # For axes that are made by plt.figure().subplot_mosaic()
        for label, ax in axes.items():
            add_label(ax, label)
    elif isinstance(axes, (np.ndarray, list)):
        # For axes that are made by plt.subplots()
        axes = np.array(axes).flat
        labels = string.ascii_letters
        for label, ax in zip(labels, axes):
            add_label(ax, label)
