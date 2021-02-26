## Brian Blaylock
## March 23, 2020    COVID-19 Era

"""
==================
Matplotlib Helpers
==================

Some helpers for plotting
    
    - _infer_interval_breaks : this helper is for pcolormesh
    - center : center an axes xlim and ylim by a value.

"""

import numpy as np
import matplotlib.pyplot as plt

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
    trim_last = tuple(slice(None, -1) if n==axis else slice(None) for n in range(coord.ndim))
    
    coord = np.concatenate([first, coord[trim_last]+deltas, last], axis=axis)
    
    if coord.ndim == 1:
        return coord

    axis = 1
    deltas = 0.5 * np.diff(coord, axis=axis)
    first = np.take(coord, [0], axis=axis) - np.take(deltas, [0], axis=axis)
    last = np.take(coord, [-1], axis=axis) + np.take(deltas, [-1], axis=axis)
    trim_last = tuple(slice(None, -1) if n==axis else slice(None) for n in range(coord.ndim))
    
    coord = np.concatenate([first, coord[trim_last]+deltas, last], axis=axis)
    
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

def add_fig_letters(axes):
    """
    Add a figure letter to top-left corner for all axes
    
    Like is done in a publication figure, all axes are labeled with a
    letter so individual axes can be referred to from the text.

    Example
    -------
    
    .. code-block: python
        
        fig, axes = plt.subplots(4,4)
        add_fig_letters(axes)

    """
    if not hasattr(axes, 'flat'): 
        np.array(axes)
    ### Add letters to plots
    import string
    
    try:
        axes = axes.flat 
    except:
        pass

    for i, (ax, letter) in enumerate(zip(axes, string.ascii_lowercase)):
        plt.sca(ax)

        # Add figure letter
        box_prop = dict(boxstyle='round',
                        facecolor='wheat',
                        alpha=1,
                        linewidth=.5)
        
        plt.text(0, 1, f'{letter}', 
                 transform=ax.transAxes, fontfamily='monospace',
                 va='top', ha='left', 
                 bbox=box_prop, zorder=10_000)