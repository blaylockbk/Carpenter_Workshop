# Brian Blaylock
# March 13, 2021

"""
=========================
NWS Standard Color Curves
=========================
Custom colormaps for standard meteorological variables with the necessary
bounds, ticks, and labels for building the colorbar.

Standardized colormaps from National Weather Service

- Source: Joseph Moore <joseph.moore@noaa.gov>
- Document: ./NWS Standard Color Curve Summary.pdf

TODO
- [ ] Units are a bit messed up. Units not factored into vmax/vmin args 

"""

import matplotlib as mpl

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotlib as mpl

def _display_cmap(ax=None, ticks=None, ticklabels=None,
                  cbar_shape=None,
                  fig_kw={},
                  **kwargs):
    """
    Display a colormap by itself.

    https://matplotlib.org/stable/api/colorbar_api.html?highlight=colorbarbase#matplotlib.colorbar.ColorbarBase
    
        The main application of using a ColorbarBase explicitly is drawing
        colorbars that are not associated with other elements in the figure,
        e.g. when showing a colormap by itself.
        --- Matplotlib Docs

    Parameters
    ----------
    ax : axes
    ticks : ticks locations
    ticklabels : labels for the tick locations
    cbar_shape : shape of a colorbar to create [x-pos, y-pos, width, height]
    fig_kw : figure kwargs
    kwargs : kwargs for ColorbarBase
    """
    kwargs.setdefault('orientation', 'horizontal')
    fig_kw.setdefault('figsize', (8,3))
    
    if ax is None:
        # Display Colorbar as Standalone. Create new figure.
        fig = plt.figure(**fig_kw)
        if kwargs['orientation'] == 'horizontal':
            ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])   # [x-pos, y-pos, width, height]
        else:
            ax = fig.add_axes([0.05, 0.80, 0.05, 2])
    elif ax is not None and cbar_shape is None:
        # Auto create a colorbar to an axis
        if kwargs['orientation'] == 'horizontal':
            ax = ax.get_figure().add_axes([.1, 0.05, 0.8, 0.05])
        else:
            ax = ax.get_figure().add_axes([.91, 0.1, 0.05, 0.8])
    else:
        # Use the values specified by cbar_shape to add the colorbar to a figure
        ax = ax.get_figure().add_axes(cbar_shape)

    cbar = mpl.colorbar.ColorbarBase(ax, **kwargs)

    if ticks is not None:
        cbar.set_ticks(ticks)
    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels)
    
    return cbar

class cm_tmp:
    def __init__(self, levels=40, vmin=-50, vmax=50):
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Temperature'
        self.units = '$\degree$C'
        self.label = f"{self.name} ({self.units})"
        self.COLORS = np.array([
            '#91003f', '#ce1256', '#e7298a', '#df65b0',
            '#ff73df', '#ffbee8', '#ffffff', '#dadaeb',
            '#bcbddc', '#9e9ac8', '#756bb1', '#54278f',
            '#0d007d', '#0d3d9c', '#0066c2', '#299eff',
            '#4ac7ff', '#73d7ff', '#adffff', '#30cfc2',
            '#009996', '#125757', '#066d2c', '#31a354',
            '#74c476', '#a1d99b', '#d3ffbe', '#ffffb3',
            '#ffeda0', '#fed176', '#feae2a', '#fd8d3c',
            '#fc4e2a', '#e31a1c', '#b10026', '#800026',
            '#590042', '#280028'
        ])
    
        if self.levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name,
                                                                  self.COLORS)
        else:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name,
                                                                  self.COLORS,
                                                                  N=self.levels)
        
        self.norm = mcolors.Normalize(self.vmin, self.vmax)
        
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, extend='both')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar

class cm_dpt:
    def __init__(self, vmin=-10, vmax=80, levels=15):
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Dew Point Temperature'
        self.units = '$\degree$C'
        self.label = f"{self.name} ({self.units})"
        self.COLORS = np.array([
            '#3b2204', '#543005', '#8c520a', '#bf812d',
            '#cca854', '#dfc27d', '#e6d9b5', '#d3ebe7',
            '#a9dbd3', '#72b8ad', '#318c85', '#01665f',
            '#003c30', '#002921'
        ])
        self.bounds = np.array([-10, 0, 10, 20, 30, 40, 45, 50, 
                                 55, 60, 65, 70, 75, 80])
        if levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS)
            self.norm = mcolors.Normalize(self.vmin, self.vmax)
        else:
            logic = np.logical_and(self.bounds >=vmin, self.bounds <= vmax)
            self.COLORS = self.COLORS[logic]
            self.bounds = self.bounds[logic]
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS,
                                                                  N=len(self.COLORS)+1)
            self.norm = mcolors.BoundaryNorm(boundaries=self.bounds,
                                             ncolors=len(self.bounds))
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, extend='both', ticks=self.bounds, spacing='proportional')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar

class cm_rh:
    def __init__(self, vmin=0, vmax=100, levels=15):
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Relative Humidity'
        self.units = '%'
        self.label = f"{self.name} ({self.units})"
        self.COLORS = np.array([
            '#910022', '#a61122', '#bd2e24', '#d44e33',
            '#e36d42', '#fa8f43', '#fcad58', '#fed884',
            '#fff2aa', '#e6f49d', '#bce378', '#71b55c',
            '#26914b', '#00572e',  'k'])
        self.bounds = np.array([0,5,10,15,
                                20,25,30,35,
                                40,50,60,70,
                                80, 90, 100])
        
        if levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS)
            self.norm = mcolors.Normalize(self.vmin, self.vmax)
        else:
            logic = np.logical_and(self.bounds >=vmin, self.bounds <= vmax)
            self.COLORS = self.COLORS[logic]
            self.bounds = self.bounds[logic]
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS,
                                                                  N=len(self.COLORS)+1)
            self.norm = mcolors.BoundaryNorm(boundaries=self.bounds,
                                             ncolors=len(self.bounds))
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, ticks=self.bounds, spacing='proportional')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar
        
class cm_wind:
    def __init__(self, vmin=0, vmax=140, levels=18, units='m/s'):
        _units = ['m/s', 'kn', 'km/h', 'mph']
        assert units in _units, f"units must be one of {_units}"
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Wind Speed'
        self.COLORS = np.array([
            '#103f78', '#225ea8', '#1d91c0', '#41b6c4',
            '#7fcdbb', '#b4d79e', '#dfff9e', '#ffffa6',
            '#ffe873', '#ffc400', '#ffaa00', '#ff5900',
            '#ff0000', '#a80000', '#6e0000', '#ffbee8',
            '#ff73df'
        ])
        
        # These are in m/s
        self.bounds = np.array([0, 5, 10, 15, 
                                20, 25, 30, 35, 
                                40, 45, 50, 60, 
                                70, 80, 100, 120, 
                                140], dtype=float)
        
        if units == 'm/s':
            self.units = 'm s$\mathregular{^{-1}}$'
        elif units == 'mph':
            self.units = 'mph'
            self.bounds *= 2.23693629
            self.vmin *= 2.23693629
            self.vmax *= 2.23693629
        elif units == 'km/h':
            self.units = 'km h$\mathregular{^{-1}}$'
            self.bounds *= 3.6
            self.vmin *= 3.6
            self.vmax *= 3.6
        elif units == 'kn':
            self.units = 'kn'
            self.bounds *= 1.94384449
            self.vmin *= 1.94384449
            self.vmax *= 1.94384449
            
            
        self.label = f"{self.name} ({self.units})"
        
        if levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS)
            self.norm = mcolors.Normalize(self.vmin, self.vmax)
        else:
            logic = np.logical_and(self.bounds >=vmin, self.bounds <= vmax)
            self.COLORS = self.COLORS[logic]
            self.bounds = self.bounds[logic]
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS,
                                                                  N=len(self.COLORS)+1)
            self.norm = mcolors.BoundaryNorm(boundaries=self.bounds,
                                             ncolors=len(self.bounds))
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, extend='max', ticks=self.bounds, spacing='proportional')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar
        
class cm_cloud:
    def __init__(self, vmin=0, vmax=100, levels=15):
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Cloud Cover'
        self.units = '%'
        self.label = f"{self.name} ({self.units})"
        self.COLORS = np.array([
            '#24a0f2', '#4eb0f2', '#80b7f8', '#a0c8ff', '#d2e1ff',
            '#e1e1e1', '#c9c9c9', '#a5a5a5', '#6e6e6e', '#505050', 'k'])
        self.bounds = np.arange(0,101,10)
        
        if levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS)
            self.norm = mcolors.Normalize(self.vmin, self.vmax)
        else:
            logic = np.logical_and(self.bounds >=vmin, self.bounds <= vmax)
            self.COLORS = self.COLORS[logic]
            self.bounds = self.bounds[logic]
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS,
                                                                  N=len(self.COLORS)+1)
            self.norm = mcolors.BoundaryNorm(boundaries=self.bounds,
                                             ncolors=len(self.bounds))
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, ticks=self.bounds, spacing='proportional')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar

class cm_pcp:
    def __init__(self, vmin=0, vmax=762, levels=15, units='mm'):
        assert units in ['mm', 'in'], 'units must be "mm" or "in"'
        self.levels = levels
        self.vmin = vmin
        self.vmax = vmax
        self.name = 'Precipitation'
        self.units = units
        self.label = f"{self.name} ({self.units})"
        self.COLORS = np.array([
            '#ffffff', '#c7e9c0', '#a1d99b', '#74c476', '#31a353', '#006d2c',
            '#fffa8a', '#ffcc4f', '#fe8d3c', '#fc4e2a', '#d61a1c', '#ad0026',
            '#700026', '#3b0030', '#4c0073', '#ffdbff'])
        
        # These are in inches
        self.bounds = np.array([0,.01,.1,.25,.5,1,1.5,2,3,4,6,8,10,15,20,30])
        
        if units == 'mm':
            self.bounds *= 25.4
            self.vmin *= 25.4
            self.vmax *= 25.4
        
        if levels is None:
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS)
            self.norm = mcolors.Normalize(self.vmin, self.vmax)
        else:
            logic = np.logical_and(self.bounds >=vmin, self.bounds <= vmax)
            self.COLORS = self.COLORS[logic]
            self.bounds = self.bounds[logic]
            self.cmap = mcolors.LinearSegmentedColormap.from_list(self.name, 
                                                                  self.COLORS,
                                                                  N=len(self.COLORS)+1)
            self.norm = mcolors.BoundaryNorm(boundaries=self.bounds,
                                             ncolors=len(self.bounds))
        self.cmap_kwargs = dict(cmap=self.cmap, norm=self.norm)
        self.cbar_kwargs = dict(label=self.label, ticks=self.bounds, spacing='proportional')

    def display(self, ax=None, ticklabels=None, fig_kw={}, **kwargs):
        cbar = _display_cmap(ax, ticklabels=ticklabels, fig_kw=fig_kw, **kwargs, **self.cmap_kwargs, **self.cbar_kwargs)
        return cbar