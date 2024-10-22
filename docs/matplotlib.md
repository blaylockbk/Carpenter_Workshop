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
