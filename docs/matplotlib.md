# Matplotlib

## Subplot Mosaic

[See documentation](https://matplotlib.org/stable/tutorials/provisional/mosaic.html)

```python
axd = plt.figure(constrained_layout=True).subplot_mosaic(
    """
    ABD
    CCD
    """
)
```

## Jupyter magic

Enable interactive figure manipulation in Jupyter.
https://github.com/matplotlib/ipympl
(Doesn't always behave the way I think it should.)

```python
%matplotlib widget

import matplotlib.pyplot as plt
```

## Placing Text with transform coordinates

```python
ax = plt.subplots(2, 3)
txt_fmt = {'horizontalalignment': 'center',
    'verticalalignment': 'center'}
plt.text(.5, .75, 'transFigure', transform=plt.gcf().transFigure,
    color='b', **txt_fmt)
plt.text(.5, .75, 'transAxes', transform=plt.gca().transAxes,
    color='r', **txt_fmt)

```

## Jupyter Figure Transparency

Use Jupyter Magic to give transparency to the figure displayed in the notebook

```python
%config InlineBackend.print_figure_kwargs = {'facecolor':'none'}
%config InlineBackend.print_figure_kwargs = {'facecolor' : 'w'}
```

## Style parameters

```python
# Use my custom style sheet (if in )
plt.style.use('BB_style')

# Change default date formatter
plt.rcParams['date.autoformatter.day'] = '%b %d\n%H:%M'
plt.rcParams['date.autoformatter.hour'] = '%b %d\n%H:%M'

# Put grid lines behind patches (i.e., bar plots)
plt.rcParams["axes.axisbelow"] = True

# Needed this to modify fonts in Adobe Illustrator
plt.rcParams['svg.fonttype'] = 'none'
```

## Stand-alone Colorbar

See my answer on Stack Overflow https://stackoverflow.com/a/62436015/2383070

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
fig = plt.figure()
ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])
cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal',
 cmap='gist_ncar',
 norm=mpl.colors.Normalize(0, 10), # vmax and vmin
 extend='both',
 label='This is a label',
 ticks=[0, 3, 6, 9])
plt.savefig('just_colorbar', bbox_inches='tight')

```

## Discrete Colormap and Norm

```python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

cmap = plt.get_cmap('bwr', 10)
norm = mcolors.Normalize(vmin=5, vmax=10)
plt.pcolormesh(np.random.rand(10,10)*8+5, cmap=cmap, norm=norm)
plt.colorbar()

# or, make colormap index based on discrete intervals

cmap = plt.get_cmap('bwr', 10)
norm = mcolors.BoundaryNorm([1,2,5,8,10], 10)
plt.pcolormesh(np.random.rand(10,10)*8+2, cmap=cmap, norm=norm)
plt.colorbar(spacing='proportional')
```

## Dates

```python
import matplotlib.dates as mdates
formatter = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(formatter)
```

```python
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.HourLocator(range(0, 24, 3)))
ax.xaxis.set_minor_locator(mdates.HourLocator(range(0, 24, 1)))
```

Set date autoformatter:

```python
plt.rcParams['date.autoformatter.day'] = '%b %d\n%H:%M'
plt.rcParams['date.autoformatter.hour'] = '%b %d\n%H:%M'
```

Set date ticks

```python
from matplotlib.dates import HourLocator, DateFormatter
plt.plot(pd.date_range('2017-01-01', '2017-01-02', freq='h'), range(25))
plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(0,24,6)))
plt.gca().xaxis.set_major_formatter(DateFormatter('%d %b %Y\n%H:%M\n%A'))
```

## Colorbars

Custom discreate range

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
data = np.random.rand(5, 5)*100
bounds = [5, 15, 35, 65, 100]
cmap = plt.get_cmap('Spectral_r', len(bounds))
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
plt.pcolormesh(data, cmap=cmap, norm=norm)
plt.colorbar(spacing='proportional')
```

Adjust colorbar object

```python
import numpy as np
import matplotlib.pyplot as plt
data = np.random.rand(5, 5)*100
fig = plt.figure()
plt.pcolormesh(data)
plt.colorbar()
print(fig.axes)
fig.axes[1].tick_params(labelsize=30)
```

Colorbar fraction size to match axes

```python
# The magic number is 0.045
# Left plot
plt.colorbar()
# Right plot
plt.colorbar(fraction=0.045)

```

## Latex Strings

The syntax depends on the character you use. Some require an escape character or use the raw string format.

```python
# Greek Letters
plt.title('$\\theta$') # Use the \\ to escape single \, because \t means tab
plt.title(r'$\theta$') # or, use raw string r''
plt.title('$\\alpha$')
plt.title('$\Delta$')  # Does not require \\ or r''

# Superscript (e.g. wind speed m/s, FSOI J/kg, PM2.5 ug/m3)
plt.ylabel('Wind Speed (m s${^{-1}}$)')
plt.xlabel('FSOI (J kg$^{-1}$)')
plt.ylabel('PM 2.5 Concentration ($\mu$g m${^{-3}}$)')

# Subscript (e.g., CO_2, theta_surface)
plt.ylabel('CO$_2$ (ppm)')
plt.ylabel('$\\theta$${_{surface}}$')  #
plt.ylabel('$\\theta\mathregular{_{surface}}$')  # use \mathregular for non-italics

# Temperature Degree
plt.ylabel('Temperature ($\degree$C)')

```

