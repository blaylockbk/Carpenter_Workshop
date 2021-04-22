
## Brian Blaylock
## February 3, 2021 

"""
=============
Cartopy Tools
=============

General helpers for cartopy plots.

"""
import warnings

import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import xarray as xr
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as feature
import cartopy.io.img_tiles as cimgt
from cartopy.io import shapereader

try:
    from metpy.plots import USCOUNTIES
except Exception as e:
    print(f"WARNING! {e}")
    print('Without metpy, you cannot draw USCOUNTIES on the map.')
try:
    import geopandas
except Exception as e:
    print(f"WARNING! {e}")
    print('Without geopandas, you cannot subset some'
          'NaturalEarthFeatures, like "Major Highways" from roads.')

pc = ccrs.PlateCarree()

########################################################################
# Methods attached to axes created by `common_features`
def _adjust_extent(self, pad='auto', fraction=.05, verbose=False):
    """
    Adjust the extent of an existing cartopy axes.

    This is useful to fine-tune the extent of a map after the extent 
    was automatically made by a cartopy plotting method.    
    
    Parameters
    ----------
    pad : float or dict
        If float, pad the map the same on all sides. Default is half a degree.
        If dict, specify pad on each side.
            - 'top' - padding north of center point
            - 'bottom'- padding south of center point
            - 'left' - padding east of center point
            - 'right' - padding west of center point
            - 'default' - padding when pad is unspecified 
        Example: ``pad=dict(top=.5, default=.2)`` is the same as
                 ``pad=dict(top=.5, bottom=.2, left=.2, right=.2)``
        Note: Use negative numbers to remove padding.
    fraction : float
        When pad is 'auto', adjust the sides by a set fraction.
        The default 0.05 will give 5% padding on each side.
    """
    # Can't shrink the map extent by more than half in each direction, duh.
    assert fraction > -.5, "Fraction must be larger than -0.5."
        
    crs = self.projection
    
    west, east, south, north = self.get_extent(crs=crs)

    if pad == 'auto':
        pad = {}
    
    if isinstance(pad, dict):
        xmin, xmax = self.get_xlim()
        default_pad = (xmax-xmin) * fraction
        pad.setdefault('default', default_pad)
        for i in ['top', 'bottom', 'left', 'right']:
            pad.setdefault(i, pad['default'])
    else:
        pad = dict(top=pad, bottom=pad, left=pad, right=pad)

    ymin, ymax = crs.y_limits
    north = np.minimum(ymax, north + pad['top'])
    south = np.maximum(ymin, south - pad['bottom'])
    east = east + pad['right']
    west = west - pad['left']

    self.set_extent([west, east, south, north], crs=crs)

    if verbose: print(f"📐 Adjust Padding for {crs.__class__}: {pad}")
    
    return self.get_extent(crs=crs) 

def _center_extent(self, lon, lat, *, pad='auto', verbose=False):
    """
    Change the map extent to be centered on a point and adjust padding.

    Parameters
    ----------
    lon, lat : float
        Latitude and Longitude of the center point **in degrees**.
    pad : float or dict
        Default is 'auto', which defaults to ~5 degree padding on each side.
        If float, pad the map the same on all sides (in crs units).
        If dict, specify pad on each side (in crs units).
            - 'top' - padding north of center point
            - 'bottom'- padding south of center point
            - 'left' - padding east of center point
            - 'right' - padding west of center point
            - 'default' - padding when pad is unspecified (default is 5)
        Example: ``pad=dict(top=5, default=10)`` is the same as
                 ``pad=dict(top=5, bottom=10, left=10, right=10)``
    """
    crs = self.projection

    # Convert input lat/lon in degrees to the crs units
    lon, lat = crs.transform_point(lon, lat, src_crs=pc)

    if pad == 'auto':
        pad = dict()
    
    if isinstance(pad, dict):
        # This default gives 5 degrees padding on each side
        # for a PlateCarree projection. Pad is similar for other 
        # projections but not exactly 5 degrees.
        xmin, xmax = crs.x_limits
        default_pad = (xmax-xmin)/72        # Because 360/72 = 5 degrees
        pad.setdefault('default', default_pad)
        for i in ['top', 'bottom', 'left', 'right']:
            pad.setdefault(i, pad['default'])
    else:
        pad = dict(top=pad, bottom=pad, left=pad, right=pad)
        
    ymin, ymax = crs.y_limits
    north = np.minimum(ymax, lat + pad['top'])
    south = np.maximum(ymin, lat - pad['bottom'])
    east = lon + pad['right']
    west = lon - pad['left']
    
    self.set_extent([west, east, south, north], crs=crs)
    
    if verbose: print(f"📐 Padding from point for {crs.__class__}: {pad}")
        
    return self.get_extent(crs=crs) 

def _copy_extent(self, src_ax):
    """
    Copy the extent from an axes. 
    
    .. note:: 
        Copying extent from different projections might not result in
        what you expect.

    Parameters
    ----------
    src_ax : cartopy axes
        A source cartopy axes to copy extent from onto the existing axes.

    Examples
    --------
    >>> # Copy extent of ax2 to ax1
    >>> ax1.copy_extent(ax2)

    """
    src_ax = check_cartopy_axes(src_ax)

    self.set_extent(src_ax.get_extent(crs=pc), crs=pc)

    return self.get_extent(crs=pc)

########################################################################
# Main Functions
def check_cartopy_axes(ax=None, crs=pc, *, verbose=False):
    """
    Check if an axes is a cartopy axes, else create a new cartopy axes.
    
    Parameters
    ----------
    ax : {None, cartopy.mpl.geoaxes.GeoAxesSubplot}
        If None and plt.gca() is a cartopy axes, then use current axes.
        Else, create a new cartopy axes with specified crs.
    crs : cartopy.crs
        If the axes being checked is not a cartopy axes, then create one
        with this coordinate reference system (crs, aka "projection").
        Default is ccrs.PlateCarree()
    """    
    # A cartopy axes should be of type `cartopy.mpl.geoaxes.GeoAxesSubplot`
    # One way to check that is to see if ax has the 'coastlines' attribute.
    if ax is None:
        if hasattr(plt.gca(), 'coastlines'):
            if verbose: print('🌎 Using the current cartopy axes.')
            return plt.gca()  
        else:
            if verbose: print(f'🌎 The current axes is not a cartopy axes. Will create a new cartopy axes with crs={crs.__class__}.')
            # Close the axes we just opened in our test
            plt.close() 
            # Create a new cartopy axes
            return plt.axes(projection=crs)
    else:
        if hasattr(ax, 'coastlines'):
            if verbose: print('🌎 Thanks! It appears the axes you provided is a cartopy axes.')
            return ax
        else:
            raise TypeError('🌎 Sorry. The `ax` you gave me is not a cartopy axes.')

def common_features(scale='110m', ax=None, crs=pc, *, figsize=None, dpi=None,
                    counties_scale='20m', dark=False, verbose=False,                   
                    COASTLINES=True, COASTLINES_kwargs={},
                    BORDERS=False,   BORDERS_kwargs={},
                    STATES=False,    STATES_kwargs={},
                    COUNTIES=False,  COUNTIES_kwargs={},
                    OCEAN=False,     OCEAN_kwargs={},
                    LAND=False,      LAND_kwargs={},
                    RIVERS=False,    RIVERS_kwargs={},
                    LAKES=False,     LAKES_kwargs={},
                    ROADS=False,     ROADS_kwargs={},
                    STAMEN=False,    STAMEN_kwargs={},
                    OSM=False,       OSM_kwargs={},             
                    **kwargs):
    """
    Add common features to a cartopy axis. 
    
    This completes about 95% of my cartopy needs.
    
    .. tip:: This is a great way to initialize a new cartopy axes.

    Parameters
    ----------
    scale : {'10m', '50m' 110m'}
        The cartopy feature's level of detail.
        .. note::  The ``'10m'`` scale for OCEAN and LAND takes a *long* time.    
    ax : plot axes
        The axis to add the feature to.
        If None, it will create a new cartopy axes with ``crs``.
    crs : cartopy.crs
        Coordinate reference system (aka "projection") to create new map
        if no cartopy axes is given. Default is ccrs.PlateCarree.
    dark : bool
        If True, use alternative "dark theme" colors for land and water.
        
        .. figure:: _static/BB_maps/common_features-1.png
        .. figure:: _static/BB_maps/common_features-2.png

    counties_scale: {'20m', '5m', '500k'}
        Counties are plotted via MetPy and have different resolutions 
        available than other features.
        -  20m = 20,000,000 resolution (Ok if you show a large area)
        -   5m =  5,000,000 resolution (provides good detail)
        - 500k =    500,000 resolution (high resolution, plots very slow)
    figsize : tuple
        Set the figure size
    dpi : int
        Set the figure dpi
    FEATURES : bool
        Toggle on various features. By default, only COASTLINES is
        turned on. Each feature has a cooresponding ``FEATURE_kwargs={}``
        dictionary to supply additional arguments to cartopy's add_feature
        method (e.g., change line color or width by feature type).

        ========== =========================================================
        FEATURE    Description
        ========== =========================================================
        COASTLINES Coastlines, boundary between land and ocean.
        BORDERS    Borders between countries. *Does not includes coast*.
        STATES     US state borders. Includes coast.
        COUNTIES   US Counties. Includes coast.
        OCEAN      Colored ocean area
        LAND       Colored land area
        RIVERS     Lines where rivers exist
        LAKES      Colored lake area
        ROADS      All major roads. Can break filter by road type.
        ========== =========================================================
    
        ========== =========================================================
        MAP TILE   Description
        ========== =========================================================
        Stamen     Specify type and zoom level. http://maps.stamen.com/
                   Style: ``terrain-background``, ``terrain``, 
                          ``toner-background``, ``toner``, `watercolor``
                   zoom: int [0-10]
                   alpha: [0-1]
                   alpha_color: an overlay color to put on top of map
                        use 'k' to darken background
                        use 'w' to lighten background
        OSM        Open Street Maps
                   zoom: int
        ========== =========================================================

    .. note::
        For ``ROADS_kwargs`` you may provide a key for 'type' to filter 
        out the types of roads you want. The road type may be a single
        string or a list of road types. For example
        ``ROADS_kwargs=dict(type='Major Highway')`` or
        ``ROADS_kwargs=dict(type=['Secondary Highway', 'Major Highway'])
        
        Of course, the shapefile has many other road classifiers for each
        road, like "level" (Federal, State, Interstate), road "name",
        "length_km", etc. Filters for each of these could be added if I
        need them later.

    .. note::
        When adding a tile product to a map, it might be better to add
        it to the map first, then set the map extent, then make a separate
        call to ``common_features`` to add other features like roads and
        counties. The reason is because, if you add a tile map to  

    Methods
    -------
    .adjust_extent
    .center_extent
    .copy_extent
    
    Examples
    --------
    https://github.com/blaylockbk/Carpenter_Workshop/blob/main/notebooks/demo_cartopy_tools.ipynb
        
    Returns
    -------
    The cartopy axes (obviously you don't need this if you gave an ax
    as an argument, but it is useful if you initialize a new map).

    """

    ax = check_cartopy_axes(ax=ax, crs=crs, verbose=verbose)
    
    if (LAND or OCEAN) and scale in ['10m']:
        if verbose: warnings.warn('🕖 OCEAN or LAND features at 10m may take a long time (3+ mins) to display on large maps.')
    
    kwargs.setdefault('linewidth', .75)
    
    COASTLINES_kwargs.setdefault('zorder', 100)
    COASTLINES_kwargs.setdefault('facecolor', 'none')
    
    COUNTIES_kwargs.setdefault('linewidth', .5)
    
    STATES_kwargs.setdefault('alpha', .15)
    
    LAND_kwargs.setdefault('edgecolor', 'none')
    LAND_kwargs.setdefault('linewidth', 0)
    
    OCEAN_kwargs.setdefault('edgecolor', 'none')
    
    LAKES_kwargs.setdefault('linewidth', 0)

    # NOTE: I don't use the 'setdefault' method here because it doesn't 
    # work as expect when switching between dark and normal themes.
    # The defaults would be set the first time the function is called,
    # but the next time it is called and `dark=True` the defaults do not
    # reset. I don't know why this is the behavior.
    if dark:
        land = '#060613'
        water = '#0f2b38'
        
        # https://github.com/SciTools/cartopy/issues/880
        ax.set_facecolor(land)  # requires cartopy >= 0.18

        kwargs = {**{'edgecolor':'.5'}, **kwargs}
        LAND_kwargs = {**{'facecolor': land}, **LAND_kwargs}
        OCEAN_kwargs = {**{'facecolor': water}, **OCEAN_kwargs}
        RIVERS_kwargs = {**{'edgecolor': water}, **RIVERS_kwargs}
        LAKES_kwargs = {**{'facecolor': water}, **LAKES_kwargs}
        
    else:
        kwargs = {**{'edgecolor':'.15'}, **kwargs}
        RIVERS_kwargs = {**{'edgecolor': feature.COLORS['water']}, **RIVERS_kwargs}
        LAKES_kwargs = {**{'edgecolor': feature.COLORS['water']}, **LAKES_kwargs}

    ##------------------------------------------------------------------
    ## Add each element to the plot
    ## When combining kwargs, 
    ##  - kwargs is the main value
    ##  - FEATURE_kwargs is the overwrite for the feature
    ## For example:
    ##     {**kwargs, **FEATURE_kwargs}
    ## the kwargs are overwritten by FEATURE_kwargs
    ##------------------------------------------------------------------

    if COASTLINES: 
        #ax.coastlines(scale, **kwargs)  # Nah, use the crs.feature instead
        ax.add_feature(feature.COASTLINE.with_scale(scale),
                       **{**kwargs, **COASTLINES_kwargs})
        if verbose == 'debug': print('🐛 COASTLINES:', {**kwargs, **COASTLINES_kwargs})
    if BORDERS: 
        ax.add_feature(feature.BORDERS.with_scale(scale),
                       **{**kwargs, **BORDERS_kwargs})
        if verbose == 'debug': print('🐛 BORDERS:', {**kwargs, **BORDERS_kwargs})
    if STATES: 
        ax.add_feature(feature.STATES.with_scale(scale),
                       **{**kwargs, **STATES_kwargs})
        if verbose == 'debug': print('🐛 STATES:', {**kwargs, **STATES_kwargs})
    if COUNTIES:
        _counties_scale = {'20m', '5m', '500k'}
        assert counties_scale in _counties_scale, f"counties_scale must be {_counties_scale}"
        ax.add_feature(USCOUNTIES.with_scale(counties_scale),
                       **{**kwargs, **COUNTIES_kwargs})
        if verbose == 'debug': print('🐛 COUNTIES:', {**kwargs, **COUNTIES_kwargs})
    if OCEAN: 
        ax.add_feature(feature.OCEAN.with_scale(scale),
                       **{**kwargs, **OCEAN_kwargs})
        if verbose == 'debug': print('🐛 OCEAN:', {**kwargs, **OCEAN_kwargs})
    if LAND and not dark:
        # If `dark=True`, the face_color is the land color.
        ax.add_feature(feature.LAND.with_scale(scale), 
                       **{**kwargs, **LAND_kwargs})
        if verbose == 'debug': print('🐛 LAND:', {**kwargs, **LAND_kwargs})
    if RIVERS: 
        ax.add_feature(feature.RIVERS.with_scale(scale),
                       **{**kwargs, **RIVERS_kwargs})
        if verbose == 'debug': print('🐛 RIVERS:', {**kwargs, **RIVERS_kwargs})
    if LAKES: 
        ax.add_feature(feature.LAKES.with_scale(scale),
                       **{**kwargs, **LAKES_kwargs})
        if verbose == 'debug': print('🐛 LAKES:', {**kwargs, **LAKES_kwargs})
    if ROADS:
        ROADS_kwargs.setdefault('edgecolor', '#b30000')
        ROADS_kwargs.setdefault('facecolor', 'none')
        ROADS_kwargs.setdefault('linewidth', .2)
        
        if 'type' not in ROADS_kwargs:
            # Plot all roadways
            roads = feature.NaturalEarthFeature('cultural', 'roads', '10m',
                                                **ROADS_kwargs)
            ax.add_feature(roads)
        else:
            # Specify the type of road to include in plot
            road_types = ROADS_kwargs.pop('type')
            if isinstance(road_types, str): road_types = [road_types]
            shpfilename = shapereader.natural_earth('10m', 'cultural', 'roads')
            df = geopandas.read_file(shpfilename)
            _types = df['type'].unique()
            assert np.all([i in _types for i in road_types]), f"`ROADS_kwargs['type']` must be a list of these: {_types}"
            road_geos = df.loc[df['type'].apply(lambda x: x in road_types)].geometry.values
            ax.add_geometries(road_geos, crs=pc, **ROADS_kwargs)
        if verbose == 'debug': print('🐛 ROADS:', ROADS_kwargs)
    if STAMEN:
        if verbose: print("😎 Please use `ax.set_extent` before increasing Zoom level for faster plotting.")
        STAMEN_kwargs.setdefault('style', 'terrain-background')
        STAMEN_kwargs.setdefault('zoom', 3)
        
        stamen_terrain = cimgt.Stamen(STAMEN_kwargs['style'])
        ax.add_image(stamen_terrain, STAMEN_kwargs['zoom'])
        
        if 'alpha' in STAMEN_kwargs:
            # Need to manually put a white layer over the STAMEN terrain
            if dark:
                STAMEN_kwargs.setdefault('alpha_color', 'k')
            else:
                STAMEN_kwargs.setdefault('alpha_color', 'w')
            poly = ax.projection.domain
            ax.add_feature(feature.ShapelyFeature([poly], ax.projection),
                           color=STAMEN_kwargs['alpha_color'], 
                           alpha=1-STAMEN_kwargs['alpha'], 
                           zorder=1)
        if verbose == 'debug': print('🐛 STAMEN:', STAMEN_kwargs)
    if OSM:
        image = cimgt.OSM()
        OSM_kwargs.setdefault('zoom', 1)
        ax.add_image(image, OSM_kwargs['zoom'])
        if 'alpha' in OSM_kwargs:
            # Need to manually put a white layer over the STAMEN terrain
            if dark:
                OSM_kwargs.setdefault('alpha_color', 'k')
            else:
                OSM_kwargs.setdefault('alpha_color', 'w')
            poly = ax.projection.domain
            ax.add_feature(feature.ShapelyFeature([poly], ax.projection),
                           color=OSM_kwargs['alpha_color'], 
                           alpha=1-OSM_kwargs['alpha'], 
                           zorder=1)
        if verbose == 'debug': print('🐛 OSM:', OSM_kwargs)

    if figsize is not None:
        plt.gcf().set_figwidth(figsize[0])
        plt.gcf().set_figheight(figsize[1])
    if dpi is not None:
        plt.gcf().set_dpi(dpi)

    # Add my custom methods
    ax.__class__.adjust_extent = _adjust_extent
    ax.__class__.center_extent = _center_extent
    ax.__class__.copy_extent = _copy_extent

    return ax

########################################################################
# Adjust Map Extent
########################################################################

# OLD
def center_extent(lon, lat, *, ax=None, pad='auto', crs=pc, verbose=False):
    """
    Change the map extent to be centered on a point and adjust padding.

    Parameters
    ----------
    lon, lat : float
        Latitude and Longitude of the center point **in degrees**.
    ax : cartopy axes
        Default None will create a new PlateCarree cartopy.mpl.geoaxes.
    pad : float or dict
        Default is 'auto', which defaults to ~5 degree padding on each side.
        If float, pad the map the same on all sides (in crs units).
        If dict, specify pad on each side (in crs units).
            - 'top' - padding north of center point
            - 'bottom'- padding south of center point
            - 'left' - padding east of center point
            - 'right' - padding west of center point
            - 'default' - padding when pad is unspecified (default is 5)
        Example: ``pad=dict(top=5, default=10)`` is the same as
                 ``pad=dict(top=5, bottom=10, left=10, right=10)``
    crs : cartopy coordinate reference system
        Default is ccrs.PlateCarree()
    """
    warnings.warn("OLD Use the ax.center_extent method added to the axes by common_features")
    ax = check_cartopy_axes(ax, crs, verbose=verbose)

    # Convert input lat/lon in degrees to the crs units
    lon, lat = crs.transform_point(lon, lat, src_crs=pc)

    if pad == 'auto':
        pad = dict()
    
    if isinstance(pad, dict):
        # This default gives 5 degrees padding on each side
        # for a PlateCarree projection. Pad is similar for other 
        # projections but not exactly 5 degrees.
        xmin, xmax = crs.x_limits
        default_pad = (xmax-xmin)/72        # Because 360/72 = 5 degrees
        pad.setdefault('default', default_pad)
        for i in ['top', 'bottom', 'left', 'right']:
            pad.setdefault(i, pad['default'])
    else:
        pad = dict(top=pad, bottom=pad, left=pad, right=pad)
        
    ymin, ymax = crs.y_limits
    north = np.minimum(ymax, lat + pad['top'])
    south = np.maximum(ymin, lat - pad['bottom'])
    east = lon + pad['right']
    west = lon - pad['left']
    
    ax.set_extent([west, east, south, north], crs=crs)
    
    if verbose: print(f"📐 Padding from point for {crs.__class__}: {pad}")
        
    return ax.get_extent(crs=crs) 

# OLD
def adjust_extent(ax=None, pad='auto', fraction=.05, verbose=False):
    """
    Adjust the extent of an existing cartopy axes.

    This is useful to fine-tune the extent of a map after the extent 
    was automatically made by a cartopy plotting method.    
    
    Parameters
    ----------
    ax : cartopy axes
    pad : float or dict
        If float, pad the map the same on all sides. Default is half a degree.
        If dict, specify pad on each side.
            - 'top' - padding north of center point
            - 'bottom'- padding south of center point
            - 'left' - padding east of center point
            - 'right' - padding west of center point
            - 'default' - padding when pad is unspecified 
        Example: ``pad=dict(top=.5, default=.2)`` is the same as
                 ``pad=dict(top=.5, bottom=.2, left=.2, right=.2)``
        Note: Use negative numbers to remove padding.
    fraction : float
        When pad is 'auto', adjust the sides by a set fraction.
        The default 0.05 will give 5% padding on each side.
    """
    warnings.warn("OLD Use the ax.center_extent method added to the axes by common_features")
    # Can't shrink the map extent by more than half in each direction, duh.
    assert fraction > -.5, "Fraction must be larger than -0.5."
    
    ax = check_cartopy_axes(ax)
    
    crs = ax.projection
    
    west, east, south, north = ax.get_extent(crs=crs)

    if pad == 'auto':
        pad = {}
    
    if isinstance(pad, dict):
        xmin, xmax = ax.get_xlim()
        default_pad = (xmax-xmin) * fraction
        pad.setdefault('default', default_pad)
        for i in ['top', 'bottom', 'left', 'right']:
            pad.setdefault(i, pad['default'])
    else:
        pad = dict(top=pad, bottom=pad, left=pad, right=pad)

    ymin, ymax = crs.y_limits
    north = np.minimum(ymax, north + pad['top'])
    south = np.maximum(ymin, south - pad['bottom'])
    east = east + pad['right']
    west = west - pad['left']

    ax.set_extent([west, east, south, north], crs=crs)

    if verbose: print(f"📐 Adjust Padding for {crs.__class__}: {pad}")
    
    return ax.get_extent(crs=crs) 

# OLD
def copy_extent(src_ax, dst_ax):
    """
    Copy the extent from an axes. 
    
    .. note:: 
        Copying extent from different projections might not result in
        what you expect.

    Parameters
    ----------
    src_ax, dst_ax : cartopy axes
        A source cartopy axes to copy extent from onto the destination axes.
    """
    warnings.warn("OLD Use the ax.copy_extent method added to the axes by common_features")
    src_ax = check_cartopy_axes(src_ax)
    dst_ax = check_cartopy_axes(dst_ax)

    dst_ax.set_extent(src_ax.get_extent(crs=pc), crs=pc)

    return dst_ax.get_extent(crs=pc)

########################################################################
# Other
########################################################################

def domain_border(x, y=None, *, ax=None, text=None,
                  method='cutout', verbose=False,
                  facealpha=.25, polygon_only=False,
                  text_kwargs={}, **kwargs):
    """
    Add a polygon of the domain boundary to a map.

    The border is drawn from the outside values of the latitude and 
    longitude xarray coordinates or numpy array. 
    Lat/lon values should be given as degrees.

    Parameters
    ----------
        x : xarray.Dataset or numpy.ndarray
            If xarray, then should contain 'latitude' and 'longitude' coordinate.
            If numpy, then 2D numpy array for longitude and `y` arg is required.
        y : numpy.ndarray
            Only required if x is a numpy array.
            A numpy array of latitude values.
        ax : cartopy axis
            The axis to add the border to.
            Default None and will get the current axis (will create one).
        text : str
            If not None, puts the string in the bottom left.
        method : {'fill', 'cutout', 'border'}
            Plot the domain as a filled area Polygon, a Cutout from the
            map, or as a simple border.
        facealpha : float between 0 and 1
            Since there isn't a "facealpha" attribute for plotting,
            this will be it.
        polygon_only : bool
            - True: Only return the polygons and don't plot on axes.

    Returns
    -------
    Adds a border around domain to the axis and returns the artist, 
    a polygon in the crs coordinates and crs in lat/lon coordinates.
    """
    if hasattr(x, 'crs'):
        ax = check_cartopy_axes(ax, crs=x.crs)
        if verbose: print(f'crs is {x.crs}')
    else:
        print('crs is not in the xarray.Dataset')
        ax = check_cartopy_axes(ax)
    
    _method =  {'cutout', 'fill', 'border'}
    assert method in _method, f"Method must be one of {_method}."
    
    ####################################################################
    # Determine how to handle output...xarray or numpy
    if isinstance(x, (xr.core.dataset.Dataset, \
                      xr.core.dataarray.DataArray)):
        if verbose: print("process input as xarray")
        
        if 'latitude' in x.coords:
            x = x.rename({'latitude': 'lat',
                          'longitude': 'lon'})
        LON = x.lon.data
        LAT = x.lat.data
    
    elif isinstance(x, np.ndarray):
        assert y is not None, "Please supply a value for x and y"
        if verbose: print("process input as numpy array")
        LON = x
        LAT = y 
    else:
        raise ValueError("Review your input")
    ####################################################################
    
    # Path of array outside border starting from the lower left corner
    # and going around the array counter-clockwise.
    outside = list(zip(LON[0, :], LAT[0, :])) \
            + list(zip(LON[:, -1], LAT[:, -1])) \
            + list(zip(LON[-1, ::-1], LAT[-1, ::-1])) \
            + list(zip(LON[::-1, 0], LAT[::-1, 0]))
    outside = np.array(outside)
    
    ## Polygon in latlon coordinates
    ## -----------------------------
    x = outside[:, 0]
    y = outside[:, 1]
    domain_polygon_latlon = Polygon(zip(x, y))    
    
    ## Polygon in projection coordinates
    ## ----------------------------------
    transform = ax.projection.transform_points(pc, x, y)
    
    # Remove any points that run off the projection map (i.e., point's value is `inf`).
    transform = transform[~np.isinf(transform).any(axis=1)]
    
    # These are the x and y points we need to create the Polygon for
    x = transform[:, 0]
    y = transform[:, 1]
    
    domain_polygon = Polygon(zip(x, y))    # This is the boundary of the LAT/LON array supplied.
    global_polygon = ax.projection.domain  # This is the projection globe polygon
    cutout = global_polygon.difference(domain_polygon)  # This is the differencesbetween the domain and glob polygon
    
    if polygon_only:
        plt.close()
        return domain_polygon, domain_polygon_latlon
    else:
        # Plot
        kwargs.setdefault('edgecolors', 'k')
        kwargs.setdefault('linewidths', 1)
        if method=='fill':
            kwargs.setdefault('facecolor', (0,0,0,facealpha))
            artist = ax.add_feature(feature.ShapelyFeature([domain_polygon], ax.projection), **kwargs)
        elif method=='cutout':
            kwargs.setdefault('facecolor', (0,0,0,facealpha))
            artist = ax.add_feature(feature.ShapelyFeature([cutout], ax.projection), **kwargs)
        elif method=='border':
            kwargs.setdefault('facecolor', 'none')
            artist = ax.add_feature(feature.ShapelyFeature([domain_polygon.exterior], ax.projection), **kwargs)
            
        if text:
            text_kwargs.setdefault('verticalalignment', 'bottom')
            text_kwargs.setdefault('fontsize', 15)
            xx, yy = outside[0]
            ax.text(xx+.2, yy+.2, text, transform=pc, **text_kwargs)

        return artist, domain_polygon, domain_polygon_latlon