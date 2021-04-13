## Brian Blaylock
## April 13, 2021

"""
===============
Essential Tools
===============
Maybe I'm lazy, but I don't like typing `import numpy as np` in every script.
Instead, import all the tools you need in one line.

..code-block:: python

    from toolbox.tools import np, mpl, pd

"""

from toolbox.stock import Path  # This has a copy method added to the Path object

from datetime import datetime, timedelta

import numpy as np
import pandas as pd 
import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.patheffects as path_effects

